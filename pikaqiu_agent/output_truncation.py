from __future__ import annotations

from collections import deque
from typing import Deque

APPROX_BYTES_PER_TOKEN = 4
DEFAULT_MAX_OUTPUT_TOKENS = 10_000
UNIFIED_EXEC_OUTPUT_MAX_BYTES = 1024 * 1024
UNIFIED_EXEC_OUTPUT_MAX_TOKENS = UNIFIED_EXEC_OUTPUT_MAX_BYTES // APPROX_BYTES_PER_TOKEN


def _byte_len(text: str) -> int:
    return len(text.encode("utf-8"))


def approx_token_count(text: str) -> int:
    byte_count = _byte_len(str(text or ""))
    return (byte_count + APPROX_BYTES_PER_TOKEN - 1) // APPROX_BYTES_PER_TOKEN


def approx_bytes_for_tokens(tokens: int) -> int:
    return max(0, int(tokens or 0)) * APPROX_BYTES_PER_TOKEN


def approx_tokens_from_byte_count(byte_count: int) -> int:
    byte_count = max(0, int(byte_count or 0))
    return (byte_count + APPROX_BYTES_PER_TOKEN - 1) // APPROX_BYTES_PER_TOKEN


def resolve_max_tokens(max_tokens: int | None) -> int:
    if max_tokens is None:
        return DEFAULT_MAX_OUTPUT_TOKENS
    try:
        return max(0, int(max_tokens))
    except (TypeError, ValueError):
        return DEFAULT_MAX_OUTPUT_TOKENS


class HeadTailBuffer:
    """Capped byte buffer that preserves a stable prefix and suffix."""

    def __init__(self, max_bytes: int = UNIFIED_EXEC_OUTPUT_MAX_BYTES) -> None:
        self.max_bytes = max(0, int(max_bytes or 0))
        self.head_budget = self.max_bytes // 2
        self.tail_budget = self.max_bytes - self.head_budget
        self.head: Deque[bytes] = deque()
        self.tail: Deque[bytes] = deque()
        self.head_bytes = 0
        self.tail_bytes = 0
        self.omitted_bytes = 0

    def retained_bytes(self) -> int:
        return self.head_bytes + self.tail_bytes

    def push_chunk(self, chunk: bytes) -> None:
        chunk = bytes(chunk or b"")
        if not chunk:
            return
        if self.max_bytes == 0:
            self.omitted_bytes += len(chunk)
            return

        if self.head_bytes < self.head_budget:
            remaining_head = self.head_budget - self.head_bytes
            if len(chunk) <= remaining_head:
                self.head_bytes += len(chunk)
                self.head.append(chunk)
                return

            head_part = chunk[:remaining_head]
            tail_part = chunk[remaining_head:]
            if head_part:
                self.head_bytes += len(head_part)
                self.head.append(head_part)
            self._push_to_tail(tail_part)
            return

        self._push_to_tail(chunk)

    def snapshot_chunks(self) -> list[bytes]:
        return list(self.head) + list(self.tail)

    def to_bytes(self) -> bytes:
        return b"".join(self.snapshot_chunks())

    def to_text_lossy(self) -> str:
        return decode_utf8_lossy(self.to_bytes())

    def drain_chunks(self) -> list[bytes]:
        chunks = self.snapshot_chunks()
        self.head.clear()
        self.tail.clear()
        self.head_bytes = 0
        self.tail_bytes = 0
        self.omitted_bytes = 0
        return chunks

    def _push_to_tail(self, chunk: bytes) -> None:
        if not chunk:
            return
        if self.tail_budget == 0:
            self.omitted_bytes += len(chunk)
            return

        if len(chunk) >= self.tail_budget:
            start = len(chunk) - self.tail_budget
            kept = chunk[start:]
            dropped = len(chunk) - len(kept)
            self.omitted_bytes += self.tail_bytes + dropped
            self.tail.clear()
            self.tail_bytes = len(kept)
            self.tail.append(kept)
            return

        self.tail_bytes += len(chunk)
        self.tail.append(chunk)
        self._trim_tail_to_budget()

    def _trim_tail_to_budget(self) -> None:
        excess = max(0, self.tail_bytes - self.tail_budget)
        while excess > 0 and self.tail:
            front = self.tail[0]
            if excess >= len(front):
                excess -= len(front)
                self.tail_bytes -= len(front)
                self.omitted_bytes += len(front)
                self.tail.popleft()
                continue

            self.tail[0] = front[excess:]
            self.tail_bytes -= excess
            self.omitted_bytes += excess
            break


def decode_utf8_lossy(data: bytes) -> str:
    return bytes(data or b"").decode("utf-8", errors="replace")


def retain_head_tail_bytes(text: str, max_bytes: int = UNIFIED_EXEC_OUTPUT_MAX_BYTES) -> str:
    if _byte_len(text) <= max_bytes:
        return text
    buffer = HeadTailBuffer(max_bytes)
    buffer.push_chunk(text.encode("utf-8"))
    return buffer.to_text_lossy()


def formatted_truncate_text(content: str, max_tokens: int | None = None) -> str:
    max_tokens = resolve_max_tokens(max_tokens)
    policy_bytes = approx_bytes_for_tokens(max_tokens)
    if _byte_len(content) <= policy_bytes:
        return content

    original_token_count = approx_token_count(content)
    total_lines = len(content.splitlines())
    result = truncate_middle_with_token_budget(content, max_tokens)[0]
    return (
        f"Warning: truncated output (original token count: {original_token_count})\n"
        f"Total output lines: {total_lines}\n\n"
        f"{result}"
    )


def formatted_truncate_codex_exec_response(content: str, max_tokens: int | None = None) -> str:
    text = str(content or "")
    marker = "\nOutput:\n"
    if marker not in text:
        return formatted_truncate_text(text, max_tokens=max_tokens)
    header, output = text.split(marker, 1)
    return header + marker + formatted_truncate_text(output, max_tokens=max_tokens)


def truncate_middle_with_token_budget(text: str, max_tokens: int) -> tuple[str, int | None]:
    if not text:
        return "", None

    max_bytes = approx_bytes_for_tokens(max_tokens)
    if max_tokens > 0 and _byte_len(text) <= max_bytes:
        return text, None

    truncated = _truncate_with_byte_estimate(text, max_bytes, use_tokens=True)
    if truncated == text:
        return truncated, None
    return truncated, approx_token_count(text)


def truncate_middle_chars(text: str, max_bytes: int) -> str:
    return _truncate_with_byte_estimate(text, max_bytes, use_tokens=False)


def _truncate_with_byte_estimate(text: str, max_bytes: int, *, use_tokens: bool) -> str:
    if not text:
        return ""

    total_bytes = _byte_len(text)
    total_chars = len(text)
    if max_bytes == 0:
        return _format_truncation_marker(
            use_tokens,
            _removed_units(use_tokens, total_bytes, total_chars),
        )

    if total_bytes <= max_bytes:
        return text

    left_budget, right_budget = _split_budget(max_bytes)
    removed_chars, left, right = _split_string(text, left_budget, right_budget)
    marker = _format_truncation_marker(
        use_tokens,
        _removed_units(use_tokens, total_bytes - max_bytes, removed_chars),
    )
    return left + marker + right


def _split_budget(budget: int) -> tuple[int, int]:
    budget = max(0, int(budget or 0))
    left = budget // 2
    return left, budget - left


def _split_string(text: str, beginning_bytes: int, end_bytes: int) -> tuple[int, str, str]:
    if not text:
        return 0, "", ""

    encoded = text.encode("utf-8")
    total_bytes = len(encoded)
    tail_start_target = total_bytes - max(0, end_bytes)
    prefix_end = 0
    suffix_start = total_bytes
    suffix_started = False
    removed_chars = 0
    byte_idx = 0

    for ch in text:
        char_len = len(ch.encode("utf-8"))
        char_end = byte_idx + char_len
        if char_end <= beginning_bytes:
            prefix_end = char_end
            byte_idx = char_end
            continue

        if byte_idx >= tail_start_target:
            if not suffix_started:
                suffix_start = byte_idx
                suffix_started = True
            byte_idx = char_end
            continue

        removed_chars += 1
        byte_idx = char_end

    if suffix_start < prefix_end:
        suffix_start = prefix_end

    return (
        removed_chars,
        encoded[:prefix_end].decode("utf-8"),
        encoded[suffix_start:].decode("utf-8"),
    )


def _format_truncation_marker(use_tokens: bool, removed_count: int) -> str:
    if use_tokens:
        return f"…{removed_count} tokens truncated…"
    return f"…{removed_count} chars truncated…"


def _removed_units(use_tokens: bool, removed_bytes: int, removed_chars: int) -> int:
    if use_tokens:
        return approx_tokens_from_byte_count(removed_bytes)
    return max(0, int(removed_chars or 0))
