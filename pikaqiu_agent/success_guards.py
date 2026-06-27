from __future__ import annotations

import json
from typing import Any

from pikaqiu_agent import flag_capture


GUIDANCE_RESULT_TOOLS = {"knowledge_search"}


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


def current_lead(memory: dict[str, Any]) -> str:
    return last_memory_item(memory, "leads", "findings")


def next_verification_hint(memory: dict[str, Any]) -> str:
    return last_memory_item(memory, "leads", "findings")


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
    if "django" in text and any(token in text for token in ("register", "step3", "template", "alert", "premium")):
        rules.append(
            "Django registration evidence exists. Prioritize one end-to-end registration/premium/XSS/SSTI verification chain and preserve the decisive response."
        )
    lead = current_lead(memory)
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
        f"{remaining} flag(s) remain. Continue from the exact exploit path or "
        "validated privilege boundary that produced this flag.\n"
        "[/PARTIAL_FLAG_CAPTURE]"
    )


_current_lead = current_lead
_next_verification_hint = next_verification_hint
_stale_observer_steer_block_message = stale_observer_steer_block_message
_summarize_guidance_result = summarize_guidance_result
_route_guard_guidance = route_guard_guidance
_post_partial_flag_guidance = post_partial_flag_guidance
