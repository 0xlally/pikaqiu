from pathlib import Path

from pikaqiu_agent.config import AgentSettings
from pikaqiu_agent.orchestrator import OrchestratorManager
from pikaqiu_agent.storage import MissionStore


class _DummyKnowledge:
    pass


class _DummyLLM:
    pass


class _DummySandbox:
    pass


def _settings(tmp_path: Path) -> AgentSettings:
    return AgentSettings(
        workspace_root=tmp_path,
        db_path=tmp_path / "state.sqlite3",
        sandbox_container="pikaqiu-sandbox-1",
        sandbox_containers=[f"pikaqiu-sandbox-{idx}" for idx in range(1, 6)],
        sandbox_workdir="/tmp/pikaqiu-agent-workspace",
        llm_api_key="test-key",
    )


def _manager(tmp_path: Path) -> OrchestratorManager:
    return OrchestratorManager(
        settings=_settings(tmp_path),
        store=MissionStore(":memory:"),
        knowledge=_DummyKnowledge(),
        sandbox=_DummySandbox(),
        llm=_DummyLLM(),
    )


def test_agent_pool_uses_five_dedicated_containers(tmp_path):
    manager = _manager(tmp_path)

    allocated = [manager._allocate_sandbox(f"mission-{idx}") for idx in range(1, 6)]

    assert [executor._container for executor in allocated] == [
        "pikaqiu-sandbox-1",
        "pikaqiu-sandbox-2",
        "pikaqiu-sandbox-3",
        "pikaqiu-sandbox-4",
        "pikaqiu-sandbox-5",
    ]


def test_agent_pool_rejects_sixth_mission_instead_of_sharing(tmp_path):
    manager = _manager(tmp_path)
    for idx in range(1, 6):
        manager._allocate_sandbox(f"mission-{idx}")

    try:
        manager._allocate_sandbox("mission-6")
    except RuntimeError as exc:
        assert str(exc) == "all agent slots are busy"
    else:
        raise AssertionError("sixth mission unexpectedly received a sandbox")


def test_agent_slots_report_idle_when_flag_is_captured(tmp_path):
    manager = _manager(tmp_path)
    mission_id = manager.store.create_mission(
        name="flagged",
        target="http://target",
        goal="capture flag",
        scope="http://target",
        domains=["web"],
        max_rounds=1,
        max_commands=1,
        command_timeout_sec=5,
        model="mock",
        expected_flags=1,
    )
    manager._allocate_sandbox(mission_id)
    manager.store.add_event(
        mission_id=mission_id,
        round_no=1,
        event_type="flag",
        title="Flag captured",
        content="flag{abc123} (1/1)",
    )

    first = manager.agent_slots()[0]

    assert first["status"] == "idle"
    assert first["status_reason"] == "flag_captured"
    assert first["captured_flag_count"] == 1
