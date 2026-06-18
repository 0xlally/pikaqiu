from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from pikaqiu_agent import experience
from pikaqiu_agent.prompts import build_volatile_context


class SharedMemoryExperienceTests(unittest.TestCase):
    def test_experience_search_includes_manual_and_distilled_sources(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manual = root / "experience" / "rules"
            distilled = root / ".pikaqiu_agent" / "experience_distilled"
            manual.mkdir(parents=True)
            distilled.mkdir(parents=True)
            (manual / "upload.md").write_text(
                "# Upload Bypass\nUse polyglot upload when image parser saves server-side paths.",
                encoding="utf-8",
            )
            (distilled / "mission-upload.md").write_text(
                "# Distilled Experience\n"
                "source_mission_id: m-123\n"
                "confidence: high\n\n"
                "## Vulnerability Type\n"
                "Upload parser bypass with polyglot payload.\n",
                encoding="utf-8",
            )

            rows = experience.search_experience(root, "upload polyglot parser", limit=5)

            by_path = {row["path"]: row for row in rows}
            self.assertIn("experience/rules/upload.md", by_path)
            self.assertIn(".pikaqiu_agent/experience_distilled/mission-upload.md", by_path)
            self.assertFalse(by_path["experience/rules/upload.md"]["distilled"])
            self.assertTrue(by_path[".pikaqiu_agent/experience_distilled/mission-upload.md"]["distilled"])
            self.assertEqual(
                by_path[".pikaqiu_agent/experience_distilled/mission-upload.md"]["source_mission_id"],
                "m-123",
            )

            hints = experience.format_experience_hints(rows, limit=5)
            self.assertIn("## Distilled Experience Hints", hints)
            self.assertIn("[manual] experience/rules/upload.md", hints)
            self.assertIn("[distilled] .pikaqiu_agent/experience_distilled/mission-upload.md", hints)
            self.assertIn("source_mission_id=m-123", hints)

    def test_volatile_context_orders_boards_and_injects_experience_hints(self):
        memory = {
            "idea_board": {
                "active_direction": "verify upload parser",
                "primary_hypothesis": "polyglot payload reaches parser",
                "next_verification": "curl -F file=@polyglot.jpg http://x/upload",
                "failure_boundary": "upload rejects all image types",
            },
            "memory_board": {
                "facts": ["upload endpoint exists"],
                "evidence": ["GET /upload returned 200"],
                "failed_attempts": ["directory brute force timed out"],
            },
        }
        hints = "## Distilled Experience Hints\n- [distilled] .pikaqiu_agent/experience_distilled/a.md: upload parser"

        context = build_volatile_context(
            round_no=3,
            memory=memory,
            captured_flags=[],
            expected_flags=1,
            experience_hints=hints,
        )

        self.assertLess(context.index("Idea Board"), context.index("Memory Board"))
        self.assertLess(context.index("Memory Board"), context.index("Distilled Experience Hints"))
        self.assertIn("next_verification: curl -F file=@polyglot.jpg http://x/upload", context)
        self.assertIn("failure_boundary: upload rejects all image types", context)
        self.assertIn("upload endpoint exists", context)
        self.assertNotIn("tool_call_log", context)

    def test_observer_runtime_memory_view_exposes_two_boards(self):
        try:
            from pikaqiu_agent.observer_runtime import ObserverRuntime
        except ModuleNotFoundError as exc:
            raise unittest.SkipTest(f"optional observer runtime dependency is unavailable: {exc.name}") from exc

        runtime = object.__new__(ObserverRuntime)
        view = runtime._memory_view(
            {
                "idea_board": {
                    "active_direction": "probe admin",
                    "next_actions": ["curl -i http://x/admin"],
                },
                "memory_board": {
                    "facts": ["admin route exists"],
                    "evidence": ["HTTP 401 from /admin"],
                    "credentials": ["admin:admin"],
                },
            }
        )

        self.assertEqual(view["idea_board"]["active_direction"], "probe admin")
        self.assertEqual(view["idea_board"]["next_actions"], ["curl -i http://x/admin"])
        self.assertEqual(view["memory_board"]["facts"], ["admin route exists"])
        self.assertEqual(view["memory_board"]["evidence"], ["HTTP 401 from /admin"])
        self.assertEqual(view["memory_board"]["credentials"], ["admin:admin"])


if __name__ == "__main__":
    unittest.main()
