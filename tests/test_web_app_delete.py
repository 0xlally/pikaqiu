from pathlib import Path
from types import SimpleNamespace

from pikaqiu_agent.config import AgentSettings, DEFAULT_CONTEXT_COMPRESS_THRESHOLD, load_settings
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


def test_agent_settings_default_context_compress_threshold_matches_tool_budget(tmp_path):
    settings = _settings(tmp_path)

    assert settings.context_compress_threshold == DEFAULT_CONTEXT_COMPRESS_THRESHOLD
    assert settings.context_compress_threshold == 320000


def test_agent_settings_clamps_command_timeout_to_outer_limit(tmp_path):
    settings = _settings(tmp_path)

    assert settings.update({"command_timeout_sec": 999}) == {}

    assert settings.command_timeout_sec == 300
    assert settings.get_mission_params({"command_timeout_sec": 999})["command_timeout_sec"] == 300


def test_agent_settings_normalizes_max_output_tokens_runtime_values(tmp_path):
    settings = _settings(tmp_path)

    assert settings.update({"max_output_tokens": -5}) == {}
    assert settings.max_output_tokens == 0

    errors = settings.update({"max_output_tokens": "not-an-int"})

    assert "max_output_tokens" in errors
    assert settings.max_output_tokens == 0


def test_agent_settings_rejects_invalid_runtime_context_compress_threshold(tmp_path):
    settings = _settings(tmp_path)

    assert settings.update({"context_compress_threshold": 123456}) == {}
    assert settings.context_compress_threshold == 123456

    errors = settings.update({"context_compress_threshold": -1})

    assert "context_compress_threshold" in errors
    assert settings.context_compress_threshold == 123456


def test_load_settings_accepts_legacy_stdout_limit(tmp_path, monkeypatch):
    monkeypatch.delenv("PIKAQIU_MAX_OUTPUT_TOKENS", raising=False)
    monkeypatch.delenv("PIKAQIU_STDOUT_LIMIT", raising=False)
    (tmp_path / "config.yml").write_text(
        """
agent_defaults:
  stdout_limit: 1234
""",
        encoding="utf-8",
    )

    settings = load_settings(tmp_path)

    assert settings.max_output_tokens == 1234


def test_load_settings_prefers_new_max_output_tokens_env_over_legacy(tmp_path, monkeypatch):
    monkeypatch.setenv("PIKAQIU_MAX_OUTPUT_TOKENS", "2222")
    monkeypatch.setenv("PIKAQIU_STDOUT_LIMIT", "1111")
    (tmp_path / "config.yml").write_text(
        """
agent_defaults:
  max_output_tokens: 3333
""",
        encoding="utf-8",
    )

    settings = load_settings(tmp_path)

    assert settings.max_output_tokens == 2222


def test_load_settings_clamps_negative_max_output_tokens(tmp_path, monkeypatch):
    monkeypatch.delenv("PIKAQIU_MAX_OUTPUT_TOKENS", raising=False)
    monkeypatch.delenv("PIKAQIU_STDOUT_LIMIT", raising=False)
    (tmp_path / "config.yml").write_text(
        """
agent_defaults:
  max_output_tokens: -5
""",
        encoding="utf-8",
    )

    settings = load_settings(tmp_path)

    assert settings.max_output_tokens == 0


def test_load_settings_uses_default_for_negative_context_compress_threshold(tmp_path, monkeypatch):
    monkeypatch.delenv("PIKAQIU_MAX_OUTPUT_TOKENS", raising=False)
    (tmp_path / "config.yml").write_text(
        """
agent_defaults:
  context_compress_threshold: -5
""",
        encoding="utf-8",
    )

    settings = load_settings(tmp_path)

    assert settings.context_compress_threshold == DEFAULT_CONTEXT_COMPRESS_THRESHOLD


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

    assert settings.memory_compress_interval == 8
    assert client.get("/api/config").get_json()["config"]["memory_compress_interval"] == 8

    response = client.post("/api/config", json={"config": {"memory_compress_interval": 12}})

    assert response.status_code == 200
    assert settings.memory_compress_interval == 12
    assert response.get_json()["config"]["memory_compress_interval"] == 12


def test_create_mission_clamps_command_timeout_to_outer_limit(tmp_path):
    settings = _settings(tmp_path)
    store = MissionStore(":memory:")
    captured = {}

    class FakeOrchestrator:
        def agent_slots(self):
            return []

        def start_mission(self, **kwargs):
            captured.update(kwargs)
            return "mission-1"

    runtime = SimpleNamespace(
        settings=settings,
        store=store,
        orchestrator=FakeOrchestrator(),
        skills=SimpleNamespace(refresh=lambda: None, resolve=lambda skill_ids: (skill_ids, [])),
        static_root=tmp_path,
    )
    app = create_app(runtime)

    response = app.test_client().post(
        "/api/missions",
        json={
            "name": "timeout cap",
            "target": "http://target",
            "goal": "recover flag",
            "command_timeout_sec": 999,
        },
    )

    assert response.status_code == 201
    assert captured["command_timeout_sec"] == 300


def test_compression_defaults_use_model_based_compression(tmp_path, monkeypatch):
    monkeypatch.delenv("PIKAQIU_COMPRESSION_MODEL", raising=False)
    monkeypatch.delenv("PIKAQIU_COMPRESSION_REASONING_EFFORT", raising=False)
    monkeypatch.delenv("PIKAQIU_MEMORY_COMPRESS_INTERVAL", raising=False)
    (tmp_path / "config.yml").write_text(
        """
model_pool:
  - id: main
    base_url: "https://example.test/v1"
    api_key: "test-key"
    model: "gpt-5.5"
compression:
  model: ""
  reasoning_effort: ""
agent_defaults:
  memory_compress_interval: 8
""",
        encoding="utf-8",
    )

    settings = load_settings(tmp_path)

    assert settings.compression_model == "gpt-5.5"
    assert settings.compression_reasoning_effort == "low"
    assert settings.memory_compress_interval == 8
    assert settings.get_compression_model() == "gpt-5.5"
    assert settings.get_compression_reasoning_effort() == "low"


def test_compression_reasoning_effort_does_not_inherit_heavy_env(tmp_path, monkeypatch):
    monkeypatch.setenv("PIKAQIU_COMPRESSION_REASONING_EFFORT", "xhigh")
    (tmp_path / "config.yml").write_text(
        """
model_pool:
  - id: main
    api_key: "test-key"
    model: "gpt-5.5"
    reasoning_effort: "xhigh"
compression:
  model: "gpt-5.5"
  reasoning_effort: "xhigh"
""",
        encoding="utf-8",
    )

    settings = load_settings(tmp_path)

    assert settings.llm_reasoning_effort == "xhigh"
    assert settings.compression_reasoning_effort == "low"
    assert settings.get_compression_reasoning_effort() == "low"
    assert settings.to_dict()["effective_compression_reasoning_effort"] == "low"


def test_runtime_compression_reasoning_effort_rejects_heavy_values(tmp_path):
    settings = _settings(tmp_path)
    store = MissionStore(":memory:")
    runtime = SimpleNamespace(
        settings=settings,
        store=store,
        orchestrator=SimpleNamespace(
            thread_alive=lambda _mission_id: False,
            observer_runtime=SimpleNamespace(llm=None),
        ),
        static_root=tmp_path,
    )
    app = create_app(runtime)
    client = app.test_client()

    response = client.post("/api/config", json={"config": {"compression_reasoning_effort": "xhigh"}})

    assert response.status_code == 200
    config = response.get_json()["config"]
    assert settings.compression_reasoning_effort == "low"
    assert config["compression_reasoning_effort"] == "low"
    assert config["effective_compression_reasoning_effort"] == "low"


def test_runtime_config_ignores_masked_secret_roundtrip(tmp_path):
    settings = _settings(tmp_path)
    settings.compression_api_key = "real-compression-key"
    masked = settings.to_dict(mask_secrets=True)["compression_api_key"]

    errors = settings.update({"compression_api_key": masked})

    assert errors == {}
    assert settings.compression_api_key == "real-compression-key"


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
