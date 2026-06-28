from langchain_core.messages import HumanMessage

from pikaqiu_agent.output_truncation import approx_token_count
from pikaqiu_agent import token_counting
from pikaqiu_agent.token_counting import count_message_tokens, count_text_tokens


def test_gpt_5_5_uses_o200k_base_encoding():
    text = "中文 token counting with JSON {\"path\":\"/api/v1/users\"}"

    expected = len(token_counting.tiktoken.get_encoding("o200k_base").encode(text))

    assert count_text_tokens(text, model="gpt-5.5") == expected


def test_unknown_model_falls_back_to_o200k_base_when_tiktoken_is_available():
    text = "fallback model tokenizer"

    expected = len(token_counting.tiktoken.get_encoding("o200k_base").encode(text))

    assert count_text_tokens(text, model="private-model-name") == expected


def test_token_counting_falls_back_to_byte_estimate_without_tiktoken(monkeypatch):
    original_tiktoken = token_counting.tiktoken
    monkeypatch.setattr(token_counting, "tiktoken", None)
    token_counting._encoding_for_model.cache_clear()

    text = "fallback without tokenizer"

    try:
        assert count_text_tokens(text, model="gpt-5.5") == approx_token_count(text)
    finally:
        monkeypatch.setattr(token_counting, "tiktoken", original_tiktoken)
        token_counting._encoding_for_model.cache_clear()


def test_message_token_count_includes_message_overhead_and_margin():
    text = "short message"
    raw = count_text_tokens(text, model="gpt-5.5")

    counted = count_message_tokens(HumanMessage(content=text), model="gpt-5.5")

    assert counted > raw
