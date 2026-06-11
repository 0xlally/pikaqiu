import unittest

from pikaqiu_agent.flag_capture import (
    _append_flag_candidate_summary,
    _auto_capture_trusted_flag_events,
    _auto_capture_trusted_flags,
    _extract_flag_candidates,
    _flag_context,
    _trusted_tool_flag_candidates,
    _truncate_middle,
)


class FlagAutoCaptureTests(unittest.TestCase):
    def test_python_exec_result_auto_captures_flag(self):
        captured = []

        def on_flag(flag):
            captured.append(flag)
            return f"[FLAG_CAPTURED] {flag}"

        results = _auto_capture_trusted_flags(
            tool_name="python_exec",
            result_str="HTTP/1.1 200 OK\nflag{abc123}",
            captured_flags=captured,
            on_flag=on_flag,
            is_complete=lambda: bool(captured),
        )

        self.assertEqual(captured, ["flag{abc123}"])
        self.assertEqual(results, ["[FLAG_CAPTURED] flag{abc123}"])

    def test_adviser_and_placeholder_flags_are_not_auto_captured(self):
        self.assertEqual(_trusted_tool_flag_candidates("ask_adviser", "flag{realish123}"), [])
        self.assertEqual(_trusted_tool_flag_candidates("knowledge_search", "flag{realish123}"), [])
        self.assertEqual(_trusted_tool_flag_candidates("python_exec", "flag{example}"), [])
        self.assertEqual(_trusted_tool_flag_candidates("bash_exec", "flag{test_value}"), [])
        self.assertEqual(_trusted_tool_flag_candidates("python_exec", "flag{your_flag_here}"), [])

    def test_flag_summary_survives_middle_truncation(self):
        flag = "flag{98d2361b-f883-4daa-93f7-cb5c91a32c69}"
        text = "A" * 500 + "\n" + flag + "\n" + "Z" * 500
        truncated = _truncate_middle(text, 120)
        self.assertNotIn(flag, truncated)

        with_summary = _append_flag_candidate_summary(truncated, _extract_flag_candidates(text))
        self.assertIn(f"[FLAG_CANDIDATES] {flag}", with_summary)

    def test_multi_flag_capture_stops_when_complete(self):
        captured = []

        def on_flag(flag):
            captured.append(flag)
            return f"[FLAG_CAPTURED] {flag}"

        _auto_capture_trusted_flags(
            tool_name="bash_exec",
            result_str="flag{one123} flag{two456}",
            captured_flags=captured,
            on_flag=on_flag,
            is_complete=lambda: len(captured) >= 1,
        )

        self.assertEqual(captured, ["flag{one123}"])

    def test_only_result_text_is_scanned_by_helper(self):
        captured = []

        def on_flag(flag):
            captured.append(flag)
            return f"[FLAG_CAPTURED] {flag}"

        _auto_capture_trusted_flags(
            tool_name="python_exec",
            result_str="[EXIT_CODE: 0]",
            captured_flags=captured,
            on_flag=on_flag,
            is_complete=lambda: False,
        )

        self.assertEqual(captured, [])

    def test_payload_example_in_command_source_is_not_scanned(self):
        captured = []

        def on_flag(flag):
            captured.append(flag)
            return f"[FLAG_CAPTURED] {flag}"

        command_source = 'python3 -c "print(\\"flag{fake_from_source}\\")"'
        self.assertIn("flag{fake_from_source}", command_source)

        _auto_capture_trusted_flags(
            tool_name="python_exec",
            result_str="[EXIT_CODE: 0]",
            captured_flags=captured,
            on_flag=on_flag,
            is_complete=lambda: False,
        )

        self.assertEqual(captured, [])

    def test_xben_0025_log_sample_auto_captures(self):
        captured = []
        flag = "flag{98d2361b-f883-4daa-93f7-cb5c91a32c69}"

        def on_flag(found):
            captured.append(found)
            return f"[FLAG_CAPTURED] {found}"

        results = _auto_capture_trusted_flags(
            tool_name="python_exec",
            result_str=(
                "HTTP/1.1 200 OK\n"
                "Step3 response after payload {% debug %}\n"
                f"{flag}\n"
                "[EXIT_CODE: 0]"
            ),
            captured_flags=captured,
            on_flag=on_flag,
            is_complete=lambda: len(captured) >= 1,
        )

        self.assertEqual(captured, [flag])
        self.assertEqual(results, [f"[FLAG_CAPTURED] {flag}"])

    def test_html_escaped_django_debug_flag_auto_captures(self):
        captured = []
        flag = "flag{98d2361b-f883-4daa-93f7-cb5c91a32c69}"

        def on_flag(found):
            captured.append(found)
            return f"[FLAG_CAPTURED] {found}"

        results = _auto_capture_trusted_flags(
            tool_name="python_exec",
            result_str=(
                '<script>alert("Hello {&#x27;flag&#x27;: '
                f'&#x27;{flag}&#x27;}}")</script>'
            ),
            captured_flags=captured,
            on_flag=on_flag,
            is_complete=lambda: len(captured) >= 1,
        )

        self.assertEqual(captured, [flag])
        self.assertEqual(results, [f"[FLAG_CAPTURED] {flag}"])

    def test_json_escaped_flag_auto_captures(self):
        captured = []
        flag = "flag{json_escape_123}"

        def on_flag(found):
            captured.append(found)
            return f"[FLAG_CAPTURED] {found}"

        results = _auto_capture_trusted_flags(
            tool_name="bash_exec",
            result_str='{"debug":"flag\\u007bjson_escape_123\\u007d"}',
            captured_flags=captured,
            on_flag=on_flag,
            is_complete=lambda: bool(captured),
        )

        self.assertEqual(captured, [flag])
        self.assertEqual(results, [f"[FLAG_CAPTURED] {flag}"])

    def test_auto_capture_events_only_include_new_flags(self):
        captured = ["flag{old123}"]

        def on_flag(found):
            captured.append(found)
            return f"[FLAG_CAPTURED] {found}"

        events = _auto_capture_trusted_flag_events(
            tool_name="python_exec",
            result_str="flag{old123}\nflag{new456}",
            captured_flags=captured,
            on_flag=on_flag,
            is_complete=lambda: False,
        )

        self.assertEqual(events, [("flag{new456}", "[FLAG_CAPTURED] flag{new456}")])
        self.assertEqual(captured, ["flag{old123}", "flag{new456}"])

    def test_json_escaped_flag_context(self):
        context = _flag_context('{"debug":"flag\\u007bjson_escape_123\\u007d"}', "flag{json_escape_123}")
        self.assertIn("flag{json_escape_123}", context)


if __name__ == "__main__":
    unittest.main()
