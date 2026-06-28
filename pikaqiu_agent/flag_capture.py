from __future__ import annotations

import html
import re
from typing import Callable

from pikaqiu_agent.output_truncation import formatted_truncate_text


VALID_FLAG_PREFIXES = ("flag", "FLAG", "ctf", "CTF")
FLAG_RE = re.compile(r"\b(?:flag|FLAG|ctf|CTF)\{[^}\s]{4,200}\}")
TRUSTED_FLAG_CAPTURE_TOOLS = {"bash_exec", "python_exec"}
PLACEHOLDER_FLAG_BODIES = {
    "example",
    "sample",
    "yourflag",
    "your_flag",
    "replace_me",
    "changeme",
    "dummy",
    "placeholder",
}


def truncate_middle(text: str, limit: int) -> str:
    return formatted_truncate_text(text, max_tokens=limit)


def is_placeholder_flag(flag: str) -> bool:
    body = flag.partition("{")[2].rpartition("}")[0].strip().lower()
    compact = re.sub(r"[^a-z0-9]+", "", body)
    if body in PLACEHOLDER_FLAG_BODIES or compact in PLACEHOLDER_FLAG_BODIES:
        return True
    if body == "test" or re.match(r"^test[_\-.].+", body):
        return True
    if "your" in compact and "flag" in compact:
        return True
    return False


def is_valid_flag(flag: str) -> bool:
    return bool(FLAG_RE.fullmatch(str(flag or "").strip()))


def extract_flag_candidates(text: str) -> list[str]:
    seen: set[str] = set()
    flags: list[str] = []
    for variant in _flag_text_variants(text):
        for match in FLAG_RE.finditer(variant):
            flag = match.group(0)
            key = flag.lower()
            if key in seen or is_placeholder_flag(flag):
                continue
            seen.add(key)
            flags.append(flag)
    return flags


def trusted_tool_flag_candidates(tool_name: str, result_str: str) -> list[str]:
    if tool_name not in TRUSTED_FLAG_CAPTURE_TOOLS:
        return []
    return extract_flag_candidates(result_str)


def flag_context(text: str, flag: str, radius: int = 120) -> str:
    source = str(text or "")
    for variant in _flag_text_variants(source):
        idx = variant.lower().find(flag.lower())
        if idx >= 0:
            start = max(0, idx - radius)
            end = min(len(variant), idx + len(flag) + radius)
            snippet = variant[start:end].replace("\r", "\\r").replace("\n", "\\n")
            if start > 0:
                snippet = "..." + snippet
            if end < len(variant):
                snippet += "..."
            return snippet
    return ""


def append_flag_candidate_summary(text: str, flags: list[str]) -> str:
    if not flags:
        return text
    summary = "[FLAG_CANDIDATES] " + ", ".join(flags[:10])
    if summary in text:
        return text
    return f"{text}\n\n{summary}"


def auto_capture_trusted_flags(
    *,
    tool_name: str,
    result_str: str,
    captured_flags: list[str],
    on_flag: Callable[[str], str],
    is_complete: Callable[[], bool],
) -> list[str]:
    return [message for _, message in auto_capture_trusted_flag_events(
        tool_name=tool_name,
        result_str=result_str,
        captured_flags=captured_flags,
        on_flag=on_flag,
        is_complete=is_complete,
    )]


def auto_capture_trusted_flag_events(
    *,
    tool_name: str,
    result_str: str,
    captured_flags: list[str],
    on_flag: Callable[[str], str],
    is_complete: Callable[[], bool],
) -> list[tuple[str, str]]:
    submitted: list[tuple[str, str]] = []
    for flag in trusted_tool_flag_candidates(tool_name, result_str):
        if any(flag.lower() == existing.lower() for existing in captured_flags):
            continue
        submitted.append((flag, str(on_flag(flag))))
        if is_complete():
            break
    return submitted


def _flag_text_variants(text: str) -> list[str]:
    raw = str(text or "")
    variants: list[str] = []
    seen: set[str] = set()

    def add(value: str) -> None:
        if value and value not in seen:
            seen.add(value)
            variants.append(value)

    add(raw)
    add(html.unescape(raw))
    try:
        decoded = bytes(raw, "utf-8").decode("unicode_escape")
    except UnicodeError:
        decoded = ""
    add(decoded)
    if decoded:
        add(html.unescape(decoded))
    return variants


# Backwards-compatible private aliases for focused unit tests and older imports.
_FLAG_RE = FLAG_RE
_TRUSTED_FLAG_CAPTURE_TOOLS = TRUSTED_FLAG_CAPTURE_TOOLS
_PLACEHOLDER_FLAG_BODIES = PLACEHOLDER_FLAG_BODIES
_truncate_middle = truncate_middle
_is_placeholder_flag = is_placeholder_flag
_extract_flag_candidates = extract_flag_candidates
_trusted_tool_flag_candidates = trusted_tool_flag_candidates
_append_flag_candidate_summary = append_flag_candidate_summary
_auto_capture_trusted_flags = auto_capture_trusted_flags
_auto_capture_trusted_flag_events = auto_capture_trusted_flag_events
_flag_context = flag_context
