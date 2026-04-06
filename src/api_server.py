from __future__ import annotations

from datetime import datetime
from pathlib import Path
import re
from typing import Any
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from core.models import DemoRunResult, NodeStatus, utc_now_iso
from settings import AppSettings, load_settings
from workflow import apply_default_goal, build_default_workflow, default_mapping_path


class CreateRunRequest(BaseModel):
    featureDescription: str = Field(min_length=3, max_length=4000)
    mappingPath: str | None = None


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


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/runs/latest")
def get_latest_run() -> dict[str, Any]:
    if _LATEST_RUN is None:
        raise HTTPException(status_code=404, detail="暂无运行记录")
    return _LATEST_RUN


@app.get("/api/runs/latest/actions")
def get_latest_actions() -> list[dict[str, Any]]:
    if _LATEST_RUN is None:
        raise HTTPException(status_code=404, detail="暂无运行记录")
    return _LATEST_RUN.get("actionLogs", [])


@app.get("/api/runs")
def list_runs() -> list[dict[str, Any]]:
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
    for run in _RUN_HISTORY:
        if run["runId"] == run_id:
            return run
    raise HTTPException(status_code=404, detail="未找到对应运行记录")


@app.get("/api/runs/{run_id}/actions")
def get_run_actions(run_id: str) -> list[dict[str, Any]]:
    for run in _RUN_HISTORY:
        if run["runId"] == run_id:
            return run.get("actionLogs", [])
    raise HTTPException(status_code=404, detail="未找到对应运行记录")


@app.post("/api/runs")
def create_run(payload: CreateRunRequest) -> dict[str, Any]:
    global _LATEST_RUN

    try:
        settings = load_settings()
        mapping_path = Path(payload.mappingPath) if payload.mappingPath else default_mapping_path()
        effective_description = apply_default_goal(payload.featureDescription)
        result = build_default_workflow(mapping_path=mapping_path).run_demo(effective_description)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    run_summary = _build_run_summary(result, effective_description, settings)
    _LATEST_RUN = run_summary
    _RUN_HISTORY.append(run_summary)
    if len(_RUN_HISTORY) > 30:
        del _RUN_HISTORY[:-30]
    return run_summary


def _build_run_summary(result: DemoRunResult, feature_description: str, settings: AppSettings) -> dict[str, Any]:
    run_id = f"run-{datetime.now().strftime('%Y%m%d-%H%M%S-%f')}-{uuid4().hex[:6]}"
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
        timeline=timeline,
    )

    current_node = next((node for node in nodes if node["status"] == "todo" and node["nodeType"] == "test"), None)

    return {
        "runId": run_id,
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


def _build_action_logs(
    *,
    result: DemoRunResult,
    feature_description: str,
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

    agent_trace = _extract_agent_trace(act_result.raw_output)
    tool_output = _strip_agent_trace(act_result.raw_output)
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
                "agentOutput": agent_trace,
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
    marker = "[agent_trace]"
    index = raw_output.find(marker)
    if index < 0:
        return None
    value = raw_output[index + len(marker):].lstrip("\r\n")
    return value or None


def _strip_agent_trace(raw_output: str) -> str:
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
    nodes: list[dict[str, Any]] = []

    for node in result.task_tree.nodes.values():
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
                "createdAt": started_at,
                "updatedAt": updated_at,
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
    model = result.state_table

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
    return "parsing:info"


def _derive_current_actor(result: DemoRunResult) -> str | None:
    if result.parsed_result is not None:
        return "parsing"
    if result.act_result is not None:
        return "act"
    return "reasoning"


def main() -> None:
    import uvicorn

    uvicorn.run("api_server:app", host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
