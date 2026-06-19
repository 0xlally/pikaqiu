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
WORDLIST_SCAN_RE = re.compile(
    r"(\s|^)(-w|--wordlist)(\s|=)|\b(directory-list|raft-|common\.txt|seclists|wordlist|FUZZ)\b",
    re.I,
)
COOLDOWN_SCAN_TOOL_RE = re.compile(r"\b(ffuf|arjun|nuclei|sqlmap)\b", re.I)
TARGETED_PROBE_RE = re.compile(
    r"\b(curl|httpx|python|python3|requests|openssl|nc|ncat)\b|"
    r"https?://[^\s'\"]+(/[^\s'\"]+|\?[^\s'\"]+)",
    re.I,
)
EXPLICIT_TARGET_RE = re.compile(
    r"https?://[^\s'\"/?]+(?::\d+)?(?:/[^\s'\"]*)?\?[^\s'\"]+|"
    r"https?://[^\s'\"/?]+(?::\d+)?/[^\s'\"\?]+|"
    r"(\s|^)(--data|-d|--cookie|-H|--header|-p|--param|--path)(\s|=)",
    re.I,
)
MEMORY_MISSING_TOOL_RE = re.compile(r"`?([A-Za-z0-9_.+-]+)`?\s+is unavailable\b", re.I)
MISSING_TOOL_RE = re.compile(r"(?:^|\n)(?:bash:\s+line\s+\d+:\s+)?([A-Za-z0-9_.+-]+):\s+command not found\b")
GUIDANCE_RESULT_TOOLS = {"knowledge_search"}


def is_scan_like_tool_call(tool_name: str, display_cmd: str) -> bool:
    if tool_name not in {"bash_exec", "python_exec"}:
        return False
    return bool(SCAN_TOOL_RE.search(str(display_cmd or "")))


def is_broad_scan_tool_call(tool_name: str, display_cmd: str) -> bool:
    if tool_name not in {"bash_exec", "python_exec"}:
        return False
    return bool(BROAD_SCAN_RE.search(str(display_cmd or "")))


def is_wordlist_scan_tool_call(tool_name: str, display_cmd: str) -> bool:
    if tool_name not in {"bash_exec", "python_exec"}:
        return False
    return bool(WORDLIST_SCAN_RE.search(str(display_cmd or "")))


def is_targeted_probe_tool_call(tool_name: str, display_cmd: str) -> bool:
    if tool_name not in {"bash_exec", "python_exec"}:
        return False
    cmd = str(display_cmd or "")
    return bool(TARGETED_PROBE_RE.search(cmd)) and not bool(WORDLIST_SCAN_RE.search(cmd))


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


def next_verification_hint(memory: dict[str, Any]) -> str:
    return last_memory_item(memory, "next_one_command", "highest_value_lead", "next_focus", "leads", "findings")


def broad_scan_block_message(memory: dict[str, Any], *, reason: str = "round") -> str:
    lead = next_verification_hint(memory) or "the current strongest lead"
    return (
        "[BROAD_SCAN_BLOCKED]\n"
        f"Broad enumeration is blocked by the {reason} guard. "
        "Run one targeted verification tied to memory, or explicitly explain why this lead is wrong before trying another scan.\n"
        f"Next targeted lead: {lead}\n"
        "[EXIT_CODE: 0]"
    )


def mission_scan_cooldown_blocks(tool_name: str, display_cmd: str, scan_timeout_count: int) -> bool:
    if scan_timeout_count < 2:
        return False
    if tool_name not in {"bash_exec", "python_exec"}:
        return False
    cmd = str(display_cmd or "")
    if not COOLDOWN_SCAN_TOOL_RE.search(cmd):
        return False
    if WORDLIST_SCAN_RE.search(cmd):
        return True
    return not bool(EXPLICIT_TARGET_RE.search(cmd))


def missing_tool_name(result_str: str) -> str:
    match = MISSING_TOOL_RE.search(str(result_str or ""))
    return match.group(1) if match else ""


def known_missing_tool_blocks(display_cmd: str, missing_tools: set[str]) -> str:
    cmd = str(display_cmd or "").lower()
    for tool in sorted(missing_tools):
        if re.search(rf"(^|[\s;|&]){re.escape(tool.lower())}($|[\s;|&-])", cmd):
            return tool
    return ""


def missing_tools_from_memory(memory: dict[str, Any]) -> set[str]:
    tools: set[str] = set()
    for item in memory.get("dead_ends", []) or []:
        match = MEMORY_MISSING_TOOL_RE.search(str(item or ""))
        if match:
            tools.add(match.group(1).lower())
    return tools


def missing_tool_block_message(tool: str) -> str:
    return (
        "[MISSING_TOOL_BLOCKED]\n"
        f"`{tool}` was already observed as unavailable in this sandbox. "
        "Use curl with raw headers/body, page HTML, and small local parsing instead of retrying the missing tool.\n"
        "[EXIT_CODE: 0]"
    )


def low_evidence_stop_block_message(memory: dict[str, Any]) -> str:
    lead = next_verification_hint(memory) or "the current strongest lead"
    return (
        "[LOW_EVIDENCE_STOP_BLOCKED]\n"
        "Stopping is blocked because the latest evidence is too weak to conclude the mission. "
        "Run one targeted verification tied to memory, preserve the decisive raw output, or call give_up again "
        "with a concrete failure boundary, blocked prerequisite, and required next evidence.\n"
        f"Next targeted lead: {lead}\n"
        "[EXIT_CODE: 0]"
    )


def stale_observer_steer_block_message(memory: dict[str, Any]) -> str:
    lead = next_verification_hint(memory) or "the current strongest lead"
    return (
        "[STALE_OBSERVER_STEER_BLOCKED]\n"
        "The pending Observer steer has not been resolved. Execute one command that directly verifies or falsifies it "
        "before changing direction or stopping.\n"
        f"Next targeted lead: {lead}\n"
        "[EXIT_CODE: 0]"
    )


def summarize_guidance_result(tool_name: str, result_str: str, limit: int) -> str:
    if tool_name not in GUIDANCE_RESULT_TOOLS:
        return flag_capture.truncate_middle(result_str, limit)
    text = str(result_str or "")
    if len(text) <= limit:
        return text
    head = max(800, int(limit * 0.55))
    tail = max(600, limit - head - 140)
    return (
        text[:head]
        + f"\n\n... [guidance output truncated; omitted {len(text) - head - tail} chars. "
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
_is_wordlist_scan_tool_call = is_wordlist_scan_tool_call
_is_targeted_probe_tool_call = is_targeted_probe_tool_call
_highest_value_lead = highest_value_lead
_next_verification_hint = next_verification_hint
_broad_scan_block_message = broad_scan_block_message
_mission_scan_cooldown_blocks = mission_scan_cooldown_blocks
_missing_tool_name = missing_tool_name
_known_missing_tool_blocks = known_missing_tool_blocks
_missing_tools_from_memory = missing_tools_from_memory
_missing_tool_block_message = missing_tool_block_message
_low_evidence_stop_block_message = low_evidence_stop_block_message
_stale_observer_steer_block_message = stale_observer_steer_block_message
_summarize_guidance_result = summarize_guidance_result
_round_time_guidance = round_time_guidance
_route_guard_guidance = route_guard_guidance
_post_partial_flag_guidance = post_partial_flag_guidance
