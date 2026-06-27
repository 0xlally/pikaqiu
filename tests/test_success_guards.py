import unittest

from pikaqiu_agent.success_guards import (
    _post_partial_flag_guidance,
    _route_guard_guidance,
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

    def test_guidance_result_truncation_marks_guidance_only(self):
        text = "guidance\n" + ("A" * 5000)
        summarized = _summarize_guidance_result("knowledge_search", text, 1000)
        self.assertLess(len(summarized), len(text))
        self.assertIn("guidance only", summarized)

    def test_partial_flag_guidance_reports_remaining_flags(self):
        guidance = _post_partial_flag_guidance(["flag{one123}"], 2)
        self.assertIn("Captured 1/2", guidance)
        self.assertIn("1 flag(s) remain", guidance)


if __name__ == "__main__":
    unittest.main()
