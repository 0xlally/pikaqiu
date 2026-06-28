"""LangChain Tool definitions for the PikaQiu Agent sandbox and knowledge base."""
from __future__ import annotations

import json
import logging
import random
import time
from typing import Any, Callable, Literal

from langchain_core.tools import tool, BaseTool
from pydantic import BaseModel, Field

from pikaqiu_agent.flag_capture import is_valid_flag
from pikaqiu_agent.output_truncation import (
    DEFAULT_MAX_OUTPUT_TOKENS,
    approx_token_count,
    formatted_truncate_text,
    resolve_max_tokens,
)

logger = logging.getLogger(__name__)


def _clamp_timeout(timeout: int, max_timeout: int, min_timeout: int = 1) -> int:
    return max(min_timeout, min(int(timeout), max_timeout))


def _resolve_timeout(timeout: int | None, max_timeout: int, min_timeout: int = 1) -> int:
    if timeout is None:
        return max(min_timeout, int(max_timeout))
    return _clamp_timeout(timeout, max_timeout, min_timeout)


def _sandbox_output_text(result) -> str:
    output = getattr(result, "output", None)
    if output is not None:
        return str(output)
    parts = []
    if getattr(result, "stdout", ""):
        parts.append(str(result.stdout))
    if getattr(result, "stderr", ""):
        parts.append(f"[STDERR] {result.stderr}")
    return "\n".join(parts)


def _generate_chunk_id() -> str:
    return "".join(f"{random.randrange(16):x}" for _ in range(6))


def _effective_max_output_tokens(
    requested: int | None,
    *,
    cap: int | None = DEFAULT_MAX_OUTPUT_TOKENS,
) -> int:
    max_tokens = resolve_max_tokens(requested)
    if cap is None:
        return max_tokens
    return min(max_tokens, resolve_max_tokens(cap))


def _format_sandbox_result(
    result,
    *,
    wall_time: float,
    max_output_tokens: int | None = None,
    max_output_tokens_cap: int | None = DEFAULT_MAX_OUTPUT_TOKENS,
) -> str:
    output_text = _sandbox_output_text(result)
    max_tokens = _effective_max_output_tokens(
        max_output_tokens,
        cap=max_output_tokens_cap,
    )
    return "\n".join(
        [
            f"Chunk ID: {_generate_chunk_id()}",
            f"Wall time: {wall_time:.4f} seconds",
            f"Process exited with code {int(getattr(result, 'exit_code', -1))}",
            f"Original token count: {approx_token_count(output_text)}",
            "Output:",
            formatted_truncate_text(output_text, max_tokens=max_tokens),
        ]
    )


def _truncate_end(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    return text[:limit] + f"\n... [truncated {len(text) - limit} chars]"


def _jsonable_tool_arg(value: Any) -> Any:
    if isinstance(value, BaseModel):
        return value.model_dump(exclude_none=True)
    if isinstance(value, dict):
        return {str(k): _jsonable_tool_arg(v) for k, v in value.items() if v is not None}
    if isinstance(value, (list, tuple)):
        return [_jsonable_tool_arg(item) for item in value if item is not None]
    return value


# ── Input schemas ──────────────────────────────────────────────────────

class BashInput(BaseModel):
    command: str = Field(description="The bash command to execute")
    timeout: int | None = Field(
        default=None,
        description=(
            "Optional timeout in seconds. Omit to use the mission command timeout. "
            "Values above the mission command timeout are capped."
        ),
    )
    max_output_tokens: int | None = Field(
        default=None,
        description="Optional maximum approximate output tokens returned to the model.",
    )


class PythonInput(BaseModel):
    code: str = Field(description="Python source code to execute")
    timeout: int | None = Field(
        default=None,
        description=(
            "Optional timeout in seconds. Omit to use the mission command timeout. "
            "Values above the mission command timeout are capped."
        ),
    )
    max_output_tokens: int | None = Field(
        default=None,
        description="Optional maximum approximate output tokens returned to the model.",
    )


class KnowledgeSearchInput(BaseModel):
    query: str = Field(description="Search query (keywords, CVE IDs, technique names)")
    limit: int = Field(default=6, description="Maximum number of results")


class WebSearchQueryInput(BaseModel):
    q: str = Field(description="Search query")
    recency: int | None = Field(default=None, description="Optional recency filter in days")
    domains: list[str] | None = Field(default=None, description="Optional domains to restrict results")


class WebSearchOpenInput(BaseModel):
    ref_id: str = Field(description="Reference id returned by web_search, or a direct HTTP/HTTPS URL")
    lineno: int | None = Field(default=None, description="Optional 1-based line number to start from")


class WebSearchClickInput(BaseModel):
    ref_id: str = Field(description="Reference id for a previously opened page")
    id: int = Field(description="Numbered link id from that page")


class WebSearchFindInput(BaseModel):
    ref_id: str = Field(description="Reference id returned by web_search, or a direct HTTP/HTTPS URL")
    pattern: str = Field(description="Text pattern to find in the page")


class WebSearchInput(BaseModel):
    search_query: list[WebSearchQueryInput] | None = Field(
        default=None,
        description="Search the internet for one or more queries. At most four queries per call.",
    )
    image_query: list[WebSearchQueryInput] | None = Field(
        default=None,
        description="Accepted for Codex-compatible shape; currently handled as text search.",
    )
    open: list[WebSearchOpenInput] | None = Field(
        default=None,
        description="Open pages by reference id or direct URL and extract readable text.",
    )
    click: list[WebSearchClickInput] | None = Field(
        default=None,
        description="Open a numbered link from a previously opened page.",
    )
    find: list[WebSearchFindInput] | None = Field(
        default=None,
        description="Find text patterns in opened pages or direct URLs.",
    )
    response_length: Literal["short", "medium", "long"] | None = Field(
        default="medium",
        description="How much result text to return.",
    )
    timeout: int | None = Field(
        default=None,
        description=(
            "Optional timeout in seconds. Omit to use the mission command timeout. "
            "Values above the mission command timeout are capped."
        ),
    )
    max_output_tokens: int | None = Field(
        default=None,
        description="Optional maximum approximate output tokens returned to the model.",
    )


class SubmitFlagInput(BaseModel):
    flag: str = Field(description="The captured flag string. Accepted prefixes: flag{...}, FLAG{...}, ctf{...}, CTF{...}")


class SkillSearchInput(BaseModel):
    query: str = Field(
        description=(
            "Specific basis for matching skills, such as product/version, endpoint or parameter behavior, "
            "framework error, file type, likely vulnerability class, failing tool output, or mission phase"
        )
    )
    limit: int = Field(default=5, description="Maximum number of matching skills")


class ActivateSkillInput(BaseModel):
    skill_id: str = Field(description="Skill id to activate, such as recon, ffuf-skill, or remote-cmd-execution")
    reason: str = Field(
        default="",
        description="Why this skill fits the current situation or next phase; avoid generic labels or startup guesses",
    )


class SkillReferenceInput(BaseModel):
    skill_id: str = Field(description="Skill id")
    path: str = Field(description="Reference path inside the skill directory")
    max_chars: int = Field(default=20000, description="Maximum characters to return")


# ── Tool factories ─────────────────────────────────────────────────────

def create_bash_tool(
    sandbox,
    workdir: str,
    stop_fn: Callable[[], bool] | None = None,
    on_chunk: Callable[[str], None] | None = None,
    max_timeout: int = 300,
    max_output_tokens_cap: int | None = DEFAULT_MAX_OUTPUT_TOKENS,
) -> BaseTool:
    @tool("bash_exec", args_schema=BashInput)
    def bash_exec(command: str, timeout: int | None = None, max_output_tokens: int | None = None) -> str:
        """Execute a bash command in the Kali Linux sandbox.
        Use for recon and exploitation.
        Do not hide stderr with 2>/dev/null while validating a command; tool errors
        and missing wordlists must stay visible.
        """
        timeout = _resolve_timeout(timeout, max_timeout)
        started = time.monotonic()
        result = sandbox.run(command, timeout_sec=timeout, workdir=workdir, stop_fn=stop_fn, on_chunk=on_chunk)
        return _format_sandbox_result(
            result,
            wall_time=time.monotonic() - started,
            max_output_tokens=max_output_tokens,
            max_output_tokens_cap=max_output_tokens_cap,
        )
    return bash_exec


def create_python_tool(
    sandbox,
    workdir: str,
    stop_fn: Callable[[], bool] | None = None,
    on_chunk: Callable[[str], None] | None = None,
    max_timeout: int = 300,
    max_output_tokens_cap: int | None = DEFAULT_MAX_OUTPUT_TOKENS,
) -> BaseTool:
    @tool("python_exec", args_schema=PythonInput)
    def python_exec(code: str, timeout: int | None = None, max_output_tokens: int | None = None) -> str:
        """Execute Python code in the Kali sandbox.
        Preferred for HTTP sessions, cookies, JSON parsing, complex logic.

        CRITICAL: Each call is an ISOLATED process — variables/sessions from previous
        calls are GONE. Login + all operations MUST be in the same call.
        If you need to maintain a session (cookies etc.), you must login again in each call.
        Code is sent via base64 — no escaping needed.
        """
        timeout = _resolve_timeout(timeout, max_timeout)
        started = time.monotonic()
        result = sandbox.run_python(code, timeout_sec=timeout, workdir=workdir, stop_fn=stop_fn, on_chunk=on_chunk)
        return _format_sandbox_result(
            result,
            wall_time=time.monotonic() - started,
            max_output_tokens=max_output_tokens,
            max_output_tokens_cap=max_output_tokens_cap,
        )
    return python_exec


def create_web_search_tool(
    sandbox,
    workdir: str,
    stop_fn: Callable[[], bool] | None = None,
    on_chunk: Callable[[str], None] | None = None,
    max_timeout: int = 300,
    max_output_tokens_cap: int | None = DEFAULT_MAX_OUTPUT_TOKENS,
    web_search_base_url: str = "",
    web_search_api_key: str = "",
    web_search_model: str = "",
) -> BaseTool:
    @tool("web_search", args_schema=WebSearchInput)
    def web_search(
        search_query: list[dict[str, Any]] | None = None,
        image_query: list[dict[str, Any]] | None = None,
        open: list[dict[str, Any]] | None = None,
        click: list[dict[str, Any]] | None = None,
        find: list[dict[str, Any]] | None = None,
        response_length: str | None = "medium",
        timeout: int | None = None,
        max_output_tokens: int | None = None,
    ) -> str:
        """联网搜索工具。"""
        timeout = _resolve_timeout(timeout, max_timeout)
        commands = {
            "search_query": _jsonable_tool_arg(search_query),
            "image_query": _jsonable_tool_arg(image_query),
            "open": _jsonable_tool_arg(open),
            "click": _jsonable_tool_arg(click),
            "find": _jsonable_tool_arg(find),
            "response_length": response_length or "medium",
        }
        code = f"""
import html
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

commands = json.loads({json.dumps(json.dumps(commands, ensure_ascii=False), ensure_ascii=False)})
timeout = {timeout}
web_search_base_url = {json.dumps(str(web_search_base_url or ""))}
web_search_api_key = {json.dumps(str(web_search_api_key or ""))}
web_search_model = {json.dumps(str(web_search_model or ""))}
ua = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 PikaQiu-Agent/1.0"
cache_path = os.path.join(os.getcwd(), ".pikaqiu_web_search_cache.json")
length = str(commands.get("response_length") or "medium").lower()
max_chars_by_length = {{"short": 5000, "medium": 12000, "long": 24000}}
max_chars = max_chars_by_length.get(length, 12000)
search_limit_by_length = {{"short": 5, "medium": 8, "long": 12}}
search_limit = search_limit_by_length.get(length, 8)


def load_cache():
    try:
        with open(cache_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            data.setdefault("turn", 0)
            data.setdefault("refs", {{}})
            return data
    except Exception:
        pass
    return {{"turn": 0, "refs": {{}}}}


def save_cache(cache):
    try:
        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def headers_for_url(url):
    return {{"User-Agent": ua, "Accept-Language": "en-US,en;q=0.8"}}


def clean_url(url):
    return html.unescape(str(url or "")).strip()


def extract_links(page_url, text):
    links = []
    seen = set()
    for href, label in re.findall(r'(?is)<a\\b[^>]*href=["\\']([^"\\']+)["\\'][^>]*>(.*?)</a>', text):
        url = clean_url(urllib.parse.urljoin(page_url, href))
        if not re.match(r"^https?://", url, re.I) or url in seen:
            continue
        label = html.unescape(re.sub(r"(?s)<[^>]+>", " ", label))
        label = re.sub(r"\\s+", " ", label).strip()
        if not label:
            label = url
        seen.add(url)
        links.append({{"id": len(links), "text": label[:160], "url": url}})
        if len(links) >= 80:
            break
    return links


def readable_text(content_type, text):
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
    return title, text


def fetch_url(url):
    if not re.match(r"^https?://", str(url or ""), re.I):
        raise ValueError("only http/https URLs are supported")
    req = urllib.request.Request(url, headers=headers_for_url(url))
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        status = getattr(resp, "status", 0)
        final_url = resp.geturl()
        content_type = resp.headers.get("content-type", "")
        charset = resp.headers.get_content_charset() or "utf-8"
        raw = resp.read(min(max_chars * 12, 2000000))
    text = raw.decode(charset, "replace")
    links = extract_links(final_url, text)
    title, clean = readable_text(content_type, text)
    if len(clean) > max_chars:
        clean = clean[:max_chars] + "\\n... [truncated]"
    return {{
        "url": url,
        "final_url": final_url,
        "status": status,
        "content_type": content_type,
        "title": title,
        "text": clean,
        "links": links,
    }}


def search_web(query):
    q = str(query.get("q") or "").strip()
    domains = [str(d).strip() for d in (query.get("domains") or []) if str(d).strip()]
    recency = query.get("recency")
    if not q:
        return []
    search_q = q
    if domains:
        search_q = q + " " + " ".join("site:" + d for d in domains)
    if recency:
        search_q += " recent within " + str(recency) + " days"
    if not web_search_base_url or not web_search_api_key or not web_search_model:
        raise RuntimeError("hosted web_search requires web_search_base_url, web_search_api_key, and web_search_model")
    base = web_search_base_url.rstrip("/")
    endpoint = base + "/responses" if base.endswith("/v1") else base + "/v1/responses"
    prompt = (
        "Use web search for this query and return strict JSON only. "
        "Do not include markdown. Schema: "
        "{{\\"results\\":[{{\\"title\\":\\"...\\",\\"url\\":\\"https://...\\",\\"snippet\\":\\"...\\"}}]}}. "
        "Return up to " + str(search_limit) + " results. Query: " + search_q
    )
    payload = {{
        "model": web_search_model,
        "input": prompt,
        "tools": [{{"type": "web_search"}}],
        "tool_choice": {{"type": "web_search"}},
        "store": False,
        "max_output_tokens": 1200 if length == "short" else 2000 if length == "medium" else 3500,
    }}
    req = urllib.request.Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers={{"Authorization": "Bearer " + web_search_api_key, "Content-Type": "application/json"}},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read(2000000)
            response_text = raw.decode("utf-8", "replace")
    except urllib.error.HTTPError as exc:
        body = exc.read(4000).decode("utf-8", "replace")
        raise RuntimeError("hosted web_search HTTP " + str(exc.code) + ": " + body[:1200])
    data = json.loads(response_text)
    text_parts = []
    if isinstance(data.get("output_text"), str):
        text_parts.append(data["output_text"])
    for item in data.get("output") or []:
        if not isinstance(item, dict):
            continue
        for content in item.get("content") or []:
            if isinstance(content, dict) and isinstance(content.get("text"), str):
                text_parts.append(content["text"])
    answer_text = "\\n".join(part for part in text_parts if part).strip()
    if not answer_text:
        raise RuntimeError("hosted web_search returned no text output")
    json_text = answer_text
    fenced = re.search(r"(?s)```(?:json)?\\s*(.*?)\\s*```", json_text)
    if fenced:
        json_text = fenced.group(1)
    start = json_text.find("{{")
    end = json_text.rfind("}}")
    if start >= 0 and end >= start:
        json_text = json_text[start:end + 1]
    parsed = json.loads(json_text)
    results = []
    seen = set()
    for item in parsed.get("results") or []:
        if not isinstance(item, dict):
            continue
        result_url = clean_url(item.get("url"))
        if not re.match(r"^https?://", result_url, re.I) or result_url in seen:
            continue
        host = urllib.parse.urlparse(result_url).netloc.lower()
        if domains and not any(host == d.lower() or host.endswith("." + d.lower()) for d in domains):
            continue
        title = str(item.get("title") or result_url)
        title = re.sub(r"\\s+", " ", title).strip()
        snippet = re.sub(r"\\s+", " ", str(item.get("snippet") or "")).strip()
        seen.add(result_url)
        results.append({{"title": title or result_url, "url": result_url, "snippet": snippet}})
        if len(results) >= search_limit:
            break
    return results


def resolve_ref(cache, ref_id):
    if re.match(r"^https?://", str(ref_id or ""), re.I):
        return {{"url": ref_id}}
    return cache.get("refs", {{}}).get(str(ref_id or ""))


cache = load_cache()
cache["turn"] = int(cache.get("turn") or 0) + 1
turn = cache["turn"]
out = {{"search_results": [], "opened_pages": [], "findings": [], "errors": []}}

try:
    for query in (commands.get("search_query") or [])[:4] + (commands.get("image_query") or [])[:4]:
        try:
            results = search_web(query)
            formatted = []
            for idx, item in enumerate(results):
                ref = f"turn{{turn}}search{{len(out['search_results']) + idx}}"
                cache["refs"][ref] = {{"url": item["url"], "title": item["title"], "kind": "search_result"}}
                formatted.append({{"ref_id": ref, **item}})
            out["search_results"].append({{"query": query.get("q", ""), "results": formatted}})
        except Exception as exc:
            out["errors"].append({{"operation": "search_query", "query": query.get("q", ""), "error": str(exc)}})

    for op in commands.get("open") or []:
        ref_id = str(op.get("ref_id") or "")
        try:
            target = resolve_ref(cache, ref_id)
            if not target:
                raise ValueError("unknown ref_id")
            page = fetch_url(target["url"])
            fetch_ref = f"turn{{turn}}fetch{{len(out['opened_pages'])}}"
            cache["refs"][fetch_ref] = {{
                "url": page["final_url"],
                "title": page["title"],
                "kind": "opened_page",
                "text": page["text"],
                "links": page["links"],
            }}
            lineno = op.get("lineno")
            text = page["text"]
            if lineno:
                lines = text.splitlines()
                start = max(0, int(lineno) - 1)
                text = "\\n".join(lines[start:start + 120])
            out["opened_pages"].append({{
                "ref_id": fetch_ref,
                "source_ref_id": ref_id,
                "url": page["final_url"],
                "status": page["status"],
                "content_type": page["content_type"],
                "title": page["title"],
                "text": text,
                "links": page["links"][:30],
            }})
        except Exception as exc:
            out["errors"].append({{"operation": "open", "ref_id": ref_id, "error": str(exc)}})

    for op in commands.get("click") or []:
        ref_id = str(op.get("ref_id") or "")
        try:
            target = resolve_ref(cache, ref_id)
            if not target:
                raise ValueError("unknown ref_id")
            links = target.get("links") or []
            link_id = int(op.get("id"))
            link = next((item for item in links if int(item.get("id", -1)) == link_id), None)
            if not link:
                raise ValueError("unknown link id")
            page = fetch_url(link["url"])
            fetch_ref = f"turn{{turn}}fetch{{len(out['opened_pages'])}}"
            cache["refs"][fetch_ref] = {{
                "url": page["final_url"],
                "title": page["title"],
                "kind": "opened_page",
                "text": page["text"],
                "links": page["links"],
            }}
            out["opened_pages"].append({{
                "ref_id": fetch_ref,
                "source_ref_id": ref_id,
                "clicked_link_id": link_id,
                "url": page["final_url"],
                "status": page["status"],
                "content_type": page["content_type"],
                "title": page["title"],
                "text": page["text"],
                "links": page["links"][:30],
            }})
        except Exception as exc:
            out["errors"].append({{"operation": "click", "ref_id": ref_id, "id": op.get("id"), "error": str(exc)}})

    for op in commands.get("find") or []:
        ref_id = str(op.get("ref_id") or "")
        pattern = str(op.get("pattern") or "")
        try:
            target = resolve_ref(cache, ref_id)
            if not target:
                raise ValueError("unknown ref_id")
            text = target.get("text")
            url = target.get("url")
            if text is None:
                page = fetch_url(url)
                text = page["text"]
            matches = []
            for m in re.finditer(re.escape(pattern), text, re.I):
                start = max(0, m.start() - 180)
                end = min(len(text), m.end() + 180)
                matches.append(text[start:end].replace("\\n", " "))
                if len(matches) >= 10:
                    break
            out["findings"].append({{"ref_id": ref_id, "url": url, "pattern": pattern, "matches": matches}})
        except Exception as exc:
            out["errors"].append({{"operation": "find", "ref_id": ref_id, "pattern": pattern, "error": str(exc)}})
finally:
    save_cache(cache)

print(json.dumps(out, ensure_ascii=False, indent=2))
"""
        started = time.monotonic()
        result = sandbox.run_python(code, timeout_sec=timeout, workdir=workdir, stop_fn=stop_fn, on_chunk=on_chunk)
        return _format_sandbox_result(
            result,
            wall_time=time.monotonic() - started,
            max_output_tokens=max_output_tokens,
            max_output_tokens_cap=max_output_tokens_cap,
        )
    return web_search


def create_knowledge_tool(knowledge, top_k: int = 3) -> BaseTool:
    @tool("knowledge_search", args_schema=KnowledgeSearchInput)
    def knowledge_search(query: str, limit: int = top_k) -> str:
        """Search the offline cybersecurity knowledge base.
        Contains payload references, technique notes, and pentest cheatsheets.
        Use for payloads, vulnerability background, and exploitation techniques.
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


def create_skill_search_tool(skills) -> BaseTool:
    @tool("skill_search", args_schema=SkillSearchInput)
    def skill_search(query: str, limit: int = 5) -> str:
        """Search available SKILL.md skills by current situation or technique.

        Use when task context, early observations, memory, source hints, target
        behavior, or tool output suggests a reusable specialist workflow may help.
        This returns metadata only; call activate_skill only for a good match that
        is likely to improve the next few actions.
        """
        try:
            limit = max(1, min(int(limit or 5), 20))
            stats = skills.refresh()
            results = skills.search(query, limit=limit)
            return json.dumps({
                "query": query,
                "stats": stats,
                "results": results,
                "next_step": (
                    "Call activate_skill(skill_id, reason) when one result is a good fit for the current phase. "
                    "The reason should cite the basis for that fit; otherwise continue with normal tools."
                ),
            }, ensure_ascii=False, indent=2)
        except Exception as exc:
            logger.exception("[skill_search] failed")
            return json.dumps({"query": query, "error": str(exc), "results": []}, ensure_ascii=False, indent=2)
    return skill_search


def create_activate_skill_tool(
    skills,
    store=None,
    mission: dict[str, Any] | None = None,
    prompt_max_chars: int = 12000,
) -> BaseTool:
    @tool("activate_skill", args_schema=ActivateSkillInput)
    def activate_skill(skill_id: str, reason: str = "") -> str:
        """Activate a skill and return its SKILL.md instructions.

        Use when a returned skill is a good fit for the current situation and the
        next phase would benefit from that workflow. Do not activate skills from
        generic guesses, target labels alone, or startup assumptions.
        """
        try:
            skills.refresh()
            skill = skills.get_skill(skill_id)
            if not skill:
                return json.dumps({
                    "ok": False,
                    "error": f"unknown or disabled skill: {skill_id}",
                    "hint": "Call skill_search with the specific basis for the current situation to find a valid skill id.",
                }, ensure_ascii=False, indent=2)

            activated_skills: list[str] = []
            mission_id = str((mission or {}).get("id") or "").strip()
            current_mission = mission or {}
            if store and mission_id:
                current_mission = store.get_mission(mission_id) or current_mission
                activated_skills = store.add_activated_skill(mission_id, skill.id)
            active_ids = [
                str(item).strip()
                for item in (
                    list(current_mission.get("skills", []))
                    + list(current_mission.get("activated_skills", []))
                )
                if str(item).strip()
            ]

            prompt = _truncate_end(skill.prompt, max(1000, int(prompt_max_chars or 12000)))
            return json.dumps({
                "ok": True,
                "activated": skill.id,
                "reason": reason,
                "already_active": skill.id in active_ids,
                "activated_skills": activated_skills,
                "skill": skill.to_dict(include_prompt=False, include_references=True),
                "prompt": prompt,
                "next_step": (
                    "Follow this SKILL.md guidance for the current situation cited in reason. "
                    "Use skill_read_reference for listed reference files only when needed."
                ),
            }, ensure_ascii=False, indent=2)
        except Exception as exc:
            logger.exception("[activate_skill] failed")
            return json.dumps({"ok": False, "skill_id": skill_id, "error": str(exc)}, ensure_ascii=False, indent=2)
    return activate_skill


def create_skill_reference_tool(
    skills,
    *,
    store=None,
    mission: dict[str, Any] | None = None,
    default_max_chars: int = 20000,
) -> BaseTool:
    @tool("skill_read_reference", args_schema=SkillReferenceInput)
    def skill_read_reference(skill_id: str, path: str, max_chars: int = 20000) -> str:
        """Read an optional reference file bundled inside an activated skill.

        Use when a SKILL.md mentions dictionaries, templates, scripts, payload
        notes, or detailed references that are needed for the current step.
        """
        try:
            configured_max = max(1000, int(default_max_chars or 20000))
            max_chars = max(1000, min(int(max_chars or configured_max), configured_max))
            current_mission = mission or {}
            mission_id = str(current_mission.get("id") or "").strip()
            if store and mission_id:
                current_mission = store.get_mission(mission_id) or current_mission
            active_ids = {
                str(item).strip()
                for item in (
                    list(current_mission.get("skills", []))
                    + list(current_mission.get("activated_skills", []))
                )
                if str(item).strip()
            }
            if str(skill_id).strip() not in active_ids:
                return json.dumps({
                    "ok": False,
                    "skill_id": skill_id,
                    "path": path,
                    "error": "skill reference can only be read after the skill is selected or activated for this mission",
                    "hint": "Call skill_search with the current evidence, then activate_skill with a valid returned skill id before reading references.",
                }, ensure_ascii=False, indent=2)
            return skills.read_reference(skill_id, path, max_chars=max_chars)
        except Exception as exc:
            logger.exception("[skill_read_reference] failed")
            return f"[skill_read_reference error] {exc}"
    return skill_read_reference



def create_submit_flag_tool(on_flag: Callable[[str], str]) -> BaseTool:
        @tool("submit_flag", args_schema=SubmitFlagInput)
        def submit_flag(flag: str) -> str:
                """Submit the captured flag string found by exploiting the target.

                CRITICAL RULES:
                - Only call this with a flag string you ACTUALLY FOUND in the target's response,
                    file system, database output, or cookie value — obtained through exploitation.
                - Accepted prefixes are exactly flag{...}, FLAG{...}, ctf{...}, or CTF{...}.
                - NEVER fabricate, invent, or guess a flag to test this tool.
                - NEVER submit flag{test_...}, flag{example}, or any string you made up.
                - This is NOT a way to probe whether flags are accepted. Only call it when
                    you have a real flag from the target.

                If you found a string matching the flag format in the target response, submit it here.
                """
                candidate = flag.strip()
                if not is_valid_flag(candidate):
                        return (
                                "[FLAG_REJECTED] Invalid flag format. Only flag{...}, FLAG{...}, "
                                "ctf{...}, and CTF{...} are accepted; other prefixes are fake flags."
                        )
                return on_flag(candidate)

        return submit_flag


def create_all_tools(
    sandbox,
    workdir: str,
    store=None,
    knowledge=None,
    skills=None,
    mission: dict | None = None,
    on_flag: Callable[[str], str] | None = None,
    stop_fn: Callable[[], bool] | None = None,
    on_chunk: Callable[[str], None] | None = None,
    knowledge_top_k: int = 3,
    command_timeout_sec: int = 300,
    max_output_tokens_cap: int | None = DEFAULT_MAX_OUTPUT_TOKENS,
    skill_prompt_max_chars: int = 12000,
    skill_reference_max_chars: int = 20000,
    web_search_base_url: str = "",
    web_search_api_key: str = "",
    web_search_model: str = "",
) -> list[BaseTool]:
    """Create all tools for a mission round."""
    tools: list[BaseTool] = [
        create_bash_tool(
            sandbox,
            workdir,
            stop_fn=stop_fn,
            on_chunk=on_chunk,
            max_timeout=command_timeout_sec,
            max_output_tokens_cap=max_output_tokens_cap,
        ),
        create_python_tool(
            sandbox,
            workdir,
            stop_fn=stop_fn,
            on_chunk=on_chunk,
            max_timeout=command_timeout_sec,
            max_output_tokens_cap=max_output_tokens_cap,
        ),
        create_web_search_tool(
            sandbox,
            workdir,
            stop_fn=stop_fn,
            on_chunk=on_chunk,
            max_timeout=command_timeout_sec,
            max_output_tokens_cap=max_output_tokens_cap,
            web_search_base_url=web_search_base_url,
            web_search_api_key=web_search_api_key,
            web_search_model=web_search_model,
        ),
    ]
    if knowledge:
        tools.append(create_knowledge_tool(knowledge, top_k=knowledge_top_k))
    if skills:
        tools.extend([
            create_skill_search_tool(skills),
            create_activate_skill_tool(
                skills,
                store=store,
                mission=mission,
                prompt_max_chars=skill_prompt_max_chars,
            ),
            create_skill_reference_tool(
                skills,
                store=store,
                mission=mission,
                default_max_chars=skill_reference_max_chars,
            ),
        ])
    if on_flag:
        tools.append(create_submit_flag_tool(on_flag))
    return tools
