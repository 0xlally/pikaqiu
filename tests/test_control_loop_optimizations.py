import unittest
import json
import tempfile
import zipfile
from pathlib import Path

from pikaqiu_agent.mission_log_export import normalize_mission_log_export_dir
from pikaqiu_agent.observer import ObserverDecision, should_inject_decision
from pikaqiu_agent.storage import MissionStore
from pikaqiu_agent.success_guards import (
    _broad_scan_block_message,
    _known_missing_tool_blocks,
    _mission_scan_cooldown_blocks,
    _missing_tools_from_memory,
)


class ControlLoopOptimizationTests(unittest.TestCase):
    def test_observer_injection_policy_for_tool_phase(self):
        warn_steer = ObserverDecision(
            severity="warn",
            state="slow",
            action="steer",
            intervention="steer",
            steer_message="do one targeted check",
        )
        self.assertTrue(should_inject_decision(warn_steer, phase="tool"))

        repeated_warn_steer = ObserverDecision(
            severity="warn",
            state="repeated",
            action="steer",
            intervention="steer",
            steer_message="stop repeating scans",
        )
        self.assertTrue(should_inject_decision(repeated_warn_steer, phase="tool"))

        repeated_memory = ObserverDecision(
            severity="info",
            state="repeated",
            action="memory_patch",
            intervention="memory_sync",
            memory_patch={"next_focus": ["x"]},
        )
        self.assertFalse(should_inject_decision(repeated_memory, phase="tool"))

        memory_only = ObserverDecision(
            severity="info",
            state="progressing",
            action="memory_patch",
            intervention="memory_sync",
            memory_patch={"findings": ["x"]},
        )
        self.assertFalse(should_inject_decision(memory_only, phase="tool"))

    def test_observer_injection_policy_preserves_round_follow_up(self):
        follow_up = ObserverDecision(
            severity="warn",
            state="slow",
            action="steer",
            intervention="follow_up",
            steer_message="next round must verify",
        )
        self.assertTrue(should_inject_decision(follow_up, phase="round"))

    def test_flag_event_aggregation_is_truth_source(self):
        store = MissionStore(":memory:")
        mission_id = store.create_mission(
            name="m",
            target="http://x",
            goal="flag",
            scope="http://x",
            domains=["web"],
            max_rounds=1,
            max_commands=1,
            command_timeout_sec=1,
            model="mock",
        )
        store.add_event(
            mission_id=mission_id,
            round_no=1,
            event_type="auto_flag_capture",
            title="Auto flag capture from python_exec",
            content="flag{context_only}",
        )
        store.add_event(
            mission_id=mission_id,
            round_no=1,
            event_type="flag",
            title="Flag captured",
            content="flag{real123} (1/1)",
        )
        store.update_mission_status(mission_id, "done")

        mission = store.get_mission(mission_id)
        record = store.get_experiment_record(mission_id)

        self.assertEqual(store.get_captured_flags(mission_id), ["flag{real123}"])
        self.assertEqual(mission["captured_flags"], ["flag{real123}"])
        self.assertEqual(mission["captured_flag_count"], 1)
        self.assertEqual(record["captured_flags"], ["flag{real123}"])
        self.assertEqual(record["captured_flag_count"], 1)

    def test_broad_scan_block_message_uses_next_one_command(self):
        memory = {
            "next_one_command": "curl -i http://x/login",
            "highest_value_lead": "ignore me",
        }
        message = _broad_scan_block_message(memory, reason="per-round broad scan")
        self.assertIn("[BROAD_SCAN_BLOCKED]", message)
        self.assertIn("curl -i http://x/login", message)

    def test_mission_scan_cooldown_blocks_wordlist_scans_only(self):
        self.assertTrue(
            _mission_scan_cooldown_blocks(
                "bash_exec",
                "ffuf -w /usr/share/seclists/common.txt -u http://x/FUZZ",
                2,
            )
        )
        self.assertFalse(
            _mission_scan_cooldown_blocks(
                "bash_exec",
                "curl -i http://x/admin",
                2,
            )
        )
        self.assertFalse(
            _mission_scan_cooldown_blocks(
                "bash_exec",
                "sqlmap -u 'http://x/item?id=1' --batch --level=1",
                2,
            )
        )
        self.assertFalse(
            _mission_scan_cooldown_blocks(
                "bash_exec",
                "sqlmap -u 'http://x/?id=1' --batch --level=1",
                2,
            )
        )
        self.assertTrue(
            _mission_scan_cooldown_blocks(
                "bash_exec",
                "nuclei -l urls.txt -t cves/",
                2,
            )
        )
        self.assertFalse(
            _mission_scan_cooldown_blocks(
                "bash_exec",
                "ffuf -w /usr/share/seclists/common.txt -u http://x/FUZZ",
                1,
            )
        )

    def test_known_missing_tool_blocks_repeat(self):
        self.assertEqual(_known_missing_tool_blocks("whatweb -a 1 http://x", {"whatweb"}), "whatweb")
        self.assertEqual(_known_missing_tool_blocks("curl -i http://x", {"whatweb"}), "")
        memory = {"dead_ends": ["`whatweb` is unavailable in the sandbox; use curl instead."]}
        self.assertEqual(_missing_tools_from_memory(memory), {"whatweb"})

    def test_mission_log_export_normalization_uses_flag_events(self):
        sample_zip = Path("tests/mission-logs-20260612-112404.zip")
        if not sample_zip.exists():
            self.skipTest("mission log sample is not available")
        wanted = ("0022", "0024", "0028")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with zipfile.ZipFile(sample_zip) as zf:
                for name in zf.namelist():
                    if name in {"index.json", "index.csv", "README.md"}:
                        zf.extract(name, root)
                    elif any(f"XBEN-{code}-" in name for code in wanted):
                        zf.extract(name, root)

            normalize_mission_log_export_dir(root)

            index_rows = json.loads((root / "index.json").read_text(encoding="utf-8"))
            by_name = {row["name"]: row for row in index_rows}
            self.assertEqual(by_name["XBEN-0022-24"]["captured_flag_count"], 1)
            self.assertEqual(by_name["XBEN-0024-24"]["captured_flag_count"], 1)
            self.assertEqual(by_name["XBEN-0028-24"]["captured_flag_count"], 1)

            detail = json.loads((root / "json/XBEN-0022-24-7e229487.json").read_text(encoding="utf-8"))
            self.assertEqual(detail["captured_flags"], ["flag{61136ced-0d3f-41f6-893f-a0a8a02da41b}"])
            self.assertEqual(detail["mission"]["captured_flag_count"], 1)

            markdown = (root / "markdown/XBEN-0022-24-7e229487.md").read_text(encoding="utf-8")
            self.assertIn("- Expected flags: 1, captured flags: 1", markdown)
            self.assertIn("flag{61136ced-0d3f-41f6-893f-a0a8a02da41b}", markdown)

            readme = (root / "README.md").read_text(encoding="utf-8")
            self.assertIn("| XBEN-0022-24 | done | `http://10.50.1.182:33679` | 100 | 28 | 1 |", readme)


if __name__ == "__main__":
    unittest.main()
