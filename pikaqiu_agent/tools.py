"""LangChain Tool definitions for the PikaQiu Agent sandbox and knowledge base."""
from __future__ import annotations

import json
import logging
from typing import Callable

from langchain_core.tools import tool, BaseTool
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


def _clamp_timeout(timeout: int, max_timeout: int, min_timeout: int = 1) -> int:
    return max(min_timeout, min(int(timeout), max_timeout))


def _format_sandbox_result(prefix: str, result) -> str:
    parts = [prefix]
    if result.stdout:
        parts.append(result.stdout)
    if result.stderr:
        parts.append(f"[STDERR] {result.stderr}")
    parts.append(f"[EXIT_CODE: {result.exit_code}]")
    return "\n".join(parts)


def _has_serialization_keywords(code: str) -> bool:
    keywords = ("pickle", "serialize", "marshal", "yaml.load", "ObjectInputStream", "unserialize")
    lowered = code.lower()
    return any(keyword.lower() in lowered for keyword in keywords)


# ── Input schemas ──────────────────────────────────────────────────────

class BashInput(BaseModel):
    command: str = Field(description="The bash command to execute")
    timeout: int = Field(default=60, description="Timeout in seconds. For long tools like sqlmap/nmap use background: cmd > /tmp/out.txt 2>&1 & then check results later.")


class PythonInput(BaseModel):
    code: str = Field(description="Python source code to execute")
    timeout: int = Field(default=60, description="Timeout in seconds.")


class KnowledgeSearchInput(BaseModel):
    query: str = Field(description="Search query (keywords, CVE IDs, technique names)")
    limit: int = Field(default=6, description="Maximum number of results")


class WebSearchInput(BaseModel):
    query: str = Field(description="Internet search query for public web pages, CVEs, exploit writeups, docs, or error messages")
    limit: int = Field(default=5, description="Maximum number of search results, capped at 10")
    timeout: int = Field(default=20, description="Timeout in seconds, capped by command timeout")


class WebFetchInput(BaseModel):
    url: str = Field(description="HTTP/HTTPS URL to fetch from the public internet")
    max_chars: int = Field(default=12000, description="Maximum extracted text characters to return, capped at 30000")
    timeout: int = Field(default=20, description="Timeout in seconds, capped by command timeout")


class CVESearchInput(BaseModel):
    product: str = Field(default="", description="Product name (e.g., 'thinkphp', 'shiro', 'weblogic', 'tomcat', 'spring', 'fastjson', 'redis', '致远OA', '泛微OA')")
    version: str = Field(default="", description="Target version (e.g., '5.0.23', '1.2.4'). Used for version-range matching.")
    cve_id: str = Field(default="", description="CVE ID (e.g., 'CVE-2021-44228')")
    vuln_type: str = Field(default="", description="Vulnerability type filter: rce, sqli, xss, ssrf, ssti, deserialization, file_upload, lfi, auth_bypass, unauth, info_leak, privesc")
    keyword: str = Field(default="", description="Free-text keyword search in title/description")
    limit: int = Field(default=8, description="Max results")


class AdviserInput(BaseModel):
    question: str = Field(description="Specific question about attack technique, payload, or next step")


class SubmitFlagInput(BaseModel):
    flag: str = Field(description="The captured flag string (e.g. flag{...} or CTF{...})")


# ── Tool factories ─────────────────────────────────────────────────────

def create_bash_tool(sandbox, workdir: str, stop_fn: Callable[[], bool] | None = None, on_chunk: Callable[[str], None] | None = None, max_timeout: int = 120) -> BaseTool:
    @tool("bash_exec", args_schema=BashInput)
    def bash_exec(command: str, timeout: int = 60) -> str:
        """Execute a bash command in the Kali Linux sandbox.
        Use for recon and exploitation.
        For long-running tools (nmap/sqlmap/gobuster), run in background and check results:
          nohup sqlmap ... > /tmp/sqlmap.log 2>&1 &
          sleep 30 && tail -50 /tmp/sqlmap.log
        """
        timeout = _clamp_timeout(timeout, max_timeout)
        result = sandbox.run(command, timeout_sec=timeout, workdir=workdir, stop_fn=stop_fn, on_chunk=on_chunk)
        return _format_sandbox_result("[输出为Kali沙箱中的本地执行结果，并非远程目标输出]", result)
    return bash_exec


def create_python_tool(sandbox, workdir: str, stop_fn: Callable[[], bool] | None = None, on_chunk: Callable[[str], None] | None = None, max_timeout: int = 120) -> BaseTool:
    @tool("python_exec", args_schema=PythonInput)
    def python_exec(code: str, timeout: int = 60) -> str:
        """Execute Python code in the Kali sandbox.
        Preferred for HTTP sessions, cookies, JSON parsing, complex logic.

        CRITICAL: Each call is an ISOLATED process — variables/sessions from previous
        calls are GONE. Login + all operations MUST be in the same call.
        If you need to maintain a session (cookies etc.), you must login again in each call.
        Code is sent via base64 — no escaping needed.
        """
        timeout = _clamp_timeout(timeout, max_timeout)
        result = sandbox.run_python(code, timeout_sec=timeout, workdir=workdir, stop_fn=stop_fn, on_chunk=on_chunk)
        parts = [_format_sandbox_result("[以下是Kali沙箱中的Python执行结果]", result)]
        # Context reminder for serialization payloads
        if _has_serialization_keywords(code):
            parts.append("[提醒] 脚本中包含序列化/反序列化操作。构造payload的过程中，命令可能在本地沙箱执行，如果看到命令执行结果请注意区分"
                         "只有通过网络请求(requests/curl)发送到目标的结果才是远程响应，但确保你将他们区分开了。如果只有一个命令执行结果，大概率是构造payload时的本地执行结果。本提示为系统提示")
        return "\n".join(parts)
    return python_exec


def create_web_search_tool(
    sandbox,
    workdir: str,
    stop_fn: Callable[[], bool] | None = None,
    on_chunk: Callable[[str], None] | None = None,
    max_timeout: int = 120,
) -> BaseTool:
    @tool("web_search", args_schema=WebSearchInput)
    def web_search(query: str, limit: int = 5, timeout: int = 20) -> str:
        """Search the public internet from inside the Kali sandbox.

        Use for current CVE/exploit research, public docs, writeups, and exact
        error strings when the offline knowledge base is insufficient.
        Returns title, URL, and snippet for each result. Use web_fetch for a URL.
        """
        limit = max(1, min(int(limit or 5), 10))
        timeout = _clamp_timeout(int(timeout or 20), max_timeout, min_timeout=5)
        code = f"""
import html
import json
import re
import sys
import urllib.parse
import urllib.request

query = {json.dumps(query)}
limit = {limit}
timeout = {timeout}
ua = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 PikaQiu-Agent/1.0"

def clean_html(value):
    value = html.unescape(value or "")
    value = re.sub(r"(?is)<(script|style|svg|noscript).*?</\\1>", " ", value)
    value = re.sub(r"(?s)<[^>]+>", " ", value)
    value = re.sub(r"\\s+", " ", value)
    return value.strip()

def normalize_url(href):
    href = html.unescape(href or "").strip()
    if href.startswith("//"):
        href = "https:" + href
    parsed = urllib.parse.urlparse(href)
    qs = urllib.parse.parse_qs(parsed.query)
    if "uddg" in qs and qs["uddg"]:
        href = qs["uddg"][0]
    return href

def search_duckduckgo():
    url = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote_plus(query)
    req = urllib.request.Request(url, headers={{"User-Agent": ua, "Accept-Language": "en-US,en;q=0.8"}})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        body = resp.read(1200000).decode(resp.headers.get_content_charset() or "utf-8", "replace")

    results = []
    matches = list(re.finditer(r'<a[^>]+class="[^"]*result__a[^"]*"[^>]+href="([^"]+)"[^>]*>(.*?)</a>', body, re.I | re.S))
    for idx, match in enumerate(matches):
        if len(results) >= limit:
            break
        href = normalize_url(match.group(1))
        title = clean_html(match.group(2))
        next_start = matches[idx + 1].start() if idx + 1 < len(matches) else len(body)
        block = body[match.end():next_start]
        snippet_match = re.search(r'<a[^>]+class="[^"]*result__snippet[^"]*"[^>]*>(.*?)</a>|<div[^>]+class="[^"]*result__snippet[^"]*"[^>]*>(.*?)</div>', block, re.I | re.S)
        snippet = clean_html((snippet_match.group(1) or snippet_match.group(2)) if snippet_match else "")
        if title and href.startswith(("http://", "https://")):
            results.append({{"title": title, "url": href, "snippet": snippet}})
    return results

try:
    results = search_duckduckgo()
    print(json.dumps({{"query": query, "results": results}}, ensure_ascii=False, indent=2))
except Exception as exc:
    print(json.dumps({{"query": query, "error": str(exc), "results": []}}, ensure_ascii=False, indent=2))
    sys.exit(1)
"""
        result = sandbox.run_python(code, timeout_sec=timeout, workdir=workdir, stop_fn=stop_fn, on_chunk=on_chunk)
        return _format_sandbox_result(f"[web_search query] {query}", result)
    return web_search


def create_web_fetch_tool(
    sandbox,
    workdir: str,
    stop_fn: Callable[[], bool] | None = None,
    on_chunk: Callable[[str], None] | None = None,
    max_timeout: int = 120,
) -> BaseTool:
    @tool("web_fetch", args_schema=WebFetchInput)
    def web_fetch(url: str, max_chars: int = 12000, timeout: int = 20) -> str:
        """Fetch an HTTP/HTTPS page from the public internet and extract readable text.

        Use after web_search when a result looks relevant. Prefer official docs,
        advisories, Exploit-DB, NVD, GitHub PoCs, and vendor pages.
        """
        max_chars = max(1000, min(int(max_chars or 12000), 30000))
        timeout = _clamp_timeout(int(timeout or 20), max_timeout, min_timeout=5)
        code = f"""
import html
import json
import re
import sys
import urllib.request

url = {json.dumps(url)}
max_chars = {max_chars}
timeout = {timeout}
ua = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 PikaQiu-Agent/1.0"

if not re.match(r"^https?://", url, re.I):
    print(json.dumps({{"url": url, "error": "only http/https URLs are supported"}}, ensure_ascii=False, indent=2))
    sys.exit(2)

try:
    req = urllib.request.Request(url, headers={{"User-Agent": ua, "Accept-Language": "en-US,en;q=0.8"}})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        status = getattr(resp, "status", 0)
        final_url = resp.geturl()
        content_type = resp.headers.get("content-type", "")
        charset = resp.headers.get_content_charset() or "utf-8"
        raw = resp.read(min(max_chars * 8, 1500000))
    text = raw.decode(charset, "replace")
    title = ""
    if "html" in content_type.lower() or "<html" in text[:500].lower():
        m = re.search(r"(?is)<title[^>]*>(.*?)</title>", text)
        title = html.unescape(re.sub(r"\\s+", " ", m.group(1))).strip() if m else ""
        text = re.sub(r"(?is)<(script|style|svg|noscript).*?</\\1>", " ", text)
        text = re.sub(r"(?s)<br\\s*/?>", "\\n", text)
        text = re.sub(r"(?s)</(p|div|li|h[1-6]|tr)>", "\\n", text)
        text = re.sub(r"(?s)<[^>]+>", " ", text)
        text = html.unescape(text)
    text = re.sub(r"[ \\t\\r\\f\\v]+", " ", text)
    text = re.sub(r"\\n\\s*\\n\\s*\\n+", "\\n\\n", text).strip()
    if len(text) > max_chars:
        text = text[:max_chars] + "\\n... [truncated]"
    print(json.dumps({{
        "url": url,
        "final_url": final_url,
        "status": status,
        "content_type": content_type,
        "title": title,
        "text": text,
    }}, ensure_ascii=False, indent=2))
except Exception as exc:
    print(json.dumps({{"url": url, "error": str(exc)}}, ensure_ascii=False, indent=2))
    sys.exit(1)
"""
        result = sandbox.run_python(code, timeout_sec=timeout, workdir=workdir, stop_fn=stop_fn, on_chunk=on_chunk)
        return _format_sandbox_result(f"[web_fetch url] {url}", result)
    return web_fetch


def create_knowledge_tool(knowledge, top_k: int = 3) -> BaseTool:
    @tool("knowledge_search", args_schema=KnowledgeSearchInput)
    def knowledge_search(query: str, limit: int = top_k) -> str:
        """Search the offline cybersecurity knowledge base.
        Contains HackTricks, PayloadsAllTheThings, CVE database with PoCs, pentest cheatsheets.
        Use for payloads, CVE details, and exploitation techniques.
        Returns full document content for each match.
        """
        try:
            results = knowledge.search(query, limit=limit)
            if not results:
                return f"[knowledge_search] No results for: {query}"
            formatted = []
            for item in results:
                entry = f"### {item.get('title', 'untitled')} [{item.get('source', '')}]\n"
                body = item.get("body") or item.get("snippet") or ""
                if body:
                    entry += body
                formatted.append(entry)
            return "\n---\n".join(formatted)
        except Exception as e:
            return f"[knowledge_search error] {e}"
    return knowledge_search


def create_cve_search_tool(store) -> BaseTool:
    @tool("search_cve", args_schema=CVESearchInput)
    def search_cve(
        product: str = "",
        version: str = "",
        cve_id: str = "",
        vuln_type: str = "",
        keyword: str = "",
        limit: int = 8,
    ) -> str:
        """Search the CVE/POC database for known vulnerabilities.
        Use when you identify a specific product+version and need matching CVEs/exploits.
        Examples:
          search_cve(product="thinkphp", version="5.0.23")
          search_cve(product="shiro")
          search_cve(cve_id="CVE-2021-44228")
          search_cve(product="weblogic", vuln_type="deserialization")
          search_cve(product="redis", version="5.0.5")
        """
        try:
            results = store.search_cve_poc(
                product=product,
                version=version,
                cve_id=cve_id,
                vuln_type=vuln_type,
                keyword=keyword,
                limit=limit,
            )
            if not results:
                parts = []
                if product:
                    parts.append(f"product={product}")
                if version:
                    parts.append(f"version={version}")
                if cve_id:
                    parts.append(f"cve={cve_id}")
                if vuln_type:
                    parts.append(f"type={vuln_type}")
                if keyword:
                    parts.append(f"keyword={keyword}")
                return f"[search_cve] No matches for: {', '.join(parts) or 'empty query'}"

            formatted = []
            for item in results:
                lines = []
                title = item.get("title", "untitled")
                cve = item.get("cve_id", "")
                prod = item.get("product", "")
                ver = item.get("version_info", "")
                vtype = item.get("vuln_type", "")

                header = f"### {title}"
                if cve:
                    header += f" [{cve}]"
                lines.append(header)

                meta_parts = []
                if prod:
                    meta_parts.append(f"Product: {prod}")
                if ver:
                    meta_parts.append(f"Version: {ver}")
                if vtype:
                    meta_parts.append(f"Type: {vtype}")
                if meta_parts:
                    lines.append(" | ".join(meta_parts))

                poc_path = item.get("poc_path", "")
                poc_url = item.get("poc_url", "")
                poc_content = item.get("poc_content", "")
                if poc_path:
                    lines.append(f"POC: {poc_path} (local)")
                elif poc_url:
                    lines.append(f"Ref: {poc_url}")

                if poc_content:
                    # Truncate very long content to keep response manageable
                    if len(poc_content) > 8000:
                        poc_content = poc_content[:8000] + "\n... [truncated]"
                    lines.append(f"--- POC Content ---\n{poc_content}")

                formatted.append("\n".join(lines))
            return "\n---\n".join(formatted)
        except Exception as e:
            return f"[search_cve error] {e}"
    return search_cve


def create_adviser_tool(
    llm_client, mission: dict, memory: dict | None = None,
    current_messages: list | None = None,
) -> BaseTool:
    @tool("ask_adviser", args_schema=AdviserInput)
    def ask_adviser(question: str) -> str:
        """Ask the expert penetration testing adviser.
        Use when stuck, need specific payloads, or bypass techniques.
        Be specific: include what you tried, errors, and what you expect.
        """
        context_parts = [
            f"目标: {mission.get('target', '')}",
            f"任务目标: {mission.get('goal', '')}",
        ]
        if memory:
            if memory.get("summary"):
                context_parts.append(f"当前态势: {memory['summary']}")
            if memory.get("findings"):
                findings = "\n".join(f"- {f}" for f in memory["findings"][:8])
                context_parts.append(f"已知发现:\n{findings}")
            if memory.get("leads"):
                leads = "\n".join(f"- {l}" for l in memory["leads"][:5])
                context_parts.append(f"待验证线索:\n{leads}")
            if memory.get("dead_ends"):
                dead = ", ".join(str(d) for d in memory["dead_ends"][:5])
                context_parts.append(f"已排除路径: {dead}")

        # Append recent tool execution history from current round
        if current_messages:
            from langchain_core.messages import AIMessage as _AI, ToolMessage as _TM
            recent = []
            for msg in current_messages[-30:]:
                if isinstance(msg, _AI) and msg.content:
                    text = str(msg.content)[:200]
                    recent.append(f"[AI] {text}")
                elif isinstance(msg, _TM):
                    text = str(msg.content)[:400]
                    recent.append(f"[工具结果] {text}")
            if recent:
                context_parts.append("本轮最近操作:\n" + "\n".join(recent[-15:]))

        context = "\n".join(context_parts)
        prompt = (
            f"## 渗透现状\n{context}\n\n"
            f"## 当前提问者的疑问\n{question}\n\n"
            "## 请你独立评估\n"
            "1. 基于以上上下文，当前渗透路径是否正确？有无被忽略的攻击向量？\n"
            "2. 如果方向有问题，直接指出并说明正确方向。\n"
            "3. 针对提问者的具体问题，给出可直接执行的命令或代码。"
        )
        result = llm_client.invoke_advisor(prompt)
        return result.raw_text
    return ask_adviser


def create_submit_flag_tool(on_flag: Callable[[str], str]) -> BaseTool:
        @tool("submit_flag", args_schema=SubmitFlagInput)
        def submit_flag(flag: str) -> str:
                """Submit the captured flag string found by exploiting the target.

                CRITICAL RULES:
                - Only call this with a flag string you ACTUALLY FOUND in the target's response,
                    file system, database output, or cookie value — obtained through exploitation.
                - NEVER fabricate, invent, or guess a flag to test this tool.
                - NEVER submit flag{test_...}, flag{example}, or any string you made up.
                - This is NOT a way to probe whether flags are accepted. Only call it when
                    you have a real flag from the target.

                If you found a string matching the flag format in the target response, submit it here.
                """
                return on_flag(flag.strip())

        return submit_flag


class GiveUpInput(BaseModel):
    reason: str = Field(description="详细说明已尝试过的所有攻击方法及其失败原因")


def create_give_up_tool(on_give_up: Callable[[str], str]) -> BaseTool:
    @tool("give_up", args_schema=GiveUpInput)
    def give_up(reason: str) -> str:
        """放弃当前渗透测试任务。

        ⚠️ 严格限制 — 仅在以下条件全部满足时才可调用：
        1. 你已尝试了所有可能的攻击向量，包括但不限于：
           端口/服务扫描、目录枚举、SQL注入、XSS、命令注入、文件包含/上传、
           SSRF、反序列化、认证绕过、信息泄露、已知CVE利用等
        2. 每种方法都已实际执行并确认失败（不是"觉得不行"就跳过）
        3. 你已参考了提示信息（如有）并按提示方向深入尝试
        4. 确实无法取得任何进展

        禁止在以下情况调用：
        - 才尝试了几种方法就想放弃
        - 遇到一两次报错就认为做不了
        - 没有按照提示方向充分探索

        调用时必须在reason中列出所有已尝试的方法和失败原因。
        """
        return on_give_up(reason.strip())
    return give_up


def create_all_tools(
    sandbox,
    workdir: str,
    store=None,
    knowledge=None,
    llm_client=None,
    mission: dict | None = None,
    memory: dict | None = None,
    on_flag: Callable[[str], str] | None = None,
    on_give_up: Callable[[str], str] | None = None,
    stop_fn: Callable[[], bool] | None = None,
    on_chunk: Callable[[str], None] | None = None,
    knowledge_top_k: int = 3,
    current_messages: list | None = None,
    command_timeout_sec: int = 120,
) -> list[BaseTool]:
    """Create all tools for a mission round."""
    tools: list[BaseTool] = [
        create_bash_tool(sandbox, workdir, stop_fn=stop_fn, on_chunk=on_chunk, max_timeout=command_timeout_sec),
        create_python_tool(sandbox, workdir, stop_fn=stop_fn, on_chunk=on_chunk, max_timeout=command_timeout_sec),
        create_web_search_tool(sandbox, workdir, stop_fn=stop_fn, on_chunk=on_chunk, max_timeout=command_timeout_sec),
        create_web_fetch_tool(sandbox, workdir, stop_fn=stop_fn, on_chunk=on_chunk, max_timeout=command_timeout_sec),
    ]
    if knowledge:
        tools.append(create_knowledge_tool(knowledge, top_k=knowledge_top_k))
    if store:
        tools.append(create_cve_search_tool(store))
    if llm_client and mission:
        tools.append(create_adviser_tool(llm_client, mission, memory=memory, current_messages=current_messages))
    if on_flag:
        tools.append(create_submit_flag_tool(on_flag))
    if on_give_up:
        tools.append(create_give_up_tool(on_give_up))
    return tools
