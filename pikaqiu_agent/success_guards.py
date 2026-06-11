from __future__ import annotations

import json
import re
from typing import Any

from pikaqiu_agent import flag_capture


SCAN_TOOL_RE = re.compile(
    r"\b(ffuf|arjun|nuclei|gobuster|dirsearch|feroxbuster|wfuzz|hydra|sqlmap|nikto)\b",
    re.I,
)
BROAD_SCAN_RE = re.compile(
    r"\b(ffuf|arjun|nuclei|gobuster|dirsearch|feroxbuster|wfuzz|sqlmap|nikto)\b|"
    r"\b(directory-list|raft-|common\.txt|seclists|wordlist|FUZZ)\b",
    re.I,
)
ADVICE_RESULT_TOOLS = {"ask_adviser", "knowledge_search"}


def is_scan_like_tool_call(tool_name: str, display_cmd: str) -> bool:
    if tool_name not in {"bash_exec", "python_exec"}:
        return False
    return bool(SCAN_TOOL_RE.search(str(display_cmd or "")))


def is_broad_scan_tool_call(tool_name: str, display_cmd: str) -> bool:
    if tool_name not in {"bash_exec", "python_exec"}:
        return False
    return bool(BROAD_SCAN_RE.search(str(display_cmd or "")))


def last_memory_item(memory: dict[str, Any], *keys: str) -> str:
    for key in keys:
        value = memory.get(key)
        if isinstance(value, list):
            items = [str(item).strip() for item in value if str(item).strip()]
            if items:
                return items[-1]
        elif isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def highest_value_lead(memory: dict[str, Any]) -> str:
    return last_memory_item(memory, "highest_value_lead", "next_focus", "leads", "findings")


def summarize_advice_result(tool_name: str, result_str: str, limit: int) -> str:
    if tool_name not in ADVICE_RESULT_TOOLS:
        return flag_capture.truncate_middle(result_str, limit)
    text = str(result_str or "")
    if len(text) <= limit:
        return text
    head = max(800, int(limit * 0.55))
    tail = max(600, limit - head - 140)
    return (
        text[:head]
        + f"\n\n... [advice output truncated; omitted {len(text) - head - tail} chars. "
          "Use this as guidance only, not target evidence.] ...\n\n"
        + text[-tail:]
    )


def round_time_guidance(remaining_round_time: float) -> str | None:
    remaining = int(max(0, remaining_round_time))
    if remaining < 45:
        return (
            "[ROUND_TIME_CRITICAL]\n"
            f"Only {remaining}s remains in this round. Do not start broad scans, fuzzers, or long research calls. "
            "Close the current lead now: auto/submit any real flag already observed, preserve decisive raw evidence, "
            "or run one minimal verification command that can finish quickly.\n"
            "[/ROUND_TIME_CRITICAL]"
        )
    if remaining < 90:
        return (
            "[ROUND_TIME_LIMITED]\n"
            f"{remaining}s remains in this round. Use only a small targeted verification tied to current memory. "
            "Avoid ffuf/arjun/nuclei/sqlmap and broad wordlists unless the exact candidate is already known.\n"
            "[/ROUND_TIME_LIMITED]"
        )
    return None


def route_guard_guidance(memory: dict[str, Any]) -> str:
    text = json.dumps(memory or {}, ensure_ascii=False).lower()
    rules: list[str] = []
    if any(
        token in text
        for token in (
            "authenticated",
            "login successful",
            "logged in",
            "session",
            "cookie",
            "jwt",
            "认证",
            "登录成功",
        )
    ):
        rules.append(
            "Auth state is already evidenced. Do not repeat the login flow unless a fresh session is required; "
            "use paired authenticated/unauthenticated or role/field differential checks."
        )
    if any(
        token in text
        for token in (
            "static",
            "styles.css",
            "scripts.js",
            "no new content",
            "no difference",
            "未发现新内容",
            "静态",
        )
    ):
        rules.append(
            "Static-path probing has low value after repeated no-difference results. Stop expanding generic static fuzzing; "
            "test only high-value filenames tied to observed references."
        )
    if "apache" in text and any(token in text for token in ("cgi-bin", "%2e%2e", ".%2e", "500")):
        rules.append(
            "Apache/cgi evidence exists. Prefer one direct-vs-alias or PATH_INFO differential with full raw response over another broad scan."
        )
    if "django" in text and any(token in text for token in ("register", "step3", "template", "alert", "premium")):
        rules.append(
            "Django registration evidence exists. Prioritize one end-to-end registration/premium/XSS/SSTI verification chain and preserve the decisive response."
        )
    if "fastapi" in text or "openapi" in text or "uvicorn" in text:
        rules.append(
            "FastAPI/OpenAPI evidence exists. Use the documented routes to build minimal auth/body differentials; avoid generic path fuzzing first."
        )
    lead = highest_value_lead(memory)
    if lead:
        rules.append(f"Highest-value lead to close next: {lead}")
    if not rules:
        return ""
    return "[ROUTE_GUARD]\n" + "\n".join(f"- {rule}" for rule in rules[:6]) + "\n[/ROUTE_GUARD]"


def post_partial_flag_guidance(captured_flags: list[str], expected_flags: int) -> str:
    remaining = max(0, int(expected_flags or 1) - len(captured_flags))
    flags = ", ".join(captured_flags[-5:])
    return (
        "[PARTIAL_FLAG_CAPTURE]\n"
        f"Captured {len(captured_flags)}/{expected_flags} flag(s): {flags}. "
        f"{remaining} flag(s) remain. Do not run broad scans now; continue from the exact exploit path or "
        "validated privilege boundary that produced this flag, and look for the next flag with one focused verification.\n"
        "[/PARTIAL_FLAG_CAPTURE]"
    )


_is_scan_like_tool_call = is_scan_like_tool_call
_is_broad_scan_tool_call = is_broad_scan_tool_call
_highest_value_lead = highest_value_lead
_summarize_advice_result = summarize_advice_result
_round_time_guidance = round_time_guidance
_route_guard_guidance = route_guard_guidance
_post_partial_flag_guidance = post_partial_flag_guidance
