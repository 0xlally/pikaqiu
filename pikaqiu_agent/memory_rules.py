from __future__ import annotations

import re
from typing import Any

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
