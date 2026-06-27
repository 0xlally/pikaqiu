import unittest
import json
import tempfile
import zipfile
from pathlib import Path

from langchain_core.messages import HumanMessage

from pikaqiu_agent.orchestrator import (
    OrchestratorManager,
    _compress_context_middle,
    _estimate_messages_size,
    _memory_agent_long_term_review_block,
)
from pikaqiu_agent.mission_log_export import normalize_mission_log_export_dir
from pikaqiu_agent.observer import ObserverDecision, should_inject_decision
from pikaqiu_agent.storage import MissionStore
from pikaqiu_agent.success_guards import (
    _broad_scan_block_message,
    _known_missing_tool_blocks,
    _mission_scan_cooldown_blocks,
    _missing_tools_from_memory,
)


class ObserverCorrectionRoutingHarness(OrchestratorManager):
    def __init__(self, store: MissionStore, *, human_guidance: list[str] | None = None) -> None:
        self.store = store
        self.observer = None  # type: ignore[assignment]
        from pikaqiu_agent.observer import ObserverAgent

        self.observer = ObserverAgent()
        self.human_guidance = human_guidance or []
        self.asked = False
        self.observer_injected = False

    def _ask_human_before_observer_correction(self, **kwargs):  # type: ignore[no-untyped-def]
        if not self._human_collab_enabled(kwargs["mission_id"]):
            return []
        self.asked = True
        return list(self.human_guidance)

    def _inject_observer_steer(self, **kwargs):  # type: ignore[no-untyped-def]
        self.observer_injected = True
        messages = kwargs.get("messages")
        if messages is not None:
            messages.append(HumanMessage(content="observer fallback"))
        return True


class FakeCompressionLLM:
    def __init__(self, summary: str | None, *, available: bool = True) -> None:
        self.summary = summary
        self.has_compression_model = available
        self.calls = []

    def invoke_compression(self, messages_text, mission_context):  # type: ignore[no-untyped-def]
        self.calls.append((messages_text, mission_context))
        return self.summary


class ControlLoopOptimizationTests(unittest.TestCase):
    def test_mid_round_context_compression_prefers_model_when_available(self):
        middle = [
            HumanMessage(content=f"confirmed lead {idx}: /wp-json/wp/v2/users " + "A" * 800)
            for idx in range(3)
        ]
        fake_llm = FakeCompressionLLM(
            (
                "- 保留 WordPress REST 用户枚举证据：/wp-json/wp/v2/users 返回用户列表。\n"
                "- 保留插件扫描死路：宽扫没有形成可复现利用链，后续应转向认证、主题或 REST 权限边界。\n"
                "- 保留当前目标、路径和失败分支，避免下一轮重复枚举。"
            )
        )

        summary, metadata = _compress_context_middle(
            middle=middle,
            msg_size=_estimate_messages_size(middle),
            mission={"target": "http://target", "goal": "capture flag"},
            llm=fake_llm,  # type: ignore[arg-type]
            compression_timeout_sec=5,
            compression_model="gpt-5.5",
        )

        self.assertEqual(metadata["method"], "model")
        self.assertEqual(metadata["model"], "gpt-5.5")
        self.assertEqual(metadata["error"], "")
        self.assertGreater(metadata["summary_chars"], 50)
        self.assertEqual(len(fake_llm.calls), 1)
        self.assertIn("[上下文已由压缩模型智能压缩]", summary)
        self.assertIn("/wp-json/wp/v2/users", summary)

    def test_mid_round_context_compression_records_fallback_when_model_unavailable(self):
        middle = [
            HumanMessage(content=f"dead end {idx}: directory brute force timed out " + "B" * 300)
            for idx in range(2)
        ]
        fake_llm = FakeCompressionLLM(None, available=False)

        summary, metadata = _compress_context_middle(
            middle=middle,
            msg_size=_estimate_messages_size(middle),
            mission={"target": "http://target", "goal": "capture flag"},
            llm=fake_llm,  # type: ignore[arg-type]
            compression_timeout_sec=5,
            compression_model="gpt-5.5",
        )

        self.assertEqual(metadata["method"], "fallback")
        self.assertEqual(metadata["model"], "")
        self.assertEqual(metadata["error"], "compression model unavailable")
        self.assertEqual(len(fake_llm.calls), 0)
        self.assertIn("[上下文过大，中间对话已按重要性压缩]", summary)

    def test_mid_round_context_compression_injects_long_term_memory_review(self):
        block, metadata = _memory_agent_long_term_review_block(
            {
                "summary": "WordPress target with REST user enumeration.",
                "findings": ["GET /wp-json/wp/v2/users returned wordpress_admin"],
                "leads": ["Verify authenticated route or plugin chain"],
                "dead_ends": ["Do not repeat broad plugin scan without token"],
                "credentials": ["wordpress_admin candidate"],
                "topology": ["browser -> WordPress"],
            }
        )

        self.assertTrue(metadata["injected"])
        self.assertEqual(metadata["findings"], 1)
        self.assertEqual(metadata["leads"], 1)
        self.assertIn("[MEMORY_AGENT_LONG_TERM_REVIEW]", block)
        self.assertIn("下一次选择工具前，必须先对照 Memory Agent 的长期记忆", block)
        self.assertIn("wordpress_admin", block)
        self.assertIn("Do not repeat broad plugin scan", block)

    def test_observer_injection_policy_for_tool_phase(self):
        warn_steer = ObserverDecision(
            verdict="WATCH",
            guidance="do one targeted check",
        )
        self.assertFalse(should_inject_decision(warn_steer, phase="tool"))

        repeated_warn_steer = ObserverDecision(
            verdict="L4",
            guidance="stop repeating scans",
        )
        self.assertTrue(should_inject_decision(repeated_warn_steer, phase="tool"))

        repeated_memory = ObserverDecision(
            verdict="WATCH",
            memory_patch={"leads": ["x"]},
        )
        self.assertFalse(should_inject_decision(repeated_memory, phase="tool"))

        memory_only = ObserverDecision(
            verdict="OK",
            memory_patch={"findings": ["x"]},
        )
        self.assertFalse(should_inject_decision(memory_only, phase="tool"))

    def test_observer_injection_policy_preserves_round_follow_up(self):
        follow_up = ObserverDecision(
            verdict="L2",
            guidance="next round must verify",
        )
        self.assertTrue(should_inject_decision(follow_up, phase="round"))

    def test_observer_injection_policy_allows_round_strong_evidence_signal(self):
        signal = ObserverDecision(
            verdict="WATCH",
            guidance="close the proven LFI chain",
            observer_enforcement_state="strong_evidence",
        )

        self.assertFalse(should_inject_decision(signal, phase="tool"))
        self.assertTrue(should_inject_decision(signal, phase="round"))

    def test_missing_tool_memory_patch_is_not_labeled_as_observer(self):
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
        harness = ObserverCorrectionRoutingHarness(store)

        memory = harness._apply_observer_memory_patch(
            mission_id=mission_id,
            round_no=1,
            memory=store.get_memory(mission_id),
            source="missing_tool",
            decision=ObserverDecision(
                verdict="OK",
                memory_patch={"dead_ends": ["post is unavailable in the sandbox"]},
            ),
        )
        events = store.get_events(mission_id)

        self.assertIn("`post`", memory["dead_ends"][0])
        self.assertIn("is unavailable in the sandbox", memory["dead_ends"][0])
        self.assertEqual(events[0]["type"], "memory_agent")
        self.assertEqual(events[0]["title"], "Missing tool memory sync applied")
        self.assertNotIn("Observer", events[0]["title"])
        self.assertEqual(events[0]["metadata"]["memory_patch_source"], "missing_tool")
        self.assertEqual(
            events[0]["metadata"]["memory_patch"],
            {"dead_ends": ["post is unavailable in the sandbox"]},
        )
        self.assertNotIn("observer_memory_patch", events[0]["metadata"])

    def test_observer_memory_patch_keeps_observer_event_label(self):
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
        harness = ObserverCorrectionRoutingHarness(store)

        harness._apply_observer_memory_patch(
            mission_id=mission_id,
            round_no=1,
            memory=store.get_memory(mission_id),
            decision=ObserverDecision(
                verdict="WATCH",
                memory_patch={"leads": ["verify /admin with browser"]},
            ),
        )
        events = store.get_events(mission_id)

        self.assertEqual(events[0]["type"], "observer_agent")
        self.assertEqual(events[0]["title"], "Observer memory sync applied")
        self.assertEqual(events[0]["metadata"]["memory_patch_source"], "observer")
        self.assertEqual(
            events[0]["metadata"]["observer_memory_patch"],
            {"leads": ["verify /admin with browser"]},
        )
        self.assertNotIn("memory_patch", events[0]["metadata"])

    def test_human_collaboration_intercepts_observer_correction(self):
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
        store.set_human_collab_enabled(mission_id, True)
        harness = ObserverCorrectionRoutingHarness(store, human_guidance=["先验证 /admin 的 403/200 差异"])
        messages = []

        injected, pending = harness._route_observer_correction(
            mission_id=mission_id,
            round_no=1,
            decision=ObserverDecision(verdict="L2", guidance="observer next step"),
            phase="round",
            messages=messages,
        )

        self.assertTrue(injected)
        self.assertIsNone(pending)
        self.assertTrue(harness.asked)
        self.assertFalse(harness.observer_injected)
        self.assertIn("HUMAN_OBSERVER_CORRECTION", messages[-1].content)
        self.assertIn("/admin", messages[-1].content)

    def test_observer_correction_falls_back_when_collaboration_disabled(self):
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
        harness = ObserverCorrectionRoutingHarness(store, human_guidance=["ignored"])
        messages = []

        injected, pending = harness._route_observer_correction(
            mission_id=mission_id,
            round_no=1,
            decision=ObserverDecision(verdict="L2", guidance="observer next step"),
            phase="round",
            messages=messages,
        )

        self.assertTrue(injected)
        self.assertIsNotNone(pending)
        self.assertTrue(harness.observer_injected)
        self.assertIn("observer fallback", messages[-1].content)

    def test_observer_summary_counts_verdicts(self):
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
        for verdict in ("OK", "WATCH", "L2"):
            store.add_observer_message(
                mission_id=mission_id,
                round_no=1,
                message_type="decision",
                direction="out",
                title=f"Observer decision: {verdict}",
                content=verdict,
                metadata={"decision": ObserverDecision(verdict=verdict).to_dict()},
            )

        summary = store.get_observer_summary(mission_id)

        self.assertEqual(summary["stats"]["ok"], 1)
        self.assertEqual(summary["stats"]["watch"], 1)
        self.assertEqual(summary["stats"]["interrupts"], 1)

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

    def test_broad_scan_block_message_uses_current_lead(self):
        memory = {
            "leads": ["curl -i http://x/login"],
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
                "echo 'sqlmap later'; curl -i http://x/admin",
                2,
            )
        )
        self.assertFalse(
            _mission_scan_cooldown_blocks(
                "bash_exec",
                "command -v sqlmap || true",
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
        memory = {
            "dead_ends": [
                (
                    "工具链卡点：已尝试调用 `whatweb`，原始结果显示 "
                    "`whatweb` is unavailable in the sandbox；当前沙箱缺少该工具，后续改用 curl。"
                )
            ]
        }
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
