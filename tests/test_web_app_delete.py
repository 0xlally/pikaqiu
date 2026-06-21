from pathlib import Path
from types import SimpleNamespace

from pikaqiu_agent.config import AgentSettings
from pikaqiu_agent.storage import MissionStore
from pikaqiu_agent.web_app import _cleanup_mission_workspace, create_app


def _settings(tmp_path: Path) -> AgentSettings:
    return AgentSettings(
        workspace_root=tmp_path,
        db_path=tmp_path / "state.sqlite3",
        sandbox_container="pikaqiu-sandbox-1",
        sandbox_containers=["pikaqiu-sandbox-1", "pikaqiu-sandbox-2"],
        sandbox_workdir="/tmp/pikaqiu-agent-workspace",
        llm_api_key="test-key",
    )


def test_agent_settings_default_command_timeout_matches_launch_fallback(tmp_path):
    settings = AgentSettings(
        workspace_root=tmp_path,
        db_path=tmp_path / "state.sqlite3",
        sandbox_container="pikaqiu-sandbox-1",
        sandbox_workdir="/tmp/pikaqiu-agent-workspace",
        llm_api_key="test-key",
    )

    assert settings.command_timeout_sec == 300


def test_memory_compress_interval_is_runtime_configurable(tmp_path):
    settings = _settings(tmp_path)
    store = MissionStore(":memory:")
    runtime = SimpleNamespace(
        settings=settings,
        store=store,
        orchestrator=SimpleNamespace(thread_alive=lambda _mission_id: False),
        static_root=tmp_path,
    )
    app = create_app(runtime)
    client = app.test_client()

    assert settings.memory_compress_interval == 64
    assert client.get("/api/config").get_json()["config"]["memory_compress_interval"] == 64

    response = client.post("/api/config", json={"config": {"memory_compress_interval": 12}})

    assert response.status_code == 200
    assert settings.memory_compress_interval == 12
    assert response.get_json()["config"]["memory_compress_interval"] == 12


def test_cleanup_mission_workspace_removes_uuid_prefix_in_each_container(tmp_path):
    calls = []

    class FakeExecutor:
        def __init__(self, settings, container_override=""):
            self.container = container_override

        def run(self, command, timeout_sec=None, workdir=None):
            calls.append({
                "container": self.container,
                "command": command,
                "timeout_sec": timeout_sec,
                "workdir": workdir,
            })
            return SimpleNamespace(exit_code=0, stdout="workspace_removed_or_absent\n", stderr="")

    cleanup = _cleanup_mission_workspace(
        _settings(tmp_path),
        "490cc8e4-64b4-63b0-5ece-05dfdb1185cd",
        executor_factory=FakeExecutor,
    )

    assert [row["container"] for row in cleanup] == ["pikaqiu-sandbox-1", "pikaqiu-sandbox-2"]
    assert all(row["ok"] for row in cleanup)
    assert {call["container"] for call in calls} == {"pikaqiu-sandbox-1", "pikaqiu-sandbox-2"}
    assert all(call["workdir"] == "/tmp/pikaqiu-agent-workspace" for call in calls)
    assert all("rm -rf -- 490cc8e4" in call["command"] for call in calls)
    assert all("/tmp/pikaqiu-agent-workspace/490cc8e4" == row["workdir"] for row in cleanup)


def test_cleanup_mission_workspace_rejects_unsafe_ids(tmp_path):
    calls = []

    def factory(*args, **kwargs):
        calls.append((args, kwargs))
        raise AssertionError("executor should not be created for unsafe ids")

    cleanup = _cleanup_mission_workspace(
        _settings(tmp_path),
        "../../etc/passwd",
        executor_factory=factory,
    )

    assert calls == []
    assert cleanup == [{"container": "", "workdir": "", "ok": False, "error": "unsafe mission id prefix"}]


def test_delete_mission_cleans_workspace_before_removing_record(tmp_path, monkeypatch):
    settings = _settings(tmp_path)
    store = MissionStore(":memory:")
    mission_id = store.create_mission(
        name="old task",
        target="http://target",
        goal="recover flag",
        scope="sandbox",
        domains=[],
        max_rounds=1,
        max_commands=1,
        command_timeout_sec=300,
        model="mock",
    )
    store.update_mission_status(mission_id, "stopped")

    cleaned = []

    def fake_cleanup(cleanup_settings, cleanup_mission_id):
        cleaned.append((cleanup_settings, cleanup_mission_id, bool(store.get_mission(cleanup_mission_id))))
        return [{"container": "pikaqiu-sandbox-1", "workdir": "/tmp/pikaqiu-agent-workspace/test", "ok": True}]

    monkeypatch.setattr("pikaqiu_agent.web_app._cleanup_mission_workspace", fake_cleanup)

    runtime = SimpleNamespace(
        settings=settings,
        store=store,
        orchestrator=SimpleNamespace(thread_alive=lambda _mission_id: False),
        static_root=tmp_path,
    )
    app = create_app(runtime)

    response = app.test_client().delete(f"/api/missions/{mission_id}")

    assert response.status_code == 200
    assert response.get_json()["workspace_cleanup"][0]["ok"] is True
    assert cleaned == [(settings, mission_id, True)]
    assert store.get_mission(mission_id) is None
