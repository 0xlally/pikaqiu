"""LangChain Tool definitions for the PikaQiu Agent sandbox and knowledge base."""
from __future__ import annotations

import json
import logging
from typing import Any, Callable

from langchain_core.tools import tool, BaseTool
from pydantic import BaseModel, Field

from pikaqiu_agent.flag_capture import is_valid_flag

logger = logging.getLogger(__name__)


def _clamp_timeout(timeout: int, max_timeout: int, min_timeout: int = 1) -> int:
    return max(min_timeout, min(int(timeout), max_timeout))


def _resolve_timeout(timeout: int | None, max_timeout: int, min_timeout: int = 1) -> int:
    if timeout is None:
        return max(min_timeout, int(max_timeout))
    return _clamp_timeout(timeout, max_timeout, min_timeout)


def _format_sandbox_result(prefix: str, result) -> str:
    parts = [prefix]
    if result.stdout:
        parts.append(result.stdout)
    if result.stderr:
        parts.append(f"[STDERR] {result.stderr}")
    if result.exit_code != 0 and "2>/dev/null" in str(result.command):
        parts.append(
            "[提示] 命令非零退出且 stderr 被 2>/dev/null 隐藏；请去掉重定向重跑一次，以保留真实工具错误。"
        )
    parts.append(f"[EXIT_CODE: {result.exit_code}]")
    return "\n".join(parts)


def _has_serialization_keywords(code: str) -> bool:
    keywords = ("pickle", "serialize", "marshal", "yaml.load", "ObjectInputStream", "unserialize")
    lowered = code.lower()
    return any(keyword.lower() in lowered for keyword in keywords)


def _truncate_end(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    return text[:limit] + f"\n... [truncated {len(text) - limit} chars]"


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


class PythonInput(BaseModel):
    code: str = Field(description="Python source code to execute")
    timeout: int | None = Field(
        default=None,
        description=(
            "Optional timeout in seconds. Omit to use the mission command timeout. "
            "Values above the mission command timeout are capped."
        ),
    )


class KnowledgeSearchInput(BaseModel):
    query: str = Field(description="Search query (keywords, CVE IDs, technique names)")
    limit: int = Field(default=6, description="Maximum number of results")


class WebFetchInput(BaseModel):
    url: str = Field(description="HTTP/HTTPS URL to fetch from the public internet")
    max_chars: int = Field(default=12000, description="Maximum extracted text characters to return, capped at 30000")
    timeout: int | None = Field(
        default=None,
        description=(
            "Optional timeout in seconds. Omit to use the mission command timeout. "
            "Values above the mission command timeout are capped."
        ),
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

def create_bash_tool(sandbox, workdir: str, stop_fn: Callable[[], bool] | None = None, on_chunk: Callable[[str], None] | None = None, max_timeout: int = 300) -> BaseTool:
    @tool("bash_exec", args_schema=BashInput)
    def bash_exec(command: str, timeout: int | None = None) -> str:
        """Execute a bash command in the Kali Linux sandbox.
        Use for recon and exploitation.
        Do not hide stderr with 2>/dev/null while validating a command; tool errors
        and missing wordlists must stay visible.
        """
        timeout = _resolve_timeout(timeout, max_timeout)
        result = sandbox.run(command, timeout_sec=timeout, workdir=workdir, stop_fn=stop_fn, on_chunk=on_chunk)
        return _format_sandbox_result("[输出为Kali沙箱中的本地执行结果，并非远程目标输出]", result)
    return bash_exec


def create_python_tool(sandbox, workdir: str, stop_fn: Callable[[], bool] | None = None, on_chunk: Callable[[str], None] | None = None, max_timeout: int = 300) -> BaseTool:
    @tool("python_exec", args_schema=PythonInput)
    def python_exec(code: str, timeout: int | None = None) -> str:
        """Execute Python code in the Kali sandbox.
        Preferred for HTTP sessions, cookies, JSON parsing, complex logic.

        CRITICAL: Each call is an ISOLATED process — variables/sessions from previous
        calls are GONE. Login + all operations MUST be in the same call.
        If you need to maintain a session (cookies etc.), you must login again in each call.
        Code is sent via base64 — no escaping needed.
        """
        timeout = _resolve_timeout(timeout, max_timeout)
        result = sandbox.run_python(code, timeout_sec=timeout, workdir=workdir, stop_fn=stop_fn, on_chunk=on_chunk)
        parts = [_format_sandbox_result("[以下是Kali沙箱中的Python执行结果]", result)]
        # Context reminder for serialization payloads
        if _has_serialization_keywords(code):
            parts.append("[提醒] 脚本中包含序列化/反序列化操作。构造payload的过程中，命令可能在本地沙箱执行，如果看到命令执行结果请注意区分"
                         "只有通过网络请求(requests/curl)发送到目标的结果才是远程响应，但确保你将他们区分开了。如果只有一个命令执行结果，大概率是构造payload时的本地执行结果。本提示为系统提示")
        return "\n".join(parts)
    return python_exec


def create_web_fetch_tool(
    sandbox,
    workdir: str,
    stop_fn: Callable[[], bool] | None = None,
    on_chunk: Callable[[str], None] | None = None,
    max_timeout: int = 300,
) -> BaseTool:
    @tool("web_fetch", args_schema=WebFetchInput)
    def web_fetch(url: str, max_chars: int = 12000, timeout: int | None = None) -> str:
        """Fetch an HTTP/HTTPS page from the public internet and extract readable text.

        Use only when you already have a specific URL. Prefer official docs,
        security bulletins, Exploit-DB, NVD, GitHub PoCs, and vendor pages.
        """
        max_chars = max(1000, min(int(max_chars or 12000), 30000))
        timeout = _resolve_timeout(timeout, max_timeout)
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
    skill_prompt_max_chars: int = 12000,
    skill_reference_max_chars: int = 20000,
) -> list[BaseTool]:
    """Create all tools for a mission round."""
    tools: list[BaseTool] = [
        create_bash_tool(sandbox, workdir, stop_fn=stop_fn, on_chunk=on_chunk, max_timeout=command_timeout_sec),
        create_python_tool(sandbox, workdir, stop_fn=stop_fn, on_chunk=on_chunk, max_timeout=command_timeout_sec),
        create_web_fetch_tool(sandbox, workdir, stop_fn=stop_fn, on_chunk=on_chunk, max_timeout=command_timeout_sec),
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
