from pikaqiu_agent.output_truncation import (
    DEFAULT_MAX_OUTPUT_TOKENS,
    HeadTailBuffer,
    UNIFIED_EXEC_OUTPUT_MAX_BYTES,
    approx_token_count,
    formatted_truncate_codex_exec_response,
    formatted_truncate_text,
    retain_head_tail_bytes,
    truncate_middle_chars,
    truncate_middle_with_token_budget,
)


def test_retain_head_tail_bytes_keeps_symmetric_prefix_and_suffix():
    text = "A" * (UNIFIED_EXEC_OUTPUT_MAX_BYTES // 2 + 20)
    text += "MIDDLE"
    text += "Z" * (UNIFIED_EXEC_OUTPUT_MAX_BYTES // 2 + 20)

    retained = retain_head_tail_bytes(text)

    assert len(retained.encode("utf-8")) == UNIFIED_EXEC_OUTPUT_MAX_BYTES
    assert retained.startswith("A" * 100)
    assert retained.endswith("Z" * 100)
    assert "MIDDLE" not in retained


def test_head_tail_buffer_streams_without_retaining_middle():
    buffer = HeadTailBuffer(12)

    buffer.push_chunk(b"abcde")
    buffer.push_chunk(b"fghij")
    buffer.push_chunk(b"klmno")

    assert buffer.retained_bytes() == 12
    assert buffer.to_bytes() == b"abcdefjklmno"
    assert buffer.omitted_bytes == 3


def test_head_tail_buffer_codex_edge_cases():
    zero = HeadTailBuffer(0)
    zero.push_chunk(b"abc")
    assert zero.retained_bytes() == 0
    assert zero.omitted_bytes == 3
    assert zero.to_bytes() == b""

    one = HeadTailBuffer(1)
    one.push_chunk(b"abc")
    assert one.retained_bytes() == 1
    assert one.omitted_bytes == 2
    assert one.to_bytes() == b"c"

    large_tail = HeadTailBuffer(10)
    large_tail.push_chunk(b"0123456789")
    large_tail.push_chunk(b"ABCDEFGHIJK")
    assert large_tail.to_bytes().startswith(b"01234")
    assert large_tail.to_bytes().endswith(b"GHIJK")


def test_head_tail_buffer_keeps_valid_lossy_text_when_split_inside_utf8():
    buffer = HeadTailBuffer(7)

    buffer.push_chunk("前".encode("utf-8") + b"A" * 10 + "后".encode("utf-8"))

    text = buffer.to_text_lossy()
    assert text.startswith("前")
    assert text.endswith("后")
    assert len(text.encode("utf-8")) >= buffer.retained_bytes()


def test_truncate_middle_matches_codex_string_examples():
    text = "example output"

    assert truncate_middle_chars(text, 1) == "\u202613 chars truncated\u2026t"
    assert truncate_middle_with_token_budget(text, 1)[0] == "ex\u20263 tokens truncated\u2026ut"

    longer = "this is an example of a long output that should be truncated"
    assert (
        truncate_middle_with_token_budget(longer, 5)[0]
        == "this is an\u202610 tokens truncated\u2026 truncated"
    )


def test_truncate_middle_respects_utf8_boundaries():
    text = "😀😀😀😀😀😀😀😀😀😀\nsecond line with text\n"

    assert truncate_middle_chars(text, 20) == "😀😀\u202621 chars truncated\u2026with text\n"
    assert truncate_middle_with_token_budget(text, 8) == (
        "😀😀😀😀\u20268 tokens truncated\u2026 line with text\n",
        16,
    )


def test_formatted_truncate_text_zero_budget_matches_codex_marker_only():
    text = "prefix-" + ("A" * 20) + "-suffix"

    truncated = formatted_truncate_text(text, max_tokens=0)

    assert truncated.startswith(
        f"Warning: truncated output (original token count: {approx_token_count(text)})\n"
        "Total output lines: 1\n\n"
    )
    assert "tokens truncated" in truncated
    assert "prefix-" not in truncated
    assert "-suffix" not in truncated


def test_formatted_truncate_text_matches_codex_warning_shape():
    text = "A" * (DEFAULT_MAX_OUTPUT_TOKENS * 4 + 200)

    truncated = formatted_truncate_text(text)

    assert truncated.startswith(
        f"Warning: truncated output (original token count: {approx_token_count(text)})\n"
        "Total output lines: 1\n\n"
    )
    assert "tokens truncated" in truncated
    assert truncated.startswith("Warning: truncated output")
    assert len(truncated) < len(text)


def test_formatted_truncate_text_honors_per_call_token_budget():
    text = "prefix-" + ("A" * 500) + "-suffix"

    truncated = formatted_truncate_text(text, max_tokens=20)

    assert "Warning: truncated output" in truncated
    assert "prefix-" in truncated
    assert "-suffix" in truncated
    assert "tokens truncated" in truncated


def test_codex_exec_response_truncates_only_output_body():
    body = "prefix-" + ("A" * 500) + "-suffix"
    text = (
        "Chunk ID: abc123\n"
        "Wall time: 0.0100 seconds\n"
        "Process exited with code 0\n"
        "Original token count: 129\n"
        "Output:\n"
        f"{body}"
    )

    truncated = formatted_truncate_codex_exec_response(text, max_tokens=20)

    assert truncated.startswith(
        "Chunk ID: abc123\n"
        "Wall time: 0.0100 seconds\n"
        "Process exited with code 0\n"
        "Original token count: 129\n"
        "Output:\n"
        "Warning: truncated output"
    )
    assert "prefix-" in truncated
    assert "-suffix" in truncated
