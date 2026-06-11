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

    assert decision.severity == "critical"
    assert decision.state == "risky"
    assert decision.action == "steer"


def test_long_tail_exit_code_is_concrete_evidence() -> None:
    observer = ObserverAgent()
    row = {
        "tool": "bash_exec",
        "args_summary": "printf long",
        "result_summary": "plain prefix without markers",
        "result_full": "A" * 1000 + "\n[EXIT_CODE: 0]",
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
            severity="critical",
            state="risky",
            intervention="steer",
            action="steer",
            problems=["possible flag found"],
            steer_message="Submit verified flag.",
        )
    )

    assert "[RUNTIME_OBSERVER_AUDIT source=observer_agent not_user_request]" in text
    assert "[/RUNTIME_OBSERVER_AUDIT]" in text
    assert "not human guidance or a user request" in text


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
