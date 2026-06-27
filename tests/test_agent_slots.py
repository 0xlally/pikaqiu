from pathlib import Path
import time

from pikaqiu_agent.config import (
    AgentSettings,
    DEFAULT_COMPRESSION_REASONING_EFFORT,
    DEFAULT_COMPRESSION_TIMEOUT_SEC,
    DEFAULT_MEMORY_COMPRESS_INTERVAL,
)
from pikaqiu_agent.llm_client import LLMResult
from pikaqiu_agent.llm_client import LLMClient
from pikaqiu_agent.orchestrator import (
    OrchestratorManager,
    _memory_compression_timeout_sec,
    _next_memory_compress_due_after,
)
from pikaqiu_agent.storage import MissionStore


class _DummyKnowledge:
    pass


class _DummyLLM:
    def __init__(self):
        self.memory_calls = 0
        self.memory_compression_calls = 0

    @property
    def has_compression_model(self) -> bool:
        return True

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

    def invoke_memory_compression(self, prompt, previous_memory):
        self.memory_compression_calls += 1

        class _Result:
            payload = {
                "summary": "compressed by dedicated model",
                "findings": ["GET /page returned 200"],
                "leads": ["test reflected input"],
                "dead_ends": [],
                "credentials": [],
                "topology": [],
            }

        return _Result()


class _LooseCompressionLLM(_DummyLLM):
    def invoke_memory_compression(self, prompt, previous_memory):
        self.memory_compression_calls += 1
        return LLMClient._ensure_memory_payload(
            self,
            LLMResult(
                raw_text="只返回自然语言摘要也应被规范化为 memory payload",
                payload={},
                used_mock=False,
            ),
            previous_memory,
        )


class _SlowMemoryLLM:
    def __init__(self, delay_sec: float = 0.1) -> None:
        self.delay_sec = delay_sec
        self.memory_calls = 0

    @property
    def has_compression_model(self) -> bool:
        return True

    def invoke_memory(self, prompt, previous_memory):
        self.memory_calls += 1
        time.sleep(self.delay_sec)

        class _Result:
            payload = {
                "summary": "late memory should not be stored after timeout",
                "findings": ["late"],
                "leads": [],
                "dead_ends": [],
                "credentials": [],
                "topology": [],
            }

        return _Result()

    def invoke_memory_compression(self, prompt, previous_memory):
        time.sleep(self.delay_sec)

        class _Result:
            payload = {
                "summary": "late compression should not be stored after timeout",
                "findings": ["late"],
                "leads": [],
                "dead_ends": [],
                "credentials": [],
                "topology": [],
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


def test_memory_compression_helper_records_current_schema_from_compression_model(tmp_path):
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

    after, succeeded = manager._compress_memory_from_tool_calls(
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

    assert succeeded is True
    assert manager.llm.memory_compression_calls == 1
    assert manager.llm.memory_calls == 0
    assert after == {
        "summary": "compressed by dedicated model",
        "findings": ["GET /page returned 200"],
        "leads": ["test reflected input"],
        "dead_ends": [],
        "credentials": [],
        "topology": [],
    }
    events = manager.store.get_events(mission_id)
    memory_events = [event for event in events if event["type"] == "memory_agent"]
    assert memory_events[-1]["metadata"]["reason"] == "8 main LLM calls"


def test_memory_compression_prefers_dedicated_compression_model(tmp_path):
    manager = _manager(tmp_path)
    mission_id = manager.store.create_mission(
        name="memory-fast",
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

    after, succeeded = manager._compress_memory_from_tool_calls(
        mission_id=mission_id,
        mission=mission,
        memory=before,
        round_no=1,
        tool_call_log=[
            {
                "tool": "bash_exec",
                "args_summary": "curl -i http://target/page",
                "result_summary": "HTTP/1.1 200 OK",
                "exit_code": 0,
            }
        ],
        reason="8 main LLM calls",
    )

    assert succeeded is True
    assert manager.llm.memory_compression_calls == 1
    assert manager.llm.memory_calls == 0
    assert after["summary"] == "compressed by dedicated model"
    memory_events = [event for event in manager.store.get_events(mission_id) if event["type"] == "memory_agent"]
    assert "method=compression_model" in memory_events[-1]["content"]


def test_memory_rebase_uses_unified_memory_agent_compression_path(tmp_path):
    manager = _manager(tmp_path)
    mission_id = manager.store.create_mission(
        name="memory-rebase",
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
    before = {
        "summary": "stalled on weak login bypass guesses",
        "findings": ["GET /search.php returned 200"],
        "leads": ["try another login bypass"],
        "dead_ends": [],
        "credentials": [],
        "topology": [],
    }

    after, succeeded = manager._compress_memory_from_tool_calls(
        mission_id=mission_id,
        mission=mission,
        memory=before,
        round_no=3,
        tool_call_log=[],
        reason="stall_rounds=2",
        mode="stall_rebase",
        stall_rounds=2,
    )

    assert succeeded is True
    assert manager.llm.memory_compression_calls == 1
    assert manager.llm.memory_calls == 0
    assert after["summary"] == "compressed by dedicated model"
    memory_events = [event for event in manager.store.get_events(mission_id) if event["type"] == "memory_agent"]
    assert memory_events[-1]["title"] == "Memory rebase (stall_rounds=2)"
    assert memory_events[-1]["metadata"]["mode"] == "stall_rebase"
    assert memory_events[-1]["metadata"]["stall_rounds"] == 2


def test_memory_compression_accepts_loose_model_text(tmp_path):
    manager = OrchestratorManager(
        settings=_settings(tmp_path),
        store=MissionStore(":memory:"),
        knowledge=_DummyKnowledge(),
        sandbox=_DummySandbox(),
        llm=_LooseCompressionLLM(),
    )
    mission_id = manager.store.create_mission(
        name="memory-loose",
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

    after, succeeded = manager._compress_memory_from_tool_calls(
        mission_id=mission_id,
        mission=mission,
        memory=before,
        round_no=1,
        tool_call_log=[
            {
                "tool": "bash_exec",
                "args_summary": "curl -i http://target/page",
                "result_summary": "HTTP/1.1 200 OK",
                "exit_code": 0,
            }
        ],
        reason="8 main LLM calls",
    )

    assert succeeded is True
    assert after["summary"] == "只返回自然语言摘要也应被规范化为 memory payload"


def test_memory_compression_timeout_is_visible_and_not_success(tmp_path):
    settings = _settings(tmp_path)
    settings.llm_timeout_sec = 1
    settings.compression_timeout_sec = 1
    manager = OrchestratorManager(
        settings=settings,
        store=MissionStore(":memory:"),
        knowledge=_DummyKnowledge(),
        sandbox=_DummySandbox(),
        llm=_SlowMemoryLLM(delay_sec=2.0),
    )
    mission_id = manager.store.create_mission(
        name="memory-timeout",
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

    after, succeeded = manager._compress_memory_from_tool_calls(
        mission_id=mission_id,
        mission=mission,
        memory=before,
        round_no=1,
        tool_call_log=[
            {
                "tool": "bash_exec",
                "args_summary": "curl -i http://target/",
                "result_summary": "HTTP/1.1 200 OK\n<title>Target</title>",
                "exit_code": 0,
            }
        ],
        reason="8 main LLM calls",
    )

    assert succeeded is False
    assert after == before
    events = manager.store.get_events(mission_id)
    memory_events = [event for event in events if event["type"] == "memory_agent"]
    assert memory_events[-1]["title"] == "Memory compression failed (8 main LLM calls)"
    assert memory_events[-1]["exit_code"] == 1
    assert "timed out after 1s" in memory_events[-1]["content"]


def test_memory_compression_due_uses_repeating_configured_interval():
    interval = DEFAULT_MEMORY_COMPRESS_INTERVAL
    assert _next_memory_compress_due_after(0, interval) == interval
    assert _next_memory_compress_due_after(interval - 1, interval) == interval
    assert _next_memory_compress_due_after(interval, interval) == interval * 2
    assert _next_memory_compress_due_after(interval * 2 - 1, interval) == interval * 2
    assert _next_memory_compress_due_after(interval * 2, interval) == interval * 3

    assert _next_memory_compress_due_after(5, 5) == 10
    assert _next_memory_compress_due_after(10, 5) == 15


def test_memory_compression_timeout_respects_compression_timeout(tmp_path):
    settings = _settings(tmp_path)
    settings.llm_timeout_sec = 240
    settings.compression_timeout_sec = 180

    assert _memory_compression_timeout_sec(settings) == 180

    settings.llm_timeout_sec = 30
    assert _memory_compression_timeout_sec(settings) == 30


def test_compression_defaults_are_fast_enough_for_memory_rewrite():
    assert DEFAULT_COMPRESSION_REASONING_EFFORT == "low"
    assert DEFAULT_COMPRESSION_TIMEOUT_SEC == 180
