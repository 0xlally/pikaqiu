from pathlib import Path

from pikaqiu_agent.config import AgentSettings, DEFAULT_MEMORY_COMPRESS_INTERVAL
from pikaqiu_agent.orchestrator import OrchestratorManager, _next_memory_compress_due_after
from pikaqiu_agent.storage import MissionStore


class _DummyKnowledge:
    pass


class _DummyLLM:
    def __init__(self):
        self.memory_calls = 0

    def invoke_memory(self, prompt, previous_memory):
        self.memory_calls += 1

        class _Result:
            payload = {
                "summary": "login endpoint verified",
                "findings": ["GET /login returned 200"],
                "leads": ["POST credentials to /login"],
                "dead_ends": [],
                "credentials": [],
                "topology": ["browser -> web"],
            }

        return _Result()


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


def test_memory_compression_helper_records_current_schema(tmp_path):
    manager = _manager(tmp_path)
    mission_id = manager.store.create_mission(
        name="memory",
        target="http://target",
        goal="capture flag",
        scope="http://target",
        domains=["web"],
        max_rounds=1,
        max_commands=1,
        command_timeout_sec=5,
        model="mock",
    )
    mission = manager.store.get_mission(mission_id)
    before = manager.store.get_memory(mission_id)

    after = manager._compress_memory_from_tool_calls(
        mission_id=mission_id,
        mission=mission,
        memory=before,
        round_no=1,
        tool_call_log=[
            {
                "tool": "bash_exec",
                "args_summary": "curl -i http://target/login",
                "result_summary": "HTTP/1.1 200 OK",
                "exit_code": 0,
            }
        ],
        reason="8 main LLM calls",
    )

    assert manager.llm.memory_calls == 1
    assert after == {
        "summary": "login endpoint verified",
        "findings": ["GET /login returned 200"],
        "leads": ["POST credentials to /login"],
        "dead_ends": [],
        "credentials": [],
        "topology": ["browser -> web"],
    }
    events = manager.store.get_events(mission_id)
    memory_events = [event for event in events if event["type"] == "memory_agent"]
    assert memory_events[-1]["metadata"]["reason"] == "8 main LLM calls"


def test_memory_compression_due_uses_repeating_configured_interval():
    interval = DEFAULT_MEMORY_COMPRESS_INTERVAL
    assert _next_memory_compress_due_after(0, interval) == interval
    assert _next_memory_compress_due_after(interval - 1, interval) == interval
    assert _next_memory_compress_due_after(interval, interval) == interval * 2
    assert _next_memory_compress_due_after(interval * 2 - 1, interval) == interval * 2
    assert _next_memory_compress_due_after(interval * 2, interval) == interval * 3

    assert _next_memory_compress_due_after(5, 5) == 10
    assert _next_memory_compress_due_after(10, 5) == 15
