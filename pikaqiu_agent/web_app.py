from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from flask import Flask, jsonify, request, send_from_directory

from pikaqiu_agent.config import AgentSettings, load_settings
from pikaqiu_agent.knowledge import KnowledgeIndexer
from pikaqiu_agent.llm_client import LLMClient
from pikaqiu_agent.orchestrator import OrchestratorManager
from pikaqiu_agent.sandbox import SandboxExecutor
from pikaqiu_agent.storage import MissionStore

logger = logging.getLogger(__name__)


def _json_error(message: str, status: int):
    return jsonify({"error": message}), status


def _clamp_int(value: Any, default: int, *, minimum: int, maximum: int) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        parsed = default
    return max(minimum, min(parsed, maximum))


class AppRuntime:
    def __init__(self, settings: AgentSettings) -> None:
        self.settings = settings
        self.store = MissionStore(settings.db_path)
        self.store.reset_stale_missions()
        self.knowledge = KnowledgeIndexer(settings.workspace_root, self.store, settings.knowledge_dir)
        self.sandbox = SandboxExecutor(settings)
        self.llm = LLMClient(settings)
        self.orchestrator = OrchestratorManager(
            settings,
            self.store,
            self.knowledge,
            self.sandbox,
            self.llm,
        )
        self.static_root = Path(__file__).resolve().parent / "static"


def create_app(runtime: AppRuntime | None = None) -> Flask:
    """Create and configure the Flask application."""
    if runtime is None:
        settings = load_settings()
        runtime = AppRuntime(settings)
        runtime.knowledge.ensure_ready()

    app = Flask(
        __name__,
        static_folder=str(runtime.static_root),
        static_url_path="",
    )
    app.config["rt"] = runtime

    def rt() -> AppRuntime:
        return app.config["rt"]

    # ── Static / SPA ──────────────────────────────────────────

    @app.route("/")
    def index():
        return send_from_directory(str(runtime.static_root), "index.html")

    @app.route("/settings.html")
    def settings_page():
        return send_from_directory(str(runtime.static_root), "settings.html")

    # ── Bootstrap ─────────────────────────────────────────────

    @app.route("/api/bootstrap")
    def api_bootstrap():
        s = rt().settings
        return jsonify({
            "llm_mode": "mock" if s.use_mock_llm else "direct-api",
            "model": s.llm_model,
            "sandbox_container": s.sandbox_container,
            "sandbox_workdir": s.sandbox_workdir,
            "knowledge": rt().store.get_knowledge_stats(),
            "defaults": {
                "max_rounds": s.initial_rounds,
                "max_commands": s.initial_commands,
                "command_timeout_sec": s.command_timeout_sec,
            },
        })

    # ── Config ────────────────────────────────────────────────

    @app.route("/api/config", methods=["GET"])
    def api_config_get():
        return jsonify({"config": rt().settings.to_dict(mask_secrets=True)})

    @app.route("/api/config", methods=["POST"])
    def api_config_post():
        changes = request.get_json(silent=True) or {}
        changes = changes.get("config", changes)
        if not isinstance(changes, dict) or not changes:
            return _json_error("provide 'config' dict with fields to update", 400)
        errors = rt().settings.update(changes)
        # Rebuild LLM client if relevant fields changed
        llm_fields = {"llm_base_url", "llm_api_key", "llm_model", "llm_timeout_sec",
                      "advisor_base_url", "advisor_api_key", "advisor_model"}
        if llm_fields & set(changes.keys()):
            rt().llm = LLMClient(rt().settings)
        resp: dict[str, Any] = {"ok": True, "config": rt().settings.to_dict(mask_secrets=True)}
        if errors:
            resp["errors"] = errors
        return jsonify(resp)

    # ── Missions ──────────────────────────────────────────────

    @app.route("/api/missions", methods=["GET"])
    def api_missions_list():
        return jsonify({"missions": rt().store.list_missions()})

    @app.route("/api/missions", methods=["POST"])
    def api_missions_create():
        payload = request.get_json(silent=True) or {}
        s = rt().settings
        max_rounds = _clamp_int(payload.get("max_rounds"), s.initial_rounds, minimum=1, maximum=s.max_rounds)
        max_commands = _clamp_int(payload.get("max_commands"), s.initial_commands, minimum=1, maximum=s.max_commands)
        command_timeout = _clamp_int(payload.get("command_timeout_sec"), s.command_timeout_sec, minimum=5, maximum=600)
        expected_flags = _clamp_int(payload.get("expected_flags"), 1, minimum=1, maximum=50)
        mission_id = rt().orchestrator.start_mission(
            name=str(payload.get("name") or "未命名任务"),
            target=str(payload.get("target") or "").strip(),
            goal=str(payload.get("goal") or "").strip(),
            scope=str(payload.get("target") or "").strip(),
            domains=[str(item) for item in payload.get("domains", ["web"]) if str(item)],
            max_rounds=max_rounds,
            max_commands=max_commands,
            command_timeout_sec=command_timeout,
            expected_flags=expected_flags,
        )
        return jsonify({"mission_id": mission_id}), 201

    @app.route("/api/missions/<mission_id>")
    def api_mission_detail(mission_id: str):
        mission = rt().store.get_mission(mission_id)
        if not mission:
            return _json_error("mission not found", 404)
        return jsonify({
            "mission": mission,
            "memory": rt().store.get_memory(mission_id),
            "rounds": rt().store.get_rounds(mission_id),
            "events": rt().store.get_events(mission_id),
            "thread_alive": rt().orchestrator.thread_alive(mission_id),
        })

    @app.route("/api/missions/<mission_id>/stop", methods=["POST"])
    def api_mission_stop(mission_id: str):
        rt().orchestrator.stop_mission(mission_id)
        return jsonify({"ok": True})

    @app.route("/api/missions/<mission_id>", methods=["DELETE"])
    def api_mission_delete(mission_id: str):
        mission = rt().store.get_mission(mission_id)
        if not mission:
            return _json_error("mission not found", 404)
        if mission["status"] in {"queued", "running"} or rt().orchestrator.thread_alive(mission_id):
            return _json_error("任务仍在执行中，请先停止任务再删除记录", 409)
        deleted = rt().store.delete_mission(mission_id)
        if not deleted:
            return _json_error("mission not found", 404)
        return jsonify({"ok": True, "deleted_id": mission_id})

    # ── Knowledge ─────────────────────────────────────────────

    @app.route("/api/knowledge/search")
    def api_knowledge_search():
        q = request.args.get("q", "")
        domains = request.args.getlist("domain")
        limit = _clamp_int(request.args.get("limit", "8"), 8, minimum=1, maximum=50)
        return jsonify({
            "items": rt().store.search_knowledge(q, domains=domains or None, limit=limit)
        })

    @app.route("/api/knowledge/cve-search")
    def api_cve_search():
        product = request.args.get("product", "")
        version = request.args.get("version", "")
        cve_id = request.args.get("cve_id", "")
        vuln_type = request.args.get("vuln_type", "")
        keyword = request.args.get("keyword", "")
        limit = _clamp_int(request.args.get("limit", "10"), 10, minimum=1, maximum=100)
        return jsonify({
            "items": rt().store.search_cve_poc(
                product=product, version=version, cve_id=cve_id,
                vuln_type=vuln_type, keyword=keyword, limit=limit,
            ),
            "stats": rt().store.get_cve_index_stats(),
        })

    @app.route("/api/knowledge/doc")
    def api_knowledge_doc():
        raw_id = request.args.get("id", "").strip()
        if not raw_id.isdigit():
            return _json_error("invalid knowledge doc id", 400)
        doc = rt().store.get_knowledge_doc(int(raw_id))
        if not doc:
            return _json_error("knowledge doc not found", 404)
        full_body = rt().knowledge.read_doc_content(
            str(doc["source"]), str(doc["path"]), fallback=str(doc["body"]),
        )
        return jsonify({
            "item": {**doc, "body": full_body, "is_markdown": str(doc["path"]).lower().endswith(".md")}
        })

    @app.route("/api/knowledge/reindex", methods=["POST"])
    def api_knowledge_reindex():
        stats = rt().knowledge.ensure_ready()
        return jsonify({"ok": True, "knowledge": stats})

    return app


def run_server() -> None:
    settings = load_settings()
    runtime = AppRuntime(settings)
    runtime.knowledge.ensure_ready()
    app = create_app(runtime)
    print(
        f"PikaQiu Agent UI: http://{settings.host}:{settings.port} "
        f"mode={'mock' if settings.use_mock_llm else 'direct-api'} "
        f"sandbox={settings.sandbox_container}"
    )
    try:
        app.run(
            host=settings.host,
            port=settings.port,
            debug=False,
            threaded=True,
            use_reloader=False,
        )
    except KeyboardInterrupt:
        print("\n[server] Shutting down...")
