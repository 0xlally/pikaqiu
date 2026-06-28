from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from pikaqiu_agent.observer import ObserverAgent, ObserverDecision
from pikaqiu_agent.skill_loader import SkillLoader


def test_observer_detects_flag_in_full_tail() -> None:
    observer = ObserverAgent()
    long_result = "A" * 2000 + "\nflag{tail_flag_value}\n"

    decision = observer.observe_tool_call(
        mission={"target": "http://target.local"},
        tool_call_log=[
            {
                "tool": "bash_exec",
                "args_summary": "cat /flag",
                "result_summary": "A" * 500,
                "result_full": long_result,
            }
        ],
        memory={},
        captured_flags=[],
    ).normalised()

    assert decision.verdict == "L4"
    assert decision.interrupts is True
    assert "flag{tail_flag_value}" in " ".join(decision.evidence)


def test_observer_ignores_fake_flag_prefixes() -> None:
    observer = ObserverAgent()

    decision = observer.observe_tool_call(
        mission={"target": "http://target.local"},
        tool_call_log=[
            {
                "tool": "bash_exec",
                "args_summary": "cat /flag",
                "result_full": "dasctf{fake_flag_value}\nfLaG{fake_flag_value}\n",
            }
        ],
        memory={},
        captured_flags=[],
    ).normalised()

    assert decision.verdict != "L4"
    assert "fake_flag_value" not in " ".join(decision.evidence)


def test_long_tail_exit_code_is_concrete_evidence() -> None:
    observer = ObserverAgent()
    row = {
        "tool": "bash_exec",
        "args_summary": "printf long",
        "result_summary": "plain prefix without markers",
        "result_full": "A" * 1000 + "\n[EXIT_CODE: 0]",
    }

    assert observer._is_low_evidence_call(row) is False


def test_codex_exit_code_marker_is_concrete_evidence() -> None:
    observer = ObserverAgent()
    row = {
        "tool": "bash_exec",
        "args_summary": "printf long",
        "result_summary": "plain prefix without markers",
        "result_full": "Chunk ID: abc123\nWall time: 0.1000 seconds\nProcess exited with code 0\nOutput:\nok",
    }

    assert observer._is_low_evidence_call(row) is False


def test_short_success_still_low_evidence() -> None:
    observer = ObserverAgent()
    row = {
        "tool": "bash_exec",
        "args_summary": "some probe",
        "result_summary": "success",
    }

    assert observer._is_low_evidence_call(row) is True


def test_observer_injection_is_runtime_telemetry() -> None:
    text = ObserverAgent().format_injection(
        ObserverDecision(
            verdict="L4",
            evidence=["possible flag found"],
            guidance="Submit verified flag.",
        )
    )

    assert "[RUNTIME_OBSERVER_AUDIT source=observer_agent not_user_request]" in text
    assert "[/RUNTIME_OBSERVER_AUDIT]" in text
    assert "不是人工指导或用户请求" in text
    assert "verdict=L4" in text


def test_watch_verdict_is_non_interrupting_observation() -> None:
    decision = ObserverDecision(
        verdict="WATCH",
        guidance="watch for context drift",
    ).normalised()

    assert decision.verdict == "WATCH"
    assert decision.interrupts is False


def test_observer_rule_classifies_environment_failure_loop() -> None:
    observer = ObserverAgent()
    decision = observer.observe_tool_call(
        mission={"target": "http://target.local"},
        tool_call_log=[
            {"tool": "bash_exec", "args_summary": "ffuf 1", "result_summary": "timeout"},
            {"tool": "bash_exec", "args_summary": "ffuf 2", "result_summary": "connection refused"},
            {"tool": "bash_exec", "args_summary": "ffuf 3", "result_summary": "command not found"},
        ],
        memory={},
        captured_flags=[],
    ).normalised()

    assert decision.verdict == "ENV"
    assert decision.interrupts is True


def test_round_review_emits_strong_evidence_next_step_for_lfi() -> None:
    observer = ObserverAgent()

    decision = observer.review_round(
        mission={"target": "http://target.local"},
        memory_before={"findings": [], "leads": [], "dead_ends": []},
        memory_after={"findings": ["filename parameter reads files"], "leads": [], "dead_ends": []},
        tool_call_log=[
            {
                "tool": "bash_exec",
                "args_summary": "curl http://target.local/read?file=../../etc/passwd",
                "result_full": "HTTP/1.1 200 OK\nroot:x:0:0:root:/root:/bin/bash\n",
            }
        ],
        llm_call_count=1,
        stall_rounds=0,
        captured_flags=[],
    ).normalised()

    assert decision.verdict == "WATCH"
    assert decision.observer_enforcement_state == "strong_evidence"
    assert "mountinfo" in decision.next_verification
    assert decision.memory_patch["leads"]


def test_round_review_emits_strong_evidence_for_sqli_error() -> None:
    observer = ObserverAgent()

    decision = observer.review_round(
        mission={"target": "http://target.local"},
        memory_before={"findings": [], "leads": [], "dead_ends": []},
        memory_after={"findings": [], "leads": [], "dead_ends": []},
        tool_call_log=[
            {
                "tool": "bash_exec",
                "args_summary": "curl http://target.local/item?id=1'",
                "result_full": "HTTP/1.1 500\nYou have an error in your SQL syntax near ''' at line 1",
            }
        ],
        llm_call_count=1,
        stall_rounds=0,
        captured_flags=[],
    ).normalised()

    assert decision.observer_enforcement_state == "strong_evidence"
    assert "SQLi" in decision.guidance
    assert "[强证据:sqli_error_or_union]" in decision.memory_patch["leads"][0]


def test_round_review_emits_strong_evidence_for_ssrf_internal_response() -> None:
    observer = ObserverAgent()

    decision = observer.review_round(
        mission={"target": "http://target.local"},
        memory_before={"findings": [], "leads": [], "dead_ends": []},
        memory_after={"findings": [], "leads": [], "dead_ends": []},
        tool_call_log=[
            {
                "tool": "bash_exec",
                "args_summary": "curl 'http://target.local/fetch?url=http://169.254.169.254/latest/meta-data/'",
                "result_full": "HTTP/1.1 200 OK\ninstance-id\ni-123456\nhostname\n",
            }
        ],
        llm_call_count=1,
        stall_rounds=0,
        captured_flags=[],
    ).normalised()

    assert decision.observer_enforcement_state == "strong_evidence"
    assert "SSRF" in decision.guidance
    assert "[强证据:ssrf_internal]" in decision.memory_patch["leads"][0]


def test_round_review_emits_strong_evidence_for_sensitive_config() -> None:
    observer = ObserverAgent()

    decision = observer.review_round(
        mission={"target": "http://target.local"},
        memory_before={"findings": [], "leads": [], "dead_ends": []},
        memory_after={"findings": [], "leads": [], "dead_ends": []},
        tool_call_log=[
            {
                "tool": "bash_exec",
                "args_summary": "curl http://target.local/.env",
                "result_full": "HTTP/1.1 200 OK\nAPP_KEY=base64:abc\nDB_PASSWORD='secret123'",
            }
        ],
        llm_call_count=1,
        stall_rounds=0,
        captured_flags=[],
    ).normalised()

    assert decision.observer_enforcement_state == "strong_evidence"
    assert "凭据" in decision.guidance
    assert "[强证据:sensitive_config]" in decision.memory_patch["leads"][0]


def test_skill_reference_requires_selected_or_activated_skill() -> None:
    try:
        from pikaqiu_agent.tools import create_skill_reference_tool
    except ModuleNotFoundError as exc:
        if exc.name == "langchain_core":
            raise unittest.SkipTest("langchain_core is not installed") from exc
        raise

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        skills_root = root / "skills"
        skill_dir = skills_root / "demo-skill"
        refs_dir = skill_dir / "references"
        refs_dir.mkdir(parents=True)
        (skill_dir / "SKILL.md").write_text(
            "---\nid: demo-skill\nname: Demo Skill\n---\nUse demo skill.",
            encoding="utf-8",
        )
        (refs_dir / "note.md").write_text("reference body", encoding="utf-8")
        loader = SkillLoader(root, "skills")
        loader.refresh()

        tool = create_skill_reference_tool(
            loader,
            mission={"id": "m1", "skills": [], "activated_skills": []},
        )
        denied = json.loads(tool.invoke({"skill_id": "demo-skill", "path": "references/note.md"}))

        assert denied["ok"] is False
        assert "selected or activated" in denied["error"]

        tool = create_skill_reference_tool(
            loader,
            mission={"id": "m1", "skills": ["demo-skill"], "activated_skills": []},
        )
        allowed = tool.invoke({"skill_id": "demo-skill", "path": "references/note.md"})

        assert allowed == "reference body"
