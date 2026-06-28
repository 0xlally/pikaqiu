import unittest
import json
import tempfile
import zipfile
from pathlib import Path

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage

from pikaqiu_agent.orchestrator import (
    OrchestratorManager,
    _CONTEXT_COMPRESSION_SUMMARY_MARKER,
    _build_compressed_round_messages,
    _compress_context_middle,
    _count_context_tokens,
    _memory_agent_long_term_review_block,
    _next_observer_review_due_after,
    _tool_call_memory_view,
    _plan_round_context_compression,
    _tool_result_for_model,
)
from pikaqiu_agent.mission_log_export import normalize_mission_log_export_dir
from pikaqiu_agent.observer import ObserverDecision, should_inject_decision
from pikaqiu_agent.observer import ObserverAgent
from pikaqiu_agent.observer_runtime import ObserverRuntime
from pikaqiu_agent.config import AgentSettings
from pikaqiu_agent.llm_client import LLMResult
from pikaqiu_agent.storage import MissionStore


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


class FakeObserverLLM:
    def invoke_observer_runtime(self, prompt, system):  # type: ignore[no-untyped-def]
        return LLMResult(
            raw_text='{"verdict":"OK","rationale":"interval review complete"}',
            payload={"verdict": "OK", "rationale": "interval review complete"},
            used_mock=False,
        )


class ControlLoopOptimizationTests(unittest.TestCase):
    def test_mid_round_context_compression_prefers_model_when_available(self):
        middle = [
            HumanMessage(content=f"confirmed lead {idx}: /wp-json/wp/v2/users " + "A" * 800)
            for idx in range(3)
        ]
        fake_llm = FakeCompressionLLM(
            (
                "- 保留 WordPress REST 用户枚举证据：/wp-json/wp/v2/users 返回用户列表。\n"
                "- 保留插件线索死路：候选插件没有形成可复现利用链，后续应转向认证、主题或 REST 权限边界。\n"
                "- 保留当前目标、路径和失败分支，避免下一轮重复枚举。"
            )
        )

        summary, metadata = _compress_context_middle(
            middle=middle,
            original_tokens=_count_context_tokens(middle, model="gpt-5.5"),
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
        self.assertIn(_CONTEXT_COMPRESSION_SUMMARY_MARKER, summary)
        self.assertIn("method=model", summary)
        self.assertIn("/wp-json/wp/v2/users", summary)

    def test_mid_round_context_compression_records_fallback_when_model_unavailable(self):
        middle = [
            HumanMessage(content=f"dead end {idx}: directory brute force timed out " + "B" * 300)
            for idx in range(2)
        ]
        fake_llm = FakeCompressionLLM(None, available=False)

        summary, metadata = _compress_context_middle(
            middle=middle,
            original_tokens=_count_context_tokens(middle, model="gpt-5.5"),
            mission={"target": "http://target", "goal": "capture flag"},
            llm=fake_llm,  # type: ignore[arg-type]
            compression_timeout_sec=5,
            compression_model="gpt-5.5",
        )

        self.assertEqual(metadata["method"], "fallback")
        self.assertEqual(metadata["model"], "")
        self.assertEqual(metadata["error"], "compression model unavailable")
        self.assertEqual(len(fake_llm.calls), 0)
        self.assertIn(_CONTEXT_COMPRESSION_SUMMARY_MARKER, summary)
        self.assertIn("method=fallback", summary)

    def test_mid_round_context_compression_can_force_fallback_after_memory_timeout(self):
        middle = [
            HumanMessage(content=f"old tool trace {idx}: " + "C" * 300)
            for idx in range(2)
        ]
        fake_llm = FakeCompressionLLM("model summary", available=True)

        summary, metadata = _compress_context_middle(
            middle=middle,
            original_tokens=_count_context_tokens(middle, model="gpt-5.5"),
            mission={"target": "http://target", "goal": "capture flag"},
            llm=fake_llm,  # type: ignore[arg-type]
            compression_timeout_sec=5,
            compression_model="gpt-5.5",
            force_fallback=True,
        )

        self.assertEqual(metadata["method"], "fallback")
        self.assertIn("forced fallback", metadata["error"])
        self.assertEqual(len(fake_llm.calls), 0)
        self.assertIn(_CONTEXT_COMPRESSION_SUMMARY_MARKER, summary)
        self.assertIn("method=fallback", summary)

    def test_sandbox_tool_results_are_not_outer_summarized(self):
        result = "Chunk ID: abc123\nOutput:\n" + ("A" * 2000)

        summarized = _tool_result_for_model("bash_exec", result, 10)

        self.assertEqual(summarized, result)

    def test_non_sandbox_tool_results_still_use_guidance_summary(self):
        result = "prefix-" + ("A" * 2000) + "-suffix"

        summarized = _tool_result_for_model("knowledge_search", result, 10)

        self.assertIn("Warning: truncated output", summarized)
        self.assertIn("prefix-", summarized)
        self.assertIn("-suffix", summarized)

    def test_memory_tool_view_uses_compact_result_snippets(self):
        large_result = "HEAD-" + ("A" * 5000) + "-TAIL"

        view = _tool_call_memory_view(
            [
                {
                    "tool": "bash_exec",
                    "args_summary": "curl http://target/large",
                    "result_summary": "small summary should not hide full output size",
                    "result_full": large_result,
                    "result_len": len(large_result),
                    "exit_code": 0,
                }
            ]
        )

        summary = view[0]["result_summary"]
        self.assertLessEqual(len(summary), 780)
        self.assertIn("HEAD-", summary)
        self.assertIn("-TAIL", summary)
        self.assertIn("memory view truncated", summary)

    def test_context_compression_skips_when_recent_tail_dominates_context(self):
        messages = [
            SystemMessage(content="system"),
            HumanMessage(content="volatile"),
            HumanMessage(content="small old detail"),
            AIMessage(content="", tool_calls=[]),
            ToolMessage(content="recent-large-1" + ("A" * 60000), tool_call_id="a"),
            AIMessage(content="", tool_calls=[]),
            ToolMessage(content="recent-large-2" + ("B" * 60000), tool_call_id="b"),
        ]

        plan, metadata = _plan_round_context_compression(messages=messages, threshold=20000)

        self.assertIsNone(plan)
        self.assertEqual(metadata["reason"], "insufficient_possible_savings")

    def test_context_compression_replaces_old_memory_review_without_stacking(self):
        old_review = "[MEMORY_AGENT_LONG_TERM_REVIEW]\nold\n[/MEMORY_AGENT_LONG_TERM_REVIEW]"
        messages = [
            SystemMessage(content="system"),
            HumanMessage(content="volatile"),
            HumanMessage(content="old detail " + ("A" * 20000)),
            HumanMessage(content=old_review),
            AIMessage(
                content="",
                tool_calls=[{"name": "bash_exec", "args": {"command": "id"}, "id": "a"}],
            ),
            ToolMessage(content="recent output", tool_call_id="a"),
            HumanMessage(content=old_review),
        ]
        plan, metadata = _plan_round_context_compression(messages=messages, threshold=1000)
        self.assertIsNotNone(plan, metadata)

        new_review = "[MEMORY_AGENT_LONG_TERM_REVIEW]\nnew\n[/MEMORY_AGENT_LONG_TERM_REVIEW]"
        compressed, apply_meta = _build_compressed_round_messages(
            plan=plan,
            compressed_summary=f"{_CONTEXT_COMPRESSION_SUMMARY_MARKER}\nsummary",
            memory_review=new_review,
            threshold=1000,
        )

        self.assertIsNotNone(compressed, apply_meta)
        joined = "\n".join(str(msg.content) for msg in compressed)
        self.assertEqual(joined.count("[MEMORY_AGENT_LONG_TERM_REVIEW]"), 1)
        self.assertIn("new", joined)
        self.assertNotIn("old", joined)

    def test_context_compression_keeps_recent_tool_batches_intact(self):
        messages = [
            SystemMessage(content="system"),
            HumanMessage(content="volatile"),
            HumanMessage(content="old reconnaissance " + ("A" * 20000)),
        ]
        for idx in range(5):
            messages.append(
                AIMessage(
                    content="",
                    tool_calls=[
                        {"name": "bash_exec", "args": {"command": f"cmd-{idx}-a"}, "id": f"{idx}a"},
                        {"name": "bash_exec", "args": {"command": f"cmd-{idx}-b"}, "id": f"{idx}b"},
                    ],
                )
            )
            messages.append(ToolMessage(content=f"result-{idx}-a", tool_call_id=f"{idx}a"))
            messages.append(ToolMessage(content=f"result-{idx}-b", tool_call_id=f"{idx}b"))

        plan, metadata = _plan_round_context_compression(messages=messages, threshold=1000)

        self.assertIsNotNone(plan, metadata)
        tail_text = "\n".join(str(message.content) for message in plan["tail"])
        middle_text = "\n".join(str(message.content) for message in plan["middle"])
        self.assertIn("result-1-a", tail_text)
        self.assertIn("result-4-b", tail_text)
        self.assertNotIn("result-1-a", middle_text)
        self.assertIn("result-0-a", middle_text)

    def test_context_compression_skips_xbow66_style_large_recent_output(self):
        large_tool_output = (
            "Chunk ID: abc123\n"
            "Wall time: 10.0000 seconds\n"
            "Process exited with code 0\n"
            "Original token count: 28498\n"
            "Output:\n"
            + ("X" * 119000)
        )
        messages = [
            SystemMessage(content="system"),
            HumanMessage(content="volatile"),
            HumanMessage(content=_CONTEXT_COMPRESSION_SUMMARY_MARKER + "\nprevious summary"),
            HumanMessage(content="older retained finding " + ("A" * 10000)),
            AIMessage(
                content="",
                tool_calls=[{"name": "python_exec", "args": {"code": "probe()"}, "id": "py1"}],
            ),
            ToolMessage(content=large_tool_output, tool_call_id="py1"),
        ]

        plan, metadata = _plan_round_context_compression(messages=messages, threshold=7000)

        self.assertIsNone(plan)
        self.assertEqual(metadata["reason"], "insufficient_possible_savings")
        self.assertGreater(metadata["minimum_possible_tokens"], 7000)

    def test_forced_context_compression_accepts_savings_above_threshold(self):
        old_review = "[MEMORY_AGENT_LONG_TERM_REVIEW]\nold\n[/MEMORY_AGENT_LONG_TERM_REVIEW]"
        large_tool_output = (
            "Chunk ID: abc123\n"
            "Wall time: 10.0000 seconds\n"
            "Process exited with code 0\n"
            "Output:\n"
            + ("X" * 119000)
        )
        messages = [
            SystemMessage(content="system"),
            HumanMessage(content="volatile"),
            HumanMessage(content=old_review),
            HumanMessage(content="older retained finding " + ("A" * 10000)),
            AIMessage(
                content="",
                tool_calls=[{"name": "python_exec", "args": {"code": "probe()"}, "id": "py1"}],
            ),
            ToolMessage(content=large_tool_output, tool_call_id="py1"),
            AIMessage(
                content="",
                tool_calls=[{"name": "bash_exec", "args": {"command": "id"}, "id": "sh1"}],
            ),
            ToolMessage(content="recent output", tool_call_id="sh1"),
        ]

        plan, metadata = _plan_round_context_compression(
            messages=messages,
            threshold=7000,
            force=True,
            keep_recent_tool_batches=1,
        )

        self.assertIsNotNone(plan, metadata)
        tail_text = "\n".join(str(message.content) for message in plan["tail"])
        middle_text = "\n".join(str(message.content) for message in plan["middle"])
        self.assertIn("recent output", tail_text)
        self.assertNotIn("recent output", middle_text)
        self.assertIn("Chunk ID: abc123", middle_text)

        compressed, apply_meta = _build_compressed_round_messages(
            plan=plan,
            compressed_summary=f"{_CONTEXT_COMPRESSION_SUMMARY_MARKER}\nsummary",
            memory_review="[MEMORY_AGENT_LONG_TERM_REVIEW]\nnew\n[/MEMORY_AGENT_LONG_TERM_REVIEW]",
            threshold=7000,
            force=True,
        )

        self.assertIsNotNone(compressed, apply_meta)
        self.assertTrue(apply_meta["force"])
        joined = "\n".join(str(msg.content) for msg in compressed)
        self.assertIn("new", joined)
        self.assertNotIn("old", joined)
        self.assertNotIn("Chunk ID: abc123", joined)

    def test_mid_round_context_compression_injects_long_term_memory_review(self):
        block, metadata = _memory_agent_long_term_review_block(
            {
                "summary": "WordPress target with REST user enumeration.",
                "findings": ["GET /wp-json/wp/v2/users returned wordpress_admin"],
                "leads": ["Verify authenticated route or plugin chain"],
                "dead_ends": ["Plugin candidate did not reproduce without token"],
                "credentials": ["wordpress_admin candidate"],
                "topology": ["browser -> WordPress"],
            }
        )

        self.assertTrue(metadata["injected"])
        self.assertEqual(metadata["findings"], 1)
        self.assertEqual(metadata["leads"], 1)
        self.assertIn("[MEMORY_AGENT_LONG_TERM_REVIEW]", block)
        self.assertIn("[POST_COMPRESSION_TOOL_GUARD]", block)
        self.assertIn("Do not use skill_search, knowledge_search, or web_search", block)
        self.assertIn("下一次选择工具前，必须先对照 Memory Agent 的长期记忆", block)
        self.assertIn("wordpress_admin", block)
        self.assertIn("Plugin candidate did not reproduce", block)

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

    def test_observer_injection_policy_preserves_interval_follow_up(self):
        follow_up = ObserverDecision(
            verdict="L2",
            guidance="next round must verify",
        )
        self.assertTrue(should_inject_decision(follow_up, phase="interval"))

    def test_observer_injection_policy_allows_interval_strong_evidence_signal(self):
        signal = ObserverDecision(
            verdict="WATCH",
            guidance="close the proven LFI chain",
            observer_enforcement_state="strong_evidence",
        )

        self.assertFalse(should_inject_decision(signal, phase="tool"))
        self.assertTrue(should_inject_decision(signal, phase="interval"))
        self.assertFalse(should_inject_decision(signal, phase="round"))

    def test_observer_review_due_uses_repeating_configured_interval(self):
        interval = 32
        self.assertEqual(_next_observer_review_due_after(0, interval), interval)
        self.assertEqual(_next_observer_review_due_after(interval - 1, interval), interval)
        self.assertEqual(_next_observer_review_due_after(interval, interval), interval * 2)
        self.assertEqual(_next_observer_review_due_after(interval * 2 - 1, interval), interval * 2)
        self.assertEqual(_next_observer_review_due_after(interval * 2, interval), interval * 3)

    def test_observer_review_schedule_repeats_after_each_due_point(self):
        interval = 32
        next_due = interval
        fired_at = []

        for total_calls in range(1, 97):
            if total_calls >= next_due:
                fired_at.append(total_calls)
                next_due = _next_observer_review_due_after(total_calls, interval)

        self.assertEqual(fired_at, [32, 64, 96])
        self.assertEqual(next_due, 128)

    def test_observer_runtime_records_reviewed_tool_calls_for_interval_review(self):
        store = MissionStore(":memory:")
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            settings = AgentSettings(
                workspace_root=root,
                db_path=root / "state.sqlite3",
                sandbox_container="sandbox",
                sandbox_workdir="/tmp/pikaqiu-agent-workspace",
            )
            runtime = ObserverRuntime(
                settings,
                store,
                FakeObserverLLM(),  # type: ignore[arg-type]
                ObserverAgent(),
            )
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

            runtime.review_progress(
                phase="interval",
                mission_id=mission_id,
                round_no=1,
                mission={"target": "http://x", "goal": "flag", "status": "running"},
                memory_before={},
                memory_after={},
                tool_call_log=[
                    {"tool": "bash_exec", "args_summary": "old", "result_full": "old"},
                    {"tool": "bash_exec", "args_summary": "new", "result_full": "new"},
                ],
                reviewed_tool_call_log=[
                    {"tool": "bash_exec", "args_summary": "new", "result_full": "new"},
                ],
                llm_call_count=32,
                stall_rounds=0,
                captured_flags=[],
            )

            observations = [
                json.loads(message["content"])
                for message in store.get_observer_messages(mission_id)
                if message["type"] == "observation"
            ]
            self.assertEqual(len(observations), 1)
            self.assertIn("reviewed_tool_calls", observations[0])
            self.assertNotIn("round_tool_calls", observations[0])
            self.assertEqual(observations[0]["reviewed_tool_calls"][0]["args_summary"], "new")
            self.assertEqual(store.get_observer_agent(mission_id)["status"], "waiting_next_review")

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
