from __future__ import annotations

import re
from typing import Any

_MISSING_TOOL_RE = re.compile(
    r"(?:`?([A-Za-z0-9_.+-]+)`?\s+is unavailable|"
    r"`?([A-Za-z0-9_.+-]+)`?\s+not found|"
    r"`?([A-Za-z0-9_.+-]+)`?:\s+command not found)",
    re.I,
)
_CHAIN_DETAIL_TERMS = (
    "入口",
    "认证",
    "权限",
    "文件读",
    "payload",
    "执行",
    "回显",
    "flag",
    "路径",
    "状态码",
    "响应",
    "stdout",
    "stderr",
    "webroot",
    "源码",
)
_VAGUE_DEAD_END_RE = re.compile(
    r"^(?:未打通|失败|没结果|无结果|没有结果|不通|失败了|没通|blocked|failed|"
    r"timeout|timed out|no result|empty result|not working|did not work)$",
    re.I,
)


def _has_chain_detail(text: str) -> bool:
    lowered = text.lower()
    hits = sum(1 for term in _CHAIN_DETAIL_TERMS if term.lower() in lowered)
    return hits >= 2 or (len(text) >= 80 and hits >= 1)


def normalize_dead_end(value: Any) -> str:
    """Keep dead-end memory specific without forcing sub-fields."""
    text = re.sub(r"\s+", " ", str(value or "")).strip()
    if not text:
        return ""

    missing_tool = _MISSING_TOOL_RE.search(text)
    if missing_tool:
        tool = next(group for group in missing_tool.groups() if group)
        return (
            f"工具可用性卡点：已尝试调用 `{tool}`，原始结果显示 `{tool}` is unavailable in the sandbox；"
            "当前沙箱缺少该工具，不要重复调用。后续应改用 curl/原始响应/小脚本解析，或先确认替代工具可用。"
        )[:900]

    if _has_chain_detail(text) and not _VAGUE_DEAD_END_RE.search(text):
        return text[:900]

    return (
        f"失败路线卡点待补全：{text[:320]}。复盘时需补充链条卡在哪一步，例如入口是否确认、认证/权限是否绕过、"
        "文件读取到哪一级、payload 是否执行、是否有回显、flag 路径是否定位，以及缺少哪条决定性原始证据。"
    )[:900]


def normalize_dead_ends(values: list[Any]) -> list[str]:
    normalized: list[str] = []
    seen: set[str] = set()
    for value in values:
        item = normalize_dead_end(value)
        key = item.lower()
        if not item or key in seen:
            continue
        normalized.append(item)
        seen.add(key)
    return normalized
