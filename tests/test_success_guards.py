import unittest

from pikaqiu_agent.success_guards import (
    _is_broad_scan_tool_call,
    _post_partial_flag_guidance,
    _round_time_guidance,
    _route_guard_guidance,
    _summarize_advice_result,
)


class SuccessGuardTests(unittest.TestCase):
    def test_round_time_guidance_has_two_budget_levels(self):
        self.assertIsNone(_round_time_guidance(120))
        self.assertIn("[ROUND_TIME_LIMITED]", _round_time_guidance(60))
        self.assertIn("[ROUND_TIME_CRITICAL]", _round_time_guidance(20))

    def test_broad_scan_detection(self):
        self.assertTrue(_is_broad_scan_tool_call("bash_exec", "ffuf -w common.txt -u http://x/FUZZ"))
        self.assertTrue(_is_broad_scan_tool_call("python_exec", "run arjun against target"))
        self.assertFalse(_is_broad_scan_tool_call("ask_adviser", "ffuf example"))
        self.assertFalse(_is_broad_scan_tool_call("bash_exec", "curl -i http://x/admin"))

    def test_route_guard_prefers_highest_value_lead(self):
        memory = {
            "summary": "Authenticated session and Apache cgi-bin %2e%2e alias observed.",
            "highest_value_lead": "Verify /cgi-bin/%2e%2e/.htaccess direct-vs-alias parity",
        }
        guidance = _route_guard_guidance(memory)
        self.assertIn("[ROUTE_GUARD]", guidance)
        self.assertIn("Highest-value lead", guidance)
        self.assertIn("Auth state", guidance)
        self.assertIn("Apache/cgi", guidance)

    def test_advice_result_truncation_marks_guidance_only(self):
        text = "advice\n" + ("A" * 5000)
        summarized = _summarize_advice_result("ask_adviser", text, 1000)
        self.assertLess(len(summarized), len(text))
        self.assertIn("guidance only", summarized)

    def test_partial_flag_guidance_blocks_broad_scans(self):
        guidance = _post_partial_flag_guidance(["flag{one123}"], 2)
        self.assertIn("Captured 1/2", guidance)
        self.assertIn("Do not run broad scans", guidance)


if __name__ == "__main__":
    unittest.main()
