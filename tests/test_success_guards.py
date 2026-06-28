import unittest

from pikaqiu_agent.success_guards import (
    _post_partial_flag_guidance,
    _route_guard_guidance,
    _stale_observer_steer_block_message,
    _summarize_guidance_result,
)


class SuccessGuardTests(unittest.TestCase):
    def test_route_guard_uses_current_lead(self):
        memory = {
            "summary": "Authenticated session and Apache cgi-bin %2e%2e alias observed.",
            "leads": ["Verify /cgi-bin/%2e%2e/.htaccess direct-vs-alias parity"],
        }
        guidance = _route_guard_guidance(memory)
        self.assertIn("[ROUTE_GUARD]", guidance)
        self.assertIn("Highest-value lead", guidance)
        self.assertIn("Auth state", guidance)

    def test_guidance_result_truncation_uses_codex_format(self):
        text = "guidance\n" + ("A" * 5000)
        summarized = _summarize_guidance_result("knowledge_search", text, 1000)
        self.assertLess(len(summarized), len(text))
        self.assertIn("Warning: truncated output", summarized)
        self.assertIn("tokens truncated", summarized)

    def test_stale_observer_guard_uses_codex_exit_marker(self):
        guidance = _stale_observer_steer_block_message({"leads": ["verify target"]})
        self.assertIn("Process exited with code 0", guidance)
        self.assertNotIn("[EXIT_CODE:", guidance)

    def test_partial_flag_guidance_reports_remaining_flags(self):
        guidance = _post_partial_flag_guidance(["flag{one123}"], 2)
        self.assertIn("Captured 1/2", guidance)
        self.assertIn("1 flag(s) remain", guidance)


if __name__ == "__main__":
    unittest.main()
