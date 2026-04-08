from __future__ import annotations

from datetime import datetime
import json
import os
from pathlib import Path
import re
import threading
from typing import Any
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from core.models import DemoRunResult, NodeStatus, NodeType, utc_now_iso
from workflow import apply_default_goal, build_default_workflow, default_mapping_path


class CreateRunRequest(BaseModel):
    featureDescription: str = Field(min_length=3, max_length=4000)
    mappingPath: str | None = None
    reasoningHint: str | None = Field(default=None, max_length=2000)


app = FastAPI(title="pikaqiu API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5173", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

_LATEST_RUN: dict[str, Any] | None = None
_RUN_HISTORY: list[dict[str, Any]] = []
_RUN_INDEX: dict[str, dict[str, Any]] = {}
_RUN_LOCK = threading.Lock()
_MAX_RUN_HISTORY = 30
_RUN_OUTPUT_DIR_ENV = "PIKAQIU_RUN_OUTPUT_DIR"
_RUN_OUTPUT_DIR_DEFAULT = "run_outputs"


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/runs/latest")
def get_latest_run() -> dict[str, Any] | None:
    with _RUN_LOCK:
        return _LATEST_RUN


@app.get("/api/runs/latest/actions")
def get_latest_actions() -> list[dict[str, Any]]:
    with _RUN_LOCK:
        if _LATEST_RUN is None:
            return []
        return _LATEST_RUN.get("actionLogs", [])


@app.get("/api/runs")
def list_runs() -> list[dict[str, Any]]:
    with _RUN_LOCK:
        items: list[dict[str, Any]] = []
        for run in reversed(_RUN_HISTORY):
            items.append(
                {
                    "runId": run["runId"],
                    "goal": run["goal"],
                    "status": run["status"],
                    "updatedAt": run["updatedAt"],
                    "currentStage": run["currentStage"],
                }
            )
        return items


@app.get("/api/runs/{run_id}")
def get_run(run_id: str) -> dict[str, Any]:
    with _RUN_LOCK:
        run = _RUN_INDEX.get(run_id)
        if run is not None:
            return run
    raise HTTPException(status_code=404, detail="未找到对应运行记录")


@app.get("/api/runs/{run_id}/actions")
def get_run_actions(run_id: str) -> list[dict[str, Any]]:
    with _RUN_LOCK:
        run = _RUN_INDEX.get(run_id)
        if run is not None:
            return run.get("actionLogs", [])
    raise HTTPException(status_code=404, detail="未找到对应运行记录")


@app.post("/api/runs")
def create_run(payload: CreateRunRequest) -> dict[str, Any]:
    try:
        mapping_path = Path(payload.mappingPath) if payload.mappingPath else default_mapping_path()
        effective_description = apply_default_goal(payload.featureDescription)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    run_id = _new_run_id()
    run_summary = _build_running_run_summary(
        run_id=run_id,
        feature_description=effective_description,
        reasoning_hint=payload.reasoningHint,
    )

    with _RUN_LOCK:
        _upsert_run_summary_locked(run_summary)

    worker = threading.Thread(
        target=_execute_run_background,
        kwargs={
            "run_id": run_id,
            "feature_description": effective_description,
            "mapping_path": mapping_path,
            "reasoning_hint": payload.reasoningHint,
        },
        daemon=True,
    )
    worker.start()
    return run_summary


def _build_run_summary(
    result: DemoRunResult,
    feature_description: str,
    reasoning_hint: str | None = None,
    run_id: str | None = None,
) -> dict[str, Any]:
    effective_run_id = run_id or _new_run_id()
    now_iso = utc_now_iso()
    act_result = result.act_result
    parsed_result = result.parsed_result

    started_at = act_result.started_at if act_result else now_iso
    updated_at = act_result.finished_at if act_result else now_iso

    run_status = "completed"
    if act_result and act_result.exit_code != 0:
        run_status = "failed"

    nodes = _build_nodes(result, started_at, updated_at)

    tool_call_id = "tc-001"
    tool_calls = _build_tool_calls(act_result, tool_call_id)
    timeline = _build_timeline(result, tool_call_id)

    parsing_event_id = next(
        (event["id"] for event in timeline if event["eventType"] == "parsing_completed"),
        timeline[-1]["id"] if timeline else "evt-001",
    )
    reasoning_event_id = next(
        (event["id"] for event in timeline if event["eventType"] == "reasoning_completed"),
        timeline[-1]["id"] if timeline else "evt-001",
    )

    parsing_results = _build_parsing_results(result, parsing_event_id)
    reasoning_results = _build_reasoning_results(result, reasoning_event_id)
    state_table = _build_state_table(result, parsing_event_id)
    action_logs = _build_action_logs(
        result=result,
        feature_description=feature_description,
        reasoning_hint=reasoning_hint,
        timeline=timeline,
    )

    current_node = next((node for node in nodes if node["status"] == "todo" and node["nodeType"] == "test"), None)

    return {
        "runId": effective_run_id,
        "target": _extract_target(feature_description),
        "goal": feature_description,
        "status": run_status,
        "currentStage": _derive_current_stage(result),
        "startedAt": started_at,
        "updatedAt": updated_at,
        "currentNodeId": current_node["id"] if current_node else None,
        "currentActor": _derive_current_actor(result),
        "nodes": nodes,
        "timeline": timeline,
        "toolCalls": tool_calls,
        "actionLogs": action_logs,
        "parsingResults": parsing_results,
        "reasoningResults": reasoning_results,
        "stateTable": state_table,
    }


def _new_run_id() -> str:
    return f"run-{datetime.now().strftime('%Y%m%d-%H%M%S-%f')}-{uuid4().hex[:6]}"


def _empty_state_table() -> dict[str, Any]:
    return {
        "identities": [],
        "sessionMaterials": [],
        "keyEntrypoints": [],
        "workflowPrerequisites": [],
        "reusableArtifacts": [],
        "sessionRisks": [],
        "notes": [],
        "latestUpdateEventId": "evt-000",
    }


def _build_running_run_summary(
    *,
    run_id: str,
    feature_description: str,
    reasoning_hint: str | None,
) -> dict[str, Any]:
    now_iso = utc_now_iso()
    hint = (reasoning_hint or "").strip()
    return {
        "runId": run_id,
        "target": _extract_target(feature_description),
        "goal": feature_description,
        "status": "running",
        "currentStage": "bootstrap",
        "startedAt": now_iso,
        "updatedAt": now_iso,
        "currentNodeId": None,
        "currentActor": "reasoning",
        "nodes": [],
        "timeline": [],
        "toolCalls": [],
        "actionLogs": [
            {
                "id": "action-live-001",
                "stepIndex": 1,
                "stage": "reasoning:plan",
                "actor": "reasoning",
                "title": "启动实时运行",
                "status": "running",
                "startedAt": now_iso,
                "finishedAt": now_iso,
                "durationMs": 0,
                "input": {
                    "featureDescription": feature_description,
                    "reasoningHint": hint,
                },
                "output": {
                    "message": "工作流已进入后台执行，将持续刷新事件。",
                },
                "error": None,
            }
        ],
        "parsingResults": [],
        "reasoningResults": [],
        "stateTable": _empty_state_table(),
    }


def _upsert_run_summary_locked(run_summary: dict[str, Any]) -> None:
    global _LATEST_RUN

    run_id = run_summary["runId"]

    output_path = _run_output_path(run_id)
    run_summary["outputFile"] = str(output_path)
    run_summary["outputFileRelative"] = _workspace_relative_path(output_path)

    _RUN_INDEX[run_id] = run_summary

    for index, item in enumerate(_RUN_HISTORY):
        if item["runId"] == run_id:
            _RUN_HISTORY[index] = run_summary
            break
    else:
        _RUN_HISTORY.append(run_summary)

    if len(_RUN_HISTORY) > _MAX_RUN_HISTORY:
        del _RUN_HISTORY[:-_MAX_RUN_HISTORY]
        _RUN_INDEX.clear()
        for item in _RUN_HISTORY:
            _RUN_INDEX[item["runId"]] = item

    _LATEST_RUN = run_summary

    _persist_run_output(run_summary, output_path)


def _workspace_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _resolve_run_output_dir() -> Path:
    configured = os.getenv(_RUN_OUTPUT_DIR_ENV, "").strip()
    if configured:
        candidate = Path(configured).expanduser()
        if not candidate.is_absolute():
            candidate = (_workspace_root() / candidate).resolve()
        return candidate
    return (_workspace_root() / _RUN_OUTPUT_DIR_DEFAULT).resolve()


def _run_output_path(run_id: str) -> Path:
    safe_run_id = re.sub(r"[^A-Za-z0-9._-]+", "_", run_id).strip("_") or "run"
    return _resolve_run_output_dir() / f"{safe_run_id}.json"


def _workspace_relative_path(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(_workspace_root())).replace("\\", "/")
    except Exception:
        return str(path)


def _persist_run_output(run_summary: dict[str, Any], output_path: Path) -> None:
    payload = {
        "runId": run_summary.get("runId"),
        "exportedAt": utc_now_iso(),
        # 这里落盘的是前端可见的完整运行数据。
        "visibleRunData": run_summary,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def _event_actor(stage: str) -> str:
    prefix = stage.split(":", 1)[0]
    if prefix in {"reasoning", "act", "parsing"}:
        return prefix
    return "system"


def _event_type(stage: str, status: str) -> str:
    if stage == "reasoning:finish":
        return "reasoning_completed"
    if stage == "parsing:finish":
        return "parsing_completed"
    if stage in {"act:start", "parsing:start", "reasoning:start"}:
        return "agent_step_started"
    if stage == "act:finish":
        return "agent_step_finished"
    if status == "failed":
        return "error"
    return "node_updated"


def _event_status(status: str) -> str:
    if status in {"running", "success", "failed", "retry"}:
        return status
    return "info"


def _map_stage_to_run_stage(current_stage: str, stage: str, event_input: dict[str, Any]) -> str:
    if stage == "workflow:finish":
        return "completed"
    if stage.startswith("reasoning:"):
        if current_stage in {"parsing:result", "parsing:test", "act:test", "reasoning:update-plan"}:
            return "reasoning:update-plan"
        return "reasoning:feature-mapping"
    if stage.startswith("act:"):
        node_type = str(event_input.get("nodeType", "")).strip().lower()
        if node_type == "test":
            return "act:test"
        if node_type == "info":
            return "act:info"
        if current_stage in {"reasoning:update-plan", "parsing:test", "act:test"}:
            return "act:test"
        return "act:info"
    if stage.startswith("parsing:"):
        return "parsing:result"
    return current_stage


def _event_to_timeline_item(event: dict[str, Any], timeline_len: int) -> dict[str, Any]:
    event_input = event.get("input") or {}
    event_output = event.get("output") or {}
    status = _event_status(str(event.get("status", "info")))
    started_at = str(event.get("timestamp") or utc_now_iso())
    finished_at = started_at if status != "running" else None
    error_message = event.get("error")
    event_id = f"evt-live-{timeline_len + 1:03d}"

    node_id = event_input.get("nodeId") or event_output.get("nodeId")
    if node_id is not None:
        node_id = str(node_id)

    return {
        "id": event_id,
        "stepIndex": timeline_len + 1,
        "eventType": _event_type(str(event.get("stage", "")), status),
        "actor": _event_actor(str(event.get("stage", ""))),
        "title": str(event.get("title") or "工作流事件"),
        "summary": str(event_output.get("summary") or event.get("title") or ""),
        "status": status,
        "startedAt": started_at,
        "finishedAt": finished_at,
        "durationMs": _duration_ms(started_at, finished_at),
        "relatedNodeId": node_id,
        "relatedToolCallId": None,
        "rawInput": event_input,
        "rawOutput": event_output,
        "parsedOutput": None,
        "error": None if not error_message else {
            "code": "WORKFLOW_EVENT_ERROR",
            "message": str(error_message),
        },
    }


def _append_live_tool_call(run_summary: dict[str, Any], event: dict[str, Any], related_event_id: str) -> None:
    stage = str(event.get("stage", ""))
    if stage != "act:finish":
        return

    output = event.get("output") or {}
    tool_name = str(output.get("toolName") or "unknown")
    command = str(output.get("command") or "")
    exit_code = int(output.get("exitCode", 0)) if str(output.get("exitCode", "")).strip() else 0
    status = "success" if exit_code == 0 else "failed"
    started_at = str(event.get("timestamp") or utc_now_iso())
    node_id = output.get("nodeId")

    run_summary["toolCalls"].append(
        {
            "id": f"tc-live-{len(run_summary['toolCalls']) + 1:03d}",
            "toolName": tool_name,
            "title": f"执行工具: {tool_name}",
            "summary": f"节点 {node_id or '-'} 执行命令。",
            "status": status,
            "startedAt": started_at,
            "finishedAt": started_at,
            "durationMs": 0,
            "request": {
                "toolName": tool_name,
                "command": command,
            },
            "response": {
                "exitCode": exit_code,
                "rawOutput": output.get("rawOutput"),
                "agentOutput": output.get("agentOutput"),
            },
            "error": None if status == "success" else {
                "code": "TOOL_EXIT_NON_ZERO",
                "message": f"工具退出码为 {exit_code}",
            },
            "relatedNodeId": str(node_id) if node_id else None,
            "relatedEventId": related_event_id,
        }
    )


def _apply_live_event(run_summary: dict[str, Any], event: dict[str, Any]) -> None:
    timeline = run_summary["timeline"]
    item = _event_to_timeline_item(event, len(timeline))
    timeline.append(item)

    _append_live_tool_call(run_summary, event, item["id"])

    stage = str(event.get("stage", ""))
    event_input = event.get("input") or {}
    event_output = event.get("output") or {}
    node_id = event_input.get("nodeId") or event_output.get("nodeId")
    if node_id is not None:
        run_summary["currentNodeId"] = str(node_id)

    run_summary["currentActor"] = _event_actor(stage)
    run_summary["currentStage"] = _map_stage_to_run_stage(
        str(run_summary.get("currentStage", "bootstrap")),
        stage,
        event_input,
    )
    run_summary["updatedAt"] = item["startedAt"]

    if stage == "workflow:finish":
        run_summary["status"] = "completed"
        run_summary["currentStage"] = "completed"
        run_summary["currentActor"] = "system"
    elif stage == "workflow:guard":
        run_summary["status"] = "failed"


def _execute_run_background(
    *,
    run_id: str,
    feature_description: str,
    mapping_path: Path,
    reasoning_hint: str | None,
) -> None:
    try:
        workflow = build_default_workflow(mapping_path=mapping_path)

        def event_callback(event: dict[str, Any]) -> None:
            with _RUN_LOCK:
                run_summary = _RUN_INDEX.get(run_id)
                if run_summary is None:
                    return
                _apply_live_event(run_summary, event)
                _sync_live_nodes_and_state(run_summary, workflow)
                _upsert_run_summary_locked(run_summary)

        result = workflow.run_demo_with_events(
            feature_description,
            event_callback=event_callback,
            reasoning_hint=reasoning_hint,
        )

        final_run = _build_run_summary(
            result,
            feature_description,
            reasoning_hint=reasoning_hint,
            run_id=run_id,
        )

        with _RUN_LOCK:
            live_run = _RUN_INDEX.get(run_id)
            if live_run is not None:
                if live_run.get("timeline"):
                    final_run["timeline"] = list(live_run["timeline"])
                if live_run.get("toolCalls"):
                    final_run["toolCalls"] = list(live_run["toolCalls"])
                final_run["startedAt"] = live_run.get("startedAt", final_run["startedAt"])
                final_run["updatedAt"] = utc_now_iso()
            _upsert_run_summary_locked(final_run)
    except Exception as exc:  # pragma: no cover
        now_iso = utc_now_iso()
        with _RUN_LOCK:
            run_summary = _RUN_INDEX.get(run_id)
            if run_summary is None:
                return
            run_summary["status"] = "failed"
            run_summary["updatedAt"] = now_iso
            run_summary["timeline"].append(
                {
                    "id": f"evt-live-{len(run_summary['timeline']) + 1:03d}",
                    "stepIndex": len(run_summary["timeline"]) + 1,
                    "eventType": "error",
                    "actor": "system",
                    "title": "后台运行失败",
                    "summary": str(exc),
                    "status": "failed",
                    "startedAt": now_iso,
                    "finishedAt": now_iso,
                    "durationMs": 0,
                    "relatedNodeId": None,
                    "relatedToolCallId": None,
                    "rawInput": None,
                    "rawOutput": None,
                    "parsedOutput": None,
                    "error": {
                        "code": "RUN_EXECUTION_FAILED",
                        "message": str(exc),
                    },
                }
            )
            _upsert_run_summary_locked(run_summary)


def _build_action_logs(
    *,
    result: DemoRunResult,
    feature_description: str,
    reasoning_hint: str | None,
    timeline: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    logs: list[dict[str, Any]] = []
    act_result = result.act_result
    parsed_result = result.parsed_result

    started_at = act_result.started_at if act_result else utc_now_iso()
    finished_at = act_result.finished_at if act_result else started_at

    logs.append(
        {
            "id": "action-001",
            "stepIndex": 1,
            "stage": "reasoning:plan",
            "actor": "reasoning",
            "title": "生成初始计划与测试节点",
            "status": "success",
            "startedAt": started_at,
            "finishedAt": started_at,
            "durationMs": 0,
            "input": {
                "featureDescription": feature_description,
                "reasoningHint": reasoning_hint,
            },
            "output": {
                "agentOutput": result.plan.trace,
                "featurePoint": {
                    "id": result.feature_point.id,
                    "name": result.feature_point.name,
                    "entryPoints": result.feature_point.entry_points,
                    "roles": result.feature_point.roles,
                    "objects": result.feature_point.objects,
                    "keyParameters": result.feature_point.key_parameters,
                },
                "recommendedFamilies": [
                    {
                        "familyId": item.family.id,
                        "familyName": item.family.name,
                        "score": item.score,
                        "matchedTerms": item.matched_terms,
                    }
                    for item in result.plan.recommended_families
                ],
                "createdNodes": [
                    {
                        "id": result.plan.info_node.id,
                        "title": result.plan.info_node.title,
                        "nodeType": result.plan.info_node.node_type.value,
                    },
                    *[
                        {
                            "id": node.id,
                            "title": node.title,
                            "nodeType": node.node_type.value,
                            "familyId": node.related_test_family,
                        }
                        for node in result.plan.test_nodes
                    ],
                ],
            },
            "error": None,
        }
    )

    if act_result is None:
        return logs

    tool_output = act_result.raw_output
    tool_stdout, tool_stderr = _split_stdout_stderr(tool_output)

    logs.append(
        {
            "id": "action-002",
            "stepIndex": 2,
            "stage": "act:agent",
            "actor": "act",
            "title": "act agent 选择工具与命令",
            "status": "success",
            "startedAt": act_result.started_at,
            "finishedAt": act_result.started_at,
            "durationMs": 0,
            "input": {
                "nodeId": act_result.node_id,
            },
            "output": {
                "agentOutput": act_result.agent_output,
                "toolName": act_result.tool_name,
                "command": act_result.command,
            },
            "error": None,
        }
    )

    tool_status = "success" if act_result.exit_code == 0 else "failed"
    logs.append(
        {
            "id": "action-003",
            "stepIndex": 3,
            "stage": "act:tool",
            "actor": "tool",
            "title": "执行工具调用",
            "status": tool_status,
            "startedAt": act_result.started_at,
            "finishedAt": act_result.finished_at,
            "durationMs": _duration_ms(act_result.started_at, act_result.finished_at),
            "input": {
                "toolName": act_result.tool_name,
                "command": act_result.command,
            },
            "output": {
                "exitCode": act_result.exit_code,
                "stdout": tool_stdout,
                "stderr": tool_stderr,
                "rawOutput": tool_output,
            },
            "error": None if act_result.exit_code == 0 else {
                "code": "TOOL_EXIT_NON_ZERO",
                "message": f"工具退出码为 {act_result.exit_code}",
            },
        }
    )

    if parsed_result is not None:
        parsing_agent_output = "\n".join(parsed_result.state_delta.notes).strip() or None
        logs.append(
            {
                "id": "action-004",
                "stepIndex": 4,
                "stage": "parsing:result",
                "actor": "parsing",
                "title": "parsing agent 结构化输出",
                "status": "success",
                "startedAt": finished_at,
                "finishedAt": finished_at,
                "durationMs": 0,
                "input": {
                    "nodeId": parsed_result.node_id,
                    "toolRawOutput": tool_output,
                },
                "output": {
                    "agentOutput": parsing_agent_output,
                    "summary": parsed_result.summary,
                    "nextStatus": parsed_result.next_status.value,
                    "evidence": [item.model_dump() for item in parsed_result.evidence],
                    "conclusions": [item.model_dump() for item in parsed_result.conclusions],
                    "stateDelta": parsed_result.state_delta.model_dump(),
                },
                "error": None,
            }
        )

        logs.append(
            {
                "id": "action-005",
                "stepIndex": 5,
                "stage": "reasoning:update",
                "actor": "reasoning",
                "title": "reasoning 吸收解析结果",
                "status": "success",
                "startedAt": finished_at,
                "finishedAt": finished_at,
                "durationMs": 0,
                "input": {
                    "nodeId": parsed_result.node_id,
                    "summary": parsed_result.summary,
                },
                "output": {
                    "agentOutput": result.reasoning_ingest_trace,
                    "stateSnapshot": {
                        "identityCount": len(result.state_table.identities),
                        "entrypointCount": len(result.state_table.key_entrypoints),
                        "sessionMaterialCount": len(result.state_table.session_materials),
                        "artifactCount": len(result.state_table.reusable_artifacts),
                    },
                },
                "error": None,
            }
        )

    logs.append(
        {
            "id": f"action-{len(logs) + 1:03d}",
            "stepIndex": len(logs) + 1,
            "stage": "system:timeline",
            "actor": "system",
            "title": "生成可视化时间线",
            "status": "success",
            "startedAt": finished_at,
            "finishedAt": finished_at,
            "durationMs": 0,
            "input": {
                "timelineEventCount": len(timeline),
            },
            "output": {
                "timeline": timeline,
            },
            "error": None,
        }
    )

    return logs


def _extract_agent_trace(raw_output: str) -> str | None:
    # 兼容旧版本日志格式，当前版本已使用独立字段 agent_output。
    marker = "[agent_trace]"
    index = raw_output.find(marker)
    if index < 0:
        return None
    value = raw_output[index + len(marker):].lstrip("\r\n")
    return value or None


def _strip_agent_trace(raw_output: str) -> str:
    # 兼容旧版本日志格式，当前版本已不再拼接 [agent_trace]。
    marker = "[agent_trace]"
    index = raw_output.find(marker)
    if index < 0:
        return raw_output
    return raw_output[:index].rstrip()


def _split_stdout_stderr(tool_output: str) -> tuple[str, str]:
    marker = "[stderr]"
    index = tool_output.find(marker)
    if index < 0:
        return tool_output, ""
    stdout = tool_output[:index].rstrip()
    stderr = tool_output[index + len(marker):].lstrip("\r\n")
    return stdout, stderr


def _build_nodes(result: DemoRunResult, started_at: str, updated_at: str) -> list[dict[str, Any]]:
    return _build_nodes_from_task_tree(
        task_tree_model=result.task_tree,
        started_at=started_at,
        updated_at=updated_at,
    )


def _build_nodes_from_task_tree(
    *,
    task_tree_model: Any,
    started_at: str,
    updated_at: str,
    previous_nodes: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    previous_by_id = {item.get("id"): item for item in (previous_nodes or [])}
    nodes: list[dict[str, Any]] = []

    for node in task_tree_model.nodes.values():
        previous = previous_by_id.get(node.id)
        created_at = started_at
        node_updated_at = updated_at
        if previous is not None:
            created_at = str(previous.get("createdAt") or started_at)
            previous_status = str(previous.get("status") or "")
            current_status = _node_status_value(node.status)
            if previous_status == current_status:
                node_updated_at = str(previous.get("updatedAt") or updated_at)

        nodes.append(
            {
                "id": node.id,
                "title": node.title,
                "nodeType": node.node_type.value,
                "status": _node_status_value(node.status),
                "parentId": node.parent_id,
                "source": node.source,
                "sourceFeatureId": node.related_feature_id,
                "familyIds": [node.related_test_family] if node.related_test_family else [],
                "primaryFamilyId": node.related_test_family,
                "notes": list(node.notes),
                "evidenceRefs": list(node.evidence_refs),
                "createdAt": created_at,
                "updatedAt": node_updated_at,
            }
        )

    return nodes


def _node_status_value(status: NodeStatus) -> str:
    if status == NodeStatus.TODO:
        return "todo"
    if status == NodeStatus.DOING:
        return "doing"
    return "done"


def _build_tool_calls(act_result: Any, tool_call_id: str) -> list[dict[str, Any]]:
    if act_result is None:
        return []

    status = "success" if act_result.exit_code == 0 else "failed"
    error = None
    if act_result.exit_code != 0:
        error = {
            "code": "TOOL_EXIT_NON_ZERO",
            "message": f"工具退出码为 {act_result.exit_code}",
            "details": act_result.raw_output[:4000],
        }

    return [
        {
            "id": tool_call_id,
            "toolName": act_result.tool_name,
            "title": f"执行工具: {act_result.tool_name}",
            "summary": f"节点 {act_result.node_id} 执行命令。",
            "status": status,
            "startedAt": act_result.started_at,
            "finishedAt": act_result.finished_at,
            "durationMs": _duration_ms(act_result.started_at, act_result.finished_at),
            "request": {
                "toolName": act_result.tool_name,
                "command": act_result.command,
            },
            "response": {
                "exitCode": act_result.exit_code,
                "rawOutput": act_result.raw_output,
                "agentOutput": act_result.agent_output,
            },
            "error": error,
            "relatedNodeId": act_result.node_id,
            "relatedEventId": "evt-003",
        }
    ]


def _build_timeline(result: DemoRunResult, tool_call_id: str) -> list[dict[str, Any]]:
    act_result = result.act_result
    parsed_result = result.parsed_result
    feature = result.feature_point

    if act_result is None:
        return []

    events: list[dict[str, Any]] = []

    def add_event(
        *,
        event_type: str,
        actor: str,
        title: str,
        summary: str,
        status: str,
        started_at: str,
        finished_at: str | None,
        related_node_id: str | None = None,
        related_tool_call_id: str | None = None,
        raw_input: Any = None,
        raw_output: Any = None,
        parsed_output: Any = None,
        error: dict[str, str] | None = None,
    ) -> str:
        event_id = f"evt-{len(events) + 1:03d}"
        events.append(
            {
                "id": event_id,
                "stepIndex": len(events) + 1,
                "eventType": event_type,
                "actor": actor,
                "title": title,
                "summary": summary,
                "status": status,
                "startedAt": started_at,
                "finishedAt": finished_at,
                "durationMs": _duration_ms(started_at, finished_at),
                "relatedNodeId": related_node_id,
                "relatedToolCallId": related_tool_call_id,
                "rawInput": raw_input,
                "rawOutput": raw_output,
                "parsedOutput": parsed_output,
                "error": error,
            }
        )
        return event_id

    info_node = result.plan.info_node
    add_event(
        event_type="node_created",
        actor="system",
        title="创建信息节点",
        summary="根据输入目标生成初始信息采集节点。",
        status="success",
        started_at=act_result.started_at,
        finished_at=act_result.started_at,
        related_node_id=info_node.id,
        raw_output={"nodeId": info_node.id, "nodeType": "info"},
    )

    add_event(
        event_type="reasoning_completed",
        actor="reasoning",
        title="推理完成测试家族映射",
        summary=f"命中 {len(result.plan.recommended_families)} 个测试家族。",
        status="success",
        started_at=act_result.started_at,
        finished_at=act_result.started_at,
        related_node_id=info_node.id,
        raw_input={"featureId": feature.id},
        raw_output={"familyCount": len(result.plan.recommended_families)},
    )

    for test_node in result.plan.test_nodes:
        add_event(
            event_type="node_created",
            actor="reasoning",
            title=f"创建测试节点: {test_node.title}",
            summary="依据测试家族扩展任务树。",
            status="success",
            started_at=act_result.started_at,
            finished_at=act_result.started_at,
            related_node_id=test_node.id,
            raw_output={"nodeId": test_node.id, "nodeType": "test"},
        )

    add_event(
        event_type="agent_step_started",
        actor="act",
        title="执行代理开始",
        summary=f"开始执行节点 {act_result.node_id}。",
        status="running",
        started_at=act_result.started_at,
        finished_at=act_result.started_at,
        related_node_id=act_result.node_id,
        raw_input={"nodeId": act_result.node_id},
    )

    add_event(
        event_type="tool_call_started",
        actor="tool",
        title="工具调用开始",
        summary="开始执行工具命令。",
        status="running",
        started_at=act_result.started_at,
        finished_at=act_result.started_at,
        related_node_id=act_result.node_id,
        related_tool_call_id=tool_call_id,
        raw_input={"toolName": act_result.tool_name, "command": act_result.command},
    )

    tool_status = "success" if act_result.exit_code == 0 else "failed"
    tool_error = None
    if act_result.exit_code != 0:
        tool_error = {
            "code": "TOOL_EXIT_NON_ZERO",
            "message": f"工具退出码为 {act_result.exit_code}",
            "details": act_result.raw_output[:4000],
        }

    add_event(
        event_type="tool_call_finished",
        actor="tool",
        title="工具调用结束",
        summary="工具返回执行结果。",
        status=tool_status,
        started_at=act_result.started_at,
        finished_at=act_result.finished_at,
        related_node_id=act_result.node_id,
        related_tool_call_id=tool_call_id,
        raw_input={"toolName": act_result.tool_name, "command": act_result.command},
        raw_output={"exitCode": act_result.exit_code, "rawOutput": act_result.raw_output},
        error=tool_error,
    )

    if parsed_result is not None:
        add_event(
            event_type="parsing_completed",
            actor="parsing",
            title="解析完成",
            summary=parsed_result.summary,
            status="success",
            started_at=act_result.finished_at,
            finished_at=act_result.finished_at,
            related_node_id=parsed_result.node_id,
            raw_output={"summary": parsed_result.summary},
            parsed_output={"evidenceCount": len(parsed_result.evidence), "conclusionCount": len(parsed_result.conclusions)},
        )

        add_event(
            event_type="node_updated",
            actor="system",
            title="节点状态更新",
            summary=f"节点更新为 {parsed_result.next_status.value}。",
            status="success",
            started_at=act_result.finished_at,
            finished_at=act_result.finished_at,
            related_node_id=parsed_result.node_id,
            raw_output={"nextStatus": parsed_result.next_status.value},
        )

        add_event(
            event_type="reasoning_completed",
            actor="reasoning",
            title="吸收解析结果并更新计划",
            summary="根据 parsing 结果更新任务树与状态表。",
            status="success",
            started_at=act_result.finished_at,
            finished_at=act_result.finished_at,
            related_node_id=parsed_result.node_id,
            raw_output={
                "agentOutput": result.reasoning_ingest_trace,
                "stateSnapshot": {
                    "identityCount": len(result.state_table.identities),
                    "entrypointCount": len(result.state_table.key_entrypoints),
                },
            },
        )

    if act_result.exit_code != 0:
        add_event(
            event_type="error",
            actor="system",
            title="执行阶段出现错误",
            summary="工具执行失败，请查看原始输出。",
            status="failed",
            started_at=act_result.finished_at,
            finished_at=act_result.finished_at,
            related_node_id=act_result.node_id,
            related_tool_call_id=tool_call_id,
            error=tool_error,
        )

    return events


def _build_parsing_results(result: DemoRunResult, parsing_event_id: str) -> list[dict[str, Any]]:
    parsed_result = result.parsed_result
    if parsed_result is None:
        return []

    sections = _empty_parsing_sections()
    evidence_refs = [item.id for item in parsed_result.evidence]
    sections["discovered_actions"] = [
        {
            "id": "action-1",
            "text": parsed_result.summary,
            "sourceEventId": parsing_event_id,
            "sourceToolCallId": "tc-001",
            "evidenceRefs": evidence_refs,
        }
    ]
    sections["discovered_objects"] = [
        {
            "id": f"conclusion-{index + 1}",
            "text": f"{item.title}: {item.summary}",
            "sourceEventId": parsing_event_id,
            "sourceToolCallId": "tc-001",
            "evidenceRefs": item.evidence_ids,
        }
        for index, item in enumerate(parsed_result.conclusions)
    ]

    discovered_endpoints: list[str] = []
    for item in parsed_result.evidence:
        for endpoint in _extract_urls(item.content):
            if endpoint not in discovered_endpoints:
                discovered_endpoints.append(endpoint)

    sections["discovered_endpoints"] = [
        {
            "id": f"endpoint-{index + 1}",
            "text": endpoint,
            "sourceEventId": parsing_event_id,
            "sourceToolCallId": "tc-001",
            "evidenceRefs": evidence_refs,
        }
        for index, endpoint in enumerate(discovered_endpoints)
    ]

    notes = [
        {
            "id": f"note-{index + 1}",
            "text": item,
            "sourceEventId": parsing_event_id,
            "evidenceRefs": [record.id for record in parsed_result.evidence],
        }
        for index, item in enumerate(parsed_result.state_delta.notes)
    ]

    return [
        {
            "id": f"parse-{parsed_result.node_id}",
            "eventId": parsing_event_id,
            "relatedNodeId": parsed_result.node_id,
            "summary": parsed_result.summary,
            "factsByType": sections,
            "notes": notes,
        }
    ]


def _build_reasoning_results(result: DemoRunResult, reasoning_event_id: str) -> list[dict[str, Any]]:
    plan = result.plan
    feature = result.feature_point
    evidence_refs: list[str] = []
    if result.parsed_result and result.parsed_result.evidence:
        evidence_refs = [result.parsed_result.evidence[0].id]

    identified_features = [
        {
            "featureId": feature.id,
            "title": feature.name,
            "summary": feature.description,
            "evidenceRefs": evidence_refs,
            "facts": feature.entry_points + feature.key_parameters + feature.roles + feature.objects,
        }
    ]

    family_mapping = []
    for item in plan.recommended_families:
        confidence = min(0.99, max(0.2, item.score / 20))
        family_mapping.append(
            {
                "featureId": feature.id,
                "familyIds": [item.family.id],
                "primaryFamilyId": item.family.id,
                "confidence": round(confidence, 2),
                "reasons": [f"命中词: {', '.join(item.matched_terms[:8]) or '-'}"],
                "familyNames": [item.family.name],
                "familyScores": {item.family.id: item.score},
            }
        )

    proposed_nodes = []
    for node in plan.test_nodes:
        proposed_nodes.append(
            {
                "title": node.title,
                "nodeType": "test",
                "sourceFeatureId": node.related_feature_id,
                "familyIds": [node.related_test_family] if node.related_test_family else [],
                "primaryFamilyId": node.related_test_family,
                "rationale": node.description,
                "priority": 1,
                "createdNodeId": node.id,
            }
        )

    return [
        {
            "id": f"reason-{feature.id}",
            "eventId": reasoning_event_id,
            "relatedNodeId": plan.info_node.id,
            "identifiedFeatures": identified_features,
            "familyMapping": family_mapping,
            "proposedTestNodes": proposed_nodes,
            "createdNodeIds": [node.id for node in plan.test_nodes],
        }
    ]


def _build_state_table(result: DemoRunResult, updated_event_id: str) -> dict[str, Any]:
    return _build_state_table_from_model(result.state_table, updated_event_id)


def _build_state_table_from_model(model: Any, updated_event_id: str) -> dict[str, Any]:

    def convert_items(items: list[Any]) -> list[dict[str, Any]]:
        return [
            {
                "id": item.id,
                "title": item.title,
                "content": item.content,
                "refs": item.refs,
                "source": item.source or "-",
                "updatedInEventId": updated_event_id,
                "isNew": True,
            }
            for item in items
        ]

    notes = [
        {
            "id": f"state-note-{index + 1}",
            "text": note,
            "updatedInEventId": updated_event_id,
            "isNew": True,
        }
        for index, note in enumerate(model.notes)
    ]

    return {
        "identities": convert_items(model.identities),
        "sessionMaterials": convert_items(model.session_materials),
        "keyEntrypoints": convert_items(model.key_entrypoints),
        "workflowPrerequisites": convert_items(model.workflow_prerequisites),
        "reusableArtifacts": convert_items(model.reusable_artifacts),
        "sessionRisks": convert_items(model.session_risks),
        "notes": notes,
        "latestUpdateEventId": updated_event_id,
    }


def _sync_live_nodes_and_state(run_summary: dict[str, Any], workflow: Any) -> None:
    now_iso = utc_now_iso()
    timeline = run_summary.get("timeline") or []
    latest_event_id = timeline[-1]["id"] if timeline else "evt-000"

    run_summary["nodes"] = _build_nodes_from_task_tree(
        task_tree_model=workflow.task_tree.model,
        started_at=str(run_summary.get("startedAt") or now_iso),
        updated_at=now_iso,
        previous_nodes=run_summary.get("nodes") or [],
    )
    run_summary["stateTable"] = _build_state_table_from_model(workflow.state_store.model, latest_event_id)

    if not run_summary.get("currentNodeId"):
        next_node = workflow.task_tree.next_todo(NodeType.INFO) or workflow.task_tree.next_todo(NodeType.TEST)
        run_summary["currentNodeId"] = next_node.id if next_node is not None else None


def _empty_parsing_sections() -> dict[str, list[dict[str, Any]]]:
    keys = [
        "discovered_pages",
        "discovered_endpoints",
        "discovered_fields",
        "discovered_objects",
        "discovered_actions",
        "discovered_flows",
        "discovered_roles",
        "discovered_render_points",
        "discovered_upload_points",
        "discovered_callback_points",
    ]
    return {key: [] for key in keys}


def _duration_ms(started_at: str, finished_at: str | None) -> int | None:
    if finished_at is None:
        return None
    started = _parse_iso(started_at)
    finished = _parse_iso(finished_at)
    return int(max((finished - started).total_seconds() * 1000, 0))


def _parse_iso(value: str) -> datetime:
    normalized = value.replace("Z", "+00:00")
    return datetime.fromisoformat(normalized)


def _extract_target(feature_description: str) -> str:
    match = re.search(r"https?://[^\s,;，；。！？]+", feature_description)
    if match:
        return match.group(0).rstrip("，。！？；,:;)")
    return feature_description.strip()[:120] or "unknown-target"


def _extract_urls(text: str) -> list[str]:
    return re.findall(r"https?://[^\s,;]+", text)


def _derive_current_stage(result: DemoRunResult) -> str:
    if result.act_result is None:
        return "bootstrap"
    if result.parsed_result is None:
        return "act:info"
    if result.reasoning_ingest_trace:
        return "reasoning:update-plan"
    return "parsing:result"


def _derive_current_actor(result: DemoRunResult) -> str | None:
    if result.reasoning_ingest_trace is not None:
        return "reasoning"
    if result.parsed_result is not None:
        return "parsing"
    if result.act_result is not None:
        return "act"
    return "reasoning"


def main() -> None:
    import uvicorn

    port_text = os.getenv("PIKAQIU_API_PORT", "8000").strip()
    try:
        port = int(port_text)
    except ValueError:
        port = 8000
    uvicorn.run("api_server:app", host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
