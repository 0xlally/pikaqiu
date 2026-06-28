from __future__ import annotations

from functools import lru_cache
from typing import Any

from pikaqiu_agent.output_truncation import approx_token_count

try:
    import tiktoken
except Exception:  # pragma: no cover - depends on optional runtime dependency
    tiktoken = None  # type: ignore[assignment]


DEFAULT_ENCODING = "o200k_base"
TOKEN_COUNT_SAFETY_MARGIN = 1.08
MESSAGE_OVERHEAD_TOKENS = 4


def _normalize_model_name(model: str | None) -> str:
    return str(model or "").strip().lower()


def _explicit_encoding_for_model(model: str | None) -> str:
    model_name = _normalize_model_name(model)
    if model_name in {"gpt-5.5", "gpt-5-5"}:
        return DEFAULT_ENCODING
    if model_name.startswith(("gpt-5", "gpt-4.1", "gpt-4o", "o1", "o3", "o4")):
        return DEFAULT_ENCODING
    return DEFAULT_ENCODING


@lru_cache(maxsize=64)
def _encoding_for_model(model: str | None):
    if tiktoken is None:
        return None

    model_name = _normalize_model_name(model)
    if model_name:
        try:
            return tiktoken.encoding_for_model(model_name)
        except Exception:
            pass

    try:
        return tiktoken.get_encoding(_explicit_encoding_for_model(model_name))
    except Exception:
        return None


def count_text_tokens(text: Any, *, model: str | None = None, safety_margin: float = 1.0) -> int:
    value = str(text or "")
    encoding = _encoding_for_model(model)
    if encoding is None:
        count = approx_token_count(value)
    else:
        count = len(encoding.encode(value))

    margin = max(1.0, float(safety_margin or 1.0))
    if margin == 1.0:
        return count
    return int(count * margin + 0.999999)


def count_message_tokens(
    message: Any,
    *,
    model: str | None = None,
    safety_margin: float = TOKEN_COUNT_SAFETY_MARGIN,
) -> int:
    content = message.content if hasattr(message, "content") else str(message)
    total = MESSAGE_OVERHEAD_TOKENS

    if isinstance(content, str):
        total += count_text_tokens(content, model=model)
    elif isinstance(content, list):
        for part in content:
            if isinstance(part, dict):
                total += count_text_tokens(part.get("text", ""), model=model)
            else:
                total += count_text_tokens(part, model=model)
    else:
        total += count_text_tokens(content, model=model)

    tool_calls = getattr(message, "tool_calls", None)
    if tool_calls:
        total += count_text_tokens(tool_calls, model=model)

    additional_kwargs = getattr(message, "additional_kwargs", None) or {}
    if additional_kwargs:
        total += count_text_tokens(additional_kwargs, model=model)

    response_metadata = getattr(message, "response_metadata", None) or {}
    if response_metadata:
        total += count_text_tokens(response_metadata, model=model)

    margin = max(1.0, float(safety_margin or 1.0))
    if margin == 1.0:
        return total
    return int(total * margin + 0.999999)


def count_messages_tokens(
    messages: list[Any],
    *,
    model: str | None = None,
    safety_margin: float = TOKEN_COUNT_SAFETY_MARGIN,
) -> int:
    return sum(count_message_tokens(message, model=model, safety_margin=safety_margin) for message in messages)
