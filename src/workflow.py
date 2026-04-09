from __future__ import annotations

import json
from pathlib import Path
import re
from typing import Any, Callable

from agents.act import ActAgent
from agents.parsing import ParsingAgent
from agents.reasoning import ReasoningAgent
from core.mapping import TestFamilyMapper
from core.models import DemoRunResult, FeaturePoint, NodeType, StateTable, TaskNode, utc_now_iso
from core.state_table import StateTableStore
from core.task_tree import TaskTree
from infra.mcp import BashMCPTool, PythonMCPTool, StateTableQueryMCPTool, ToolRegistry
from reasoning.engine import FeatureReasoningEngine, default_reasoning_rule_path
from runtime.provider import ProviderAgentRuntime
from settings import load_settings


DEFAULT_GOAL_SUFFIX = "拿到flag给我"
FLAG_PATTERN = re.compile(r"(?i)(flag\{[^}\n]{1,256}\}|ctf\{[^}\n]{1,256}\}|flag[:=]\s*[^\s\n]{1,256})")


def apply_default_goal(feature_description: str) -> str:
    """若输入未显式包含目标，自动追加默认目标。"""
    normalized = " ".join(feature_description.strip().split())
    if not normalized:
        return DEFAULT_GOAL_SUFFIX
    if DEFAULT_GOAL_SUFFIX in normalized:
        return normalized
    if normalized.endswith((",", "，", ";", "；")):
        return f"{normalized}{DEFAULT_GOAL_SUFFIX}"
    return f"{normalized}，{DEFAULT_GOAL_SUFFIX}"


def default_mapping_path() -> Path:
    """返回默认测试家族映射配置路径。"""
    return Path(__file__).resolve().parents[1] / "config" / "test_family_mapping.json"


def _build_agent_runtime_workspaces(root: Path) -> dict[str, Path]:
    workspaces: dict[str, Path] = {}
    for agent_name in ("reasoning", "act", "parsing"):
        workspace = (root / agent_name).resolve()
        workspace.mkdir(parents=True, exist_ok=True)
        workspaces[agent_name] = workspace
    return workspaces


class SRCWorkflow:
    """把 reasoning、act、parsing 三个模块串成一个可运行流程。"""

    def __init__(
        self,
        reasoning_agent: ReasoningAgent,
        act_agent: ActAgent,
        parsing_agent: ParsingAgent,
        task_tree: TaskTree | None = None,
        state_store: StateTableStore | None = None,
        max_cycles: int = 20,
    ) -> None:
        self.reasoning_agent = reasoning_agent
        self.act_agent = act_agent
        self.parsing_agent = parsing_agent
        self.task_tree = task_tree or TaskTree()
        self.state_store = state_store or StateTableStore()
        self.max_cycles = max(1, int(max_cycles))

    def _reset_run_state(self) -> None:
        """每次新运行前重置任务树和状态表，避免跨次污染。"""
        self.task_tree = TaskTree()
        self.state_store = StateTableStore()

    def run_demo(self, feature_description: str, reasoning_hint: str | None = None) -> DemoRunResult:
        """执行一个最小演示链路。"""
        return self.run_demo_with_events(feature_description, reasoning_hint=reasoning_hint)

    def run_demo_with_events(
        self,
        feature_description: str,
        event_callback: Callable[[dict[str, Any]], None] | None = None,
        reasoning_hint: str | None = None,
    ) -> DemoRunResult:
        """执行演示链路，并在关键步骤发出实时事件。"""
        self._reset_run_state()
        effective_description = apply_default_goal(feature_description)
        normalized_hint = (reasoning_hint or "").strip()
        step = 0

        def emit(
            *,
            stage: str,
            title: str,
            status: str,
            input_data: dict[str, Any] | None = None,
            output_data: dict[str, Any] | None = None,
            error: str | None = None,
        ) -> None:
            nonlocal step
            step += 1
            if event_callback is None:
                return
            event_callback(
                {
                    "stepIndex": step,
                    "timestamp": utc_now_iso(),
                    "stage": stage,
                    "title": title,
                    "status": status,
                    "input": input_data or {},
                    "output": output_data or {},
                    "error": error,
                }
            )

        emit(
            stage="reasoning:start",
            title="开始功能点推理",
            status="running",
            input_data={
                "featureDescription": effective_description,
                "reasoningHint": normalized_hint,
            },
        )

        feature = FeaturePoint.from_description(effective_description)
        plan = self.reasoning_agent.plan_feature(
            feature,
            self.task_tree,
            planning_hint=normalized_hint,
        )

        emit(
            stage="reasoning:finish",
            title="完成功能点推理",
            status="success",
            output_data={
                "featureName": feature.name,
                "entryPoints": feature.entry_points,
                "reasoningHint": normalized_hint,
                "recommendedFamilyCount": len(plan.recommended_families),
                "agentOutput": plan.trace,
            },
        )

        parsed_result = None
        executed_node_id = None
        act_result = None
        stop_reason = "no-new-nodes"
        flag_hit: str | None = None

        cycle = 0
        while cycle < self.max_cycles:
            cycle += 1
            next_node = self.task_tree.next_todo(NodeType.INFO) or self.task_tree.next_todo(NodeType.TEST)
            if next_node is None:
                frontier_items = self._frontier_queue_items()
                if frontier_items:
                    created = self._materialize_frontier_retry_nodes(frontier_items)
                    emit(
                        stage="workflow:frontier",
                        title="frontier_queue 驱动补充重试节点",
                        status="retry",
                        output_data={
                            "cycle": cycle,
                            "frontierCount": len(frontier_items),
                            "createdRetryNodes": created,
                        },
                    )
                    continue

                stop_reason = "no-new-nodes"
                emit(
                    stage="workflow:stop",
                    title="无待执行节点，结束循环",
                    status="success",
                    output_data={"cycle": cycle - 1, "nodeCount": len(self.task_tree.model.nodes)},
                )
                break

            emit(
                stage="act:start",
                title="开始执行节点",
                status="running",
                input_data={
                    "cycle": cycle,
                    "nodeId": next_node.id,
                    "nodeTitle": next_node.title,
                    "nodeType": next_node.node_type.value,
                },
            )

            act_result = self.act_agent.execute_next(self.task_tree, self.state_store.model)
            if act_result is None:
                stop_reason = "no-new-nodes"
                break

            emit(
                stage="act:finish",
                title="节点执行完成",
                status="success" if act_result.exit_code == 0 else "failed",
                output_data={
                    "cycle": cycle,
                    "nodeId": act_result.node_id,
                    "toolName": act_result.tool_name,
                    "command": act_result.command,
                    "exitCode": act_result.exit_code,
                    "rawOutput": act_result.raw_output,
                    "agentOutput": act_result.agent_output,
                },
            )

            emit(
                stage="parsing:start",
                title="开始解析执行结果",
                status="running",
                input_data={"cycle": cycle, "nodeId": act_result.node_id},
            )

            parsed_result = self.parsing_agent.parse(act_result, self.task_tree)

            emit(
                stage="parsing:finish",
                title="解析完成",
                status="success",
                output_data={
                    "cycle": cycle,
                    "summary": parsed_result.summary,
                    "nextStatus": parsed_result.next_status.value,
                    "evidenceCount": len(parsed_result.evidence),
                    "conclusionCount": len(parsed_result.conclusions),
                    "agentOutput": "\n".join(parsed_result.state_delta.notes).strip() or None,
                },
            )

            emit(
                stage="reasoning:start",
                title="开始吸收解析结果并更新计划",
                status="running",
                input_data={
                    "cycle": cycle,
                    "nodeId": act_result.node_id,
                    "summary": parsed_result.summary,
                },
            )

            node_count_before_ingest = len(self.task_tree.model.nodes)
            self.reasoning_agent.ingest_parsed_result(
                parsed_result,
                self.task_tree,
                self.state_store,
                planning_hint=normalized_hint,
            )
            node_count_after_ingest = len(self.task_tree.model.nodes)
            new_nodes_generated = node_count_after_ingest > node_count_before_ingest
            executed_node_id = act_result.node_id

            emit(
                stage="reasoning:finish",
                title="计划更新完成",
                status="success",
                output_data={
                    "cycle": cycle,
                    "newNodesGenerated": new_nodes_generated,
                    "agentOutput": self.reasoning_agent.last_ingest_trace,
                    "stateSnapshot": {
                        "identityCount": len(self.state_store.model.identities),
                        "entrypointCount": len(self.state_store.model.key_entrypoints),
                        "sessionMaterialCount": len(self.state_store.model.session_materials),
                        "artifactCount": len(self.state_store.model.reusable_artifacts),
                    },
                },
            )

            flag_hit = self._extract_flag_value(act_result.raw_output)
            if flag_hit is None and parsed_result is not None:
                flag_hit = self._extract_flag_value(parsed_result.summary)

            if flag_hit:
                stop_reason = "flag-found"
                emit(
                    stage="workflow:stop",
                    title="命中 FLAG，结束循环",
                    status="success",
                    output_data={"flag": flag_hit, "cycle": cycle},
                )
                break

            has_pending = self.task_tree.next_todo(NodeType.INFO) is not None or self.task_tree.next_todo(NodeType.TEST) is not None
            frontier_items = self._frontier_queue_items()
            has_frontier = bool(frontier_items)
            if not has_pending and has_frontier:
                created = self._materialize_frontier_retry_nodes(frontier_items)
                if created > 0:
                    new_nodes_generated = True
                    emit(
                        stage="workflow:frontier",
                        title="frontier_queue 生成重试测试节点",
                        status="retry",
                        output_data={
                            "cycle": cycle,
                            "frontierCount": len(frontier_items),
                            "createdRetryNodes": created,
                        },
                    )

            frontier_exhausted = not bool(self._frontier_queue_items())
            if not has_pending and not new_nodes_generated and frontier_exhausted:
                stop_reason = "no-new-nodes"
                emit(
                    stage="workflow:stop",
                    title="无新节点生成，结束循环",
                    status="success",
                    output_data={
                        "cycle": cycle,
                        "nodeCount": node_count_after_ingest,
                        "frontierExhausted": frontier_exhausted,
                    },
                )
                break

        if cycle >= self.max_cycles:
            stop_reason = "max-cycles"
            emit(
                stage="workflow:guard",
                title="达到最大循环次数保护",
                status="failed",
                error=f"max_cycles={self.max_cycles}",
            )

        pending_test_count = len(
            [
                node
                for node in self.task_tree.model.nodes.values()
                if node.kind == NodeType.TEST and node.status.value == "todo"
            ]
        )
        emit(
            stage="workflow:finish",
            title="工作流结束",
            status="success",
            output_data={
                "pendingTestNodes": pending_test_count,
                "stopReason": stop_reason,
                "flag": flag_hit,
            },
        )

        return DemoRunResult(
            feature_point=feature,
            plan=plan,
            executed_node_id=executed_node_id,
            act_result=act_result,
            parsed_result=parsed_result,
            reasoning_ingest_trace=self.reasoning_agent.last_ingest_trace,
            state_table=self.state_store.model,
            task_tree=self.task_tree.model,
        )

    def _frontier_queue_items(self) -> list[dict[str, Any]]:
        model = self.state_store.model
        candidates = self._to_frontier_candidates(getattr(model, "frontier_queue", None))

        if not candidates:
            for note in reversed(model.notes[-30:]):
                parsed = self._parse_frontier_candidates_from_note(note)
                if parsed:
                    candidates = parsed
                    break

        normalized: list[dict[str, Any]] = []
        for index, item in enumerate(candidates):
            payload = self._normalize_frontier_item(item, index)
            if payload is not None:
                normalized.append(payload)
        return normalized

    def _to_frontier_candidates(self, raw_queue: Any) -> list[Any]:
        if raw_queue is None:
            return []
        if isinstance(raw_queue, list):
            return raw_queue
        if isinstance(raw_queue, tuple):
            return list(raw_queue)
        if isinstance(raw_queue, dict):
            for key in ("frontier_queue", "queue", "items", "retry_items"):
                value = raw_queue.get(key)
                if isinstance(value, list):
                    return value
            return [raw_queue]
        return []

    def _parse_frontier_candidates_from_note(self, note: str) -> list[Any]:
        text = " ".join((note or "").split())
        if not text:
            return []

        if "frontier_queue=" in text:
            payload_text = text.split("frontier_queue=", 1)[1].strip()
            try:
                payload = json.loads(payload_text)
            except Exception:
                return []
            return self._to_frontier_candidates(payload)

        try:
            payload = json.loads(text)
        except Exception:
            return []

        if isinstance(payload, dict) and "frontier_queue" in payload:
            return self._to_frontier_candidates(payload.get("frontier_queue"))
        if isinstance(payload, list):
            return payload
        return []

    def _normalize_frontier_item(self, item: Any, index: int) -> dict[str, Any] | None:
        if isinstance(item, str):
            text = " ".join(item.split())
            if not text or re.search(r"待重试|retry|pending", text, flags=re.IGNORECASE) is None:
                return None
            return {
                "retry_key": f"frontier-{index}-{text[:48].lower()}",
                "title": f"Frontier Retry #{index + 1}",
                "description": text,
                "status": "retry",
                "test_family_id": None,
                "related_feature_id": None,
                "reason": text,
            }

        if not isinstance(item, dict):
            return None

        status = " ".join(
            str(item.get("status") or item.get("state") or item.get("retry_status") or item.get("node_status") or "").split()
        ).lower()
        should_retry = bool(item.get("needs_retry") or item.get("need_retry") or item.get("retry"))
        if not should_retry and re.search(r"retry|pending|todo|待重试", status, flags=re.IGNORECASE) is None:
            retries_left = item.get("retries_left")
            try:
                retries_left_int = int(retries_left)
            except Exception:
                retries_left_int = 0
            if retries_left_int <= 0:
                return None

        title = " ".join(
            str(item.get("title") or item.get("node_title") or item.get("name") or item.get("target") or item.get("endpoint") or "").split()
        )
        if not title:
            title = f"Frontier Retry #{index + 1}"

        description = " ".join(
            str(item.get("description") or item.get("reason") or item.get("error") or item.get("command") or title).split()
        )
        retry_key = " ".join(
            str(item.get("retry_key") or item.get("id") or item.get("node_id") or f"frontier-{index}-{title.lower()}").split()
        ).lower()

        return {
            "retry_key": retry_key,
            "title": title,
            "description": description,
            "status": status or "retry",
            "test_family_id": item.get("test_family_id") or item.get("family_id") or item.get("related_test_family"),
            "related_feature_id": item.get("related_feature_id") or item.get("feature_id"),
            "reason": item.get("reason") or item.get("error") or "",
        }

    def _materialize_frontier_retry_nodes(self, frontier_items: list[dict[str, Any]]) -> int:
        created = 0
        for item in frontier_items:
            retry_key = str(item.get("retry_key") or "").strip().lower()
            title = str(item.get("title") or "Frontier Retry").strip()
            family_id = str(item.get("test_family_id") or "").strip() or None
            feature_id = str(item.get("related_feature_id") or "").strip() or None
            if self._has_frontier_retry_node(retry_key=retry_key, title=title, family_id=family_id, feature_id=feature_id):
                continue

            parent_id = self._pick_frontier_parent_id(feature_id)
            node = TaskNode(
                title=title,
                node_type=NodeType.TEST,
                source="workflow_frontier_retry",
                parent_id=parent_id,
                related_feature_id=feature_id,
                related_test_family=family_id,
                notes=[
                    "来自 frontier_queue 的待重试项。",
                    *([f"待重试原因：{str(item.get('reason') or '').strip()}"] if str(item.get("reason") or "").strip() else []),
                ],
                description=str(item.get("description") or "").strip(),
                metadata={
                    "frontier_retry_key": retry_key,
                    "frontier_status": item.get("status"),
                },
            )
            self.task_tree.add_node(node)
            created += 1

        return created

    def _has_frontier_retry_node(
        self,
        *,
        retry_key: str,
        title: str,
        family_id: str | None,
        feature_id: str | None,
    ) -> bool:
        normalized_title = " ".join(title.split()).lower()
        for node in self.task_tree.model.nodes.values():
            if node.node_type != NodeType.TEST:
                continue
            node_retry_key = " ".join(str(node.metadata.get("frontier_retry_key") or "").split()).lower()
            if retry_key and node_retry_key and node_retry_key == retry_key:
                return True

            if feature_id and node.related_feature_id and node.related_feature_id != feature_id:
                continue
            if family_id and node.related_test_family and node.related_test_family != family_id:
                continue
            if normalized_title and " ".join(node.title.split()).lower() == normalized_title:
                return True
        return False

    def _pick_frontier_parent_id(self, feature_id: str | None) -> str | None:
        if feature_id:
            for node in self.task_tree.model.nodes.values():
                if node.node_type == NodeType.INFO and node.related_feature_id == feature_id:
                    return node.id

        for node in self.task_tree.model.nodes.values():
            if node.node_type == NodeType.INFO and node.status.value != "done":
                return node.id
        for node in self.task_tree.model.nodes.values():
            if node.node_type == NodeType.INFO:
                return node.id
        return None

    def _extract_flag_value(self, text: str | None) -> str | None:
        if not text:
            return None
        matched = FLAG_PATTERN.search(text)
        if not matched:
            return None
        return matched.group(1)


def build_default_workflow(
    mapping_path: str | Path | None = None,
    max_cycles: int | None = None,
) -> SRCWorkflow:
    """构建默认工作流（直连 provider）。"""
    settings = load_settings()
    state_store = StateTableStore(StateTable())
    tools = ToolRegistry([
        PythonMCPTool(),
        BashMCPTool(),
        StateTableQueryMCPTool(lambda: state_store.model),
    ])
    workspaces = _build_agent_runtime_workspaces(settings.runtime_workspace_root)

    provider_args = {
        "model": settings.model,
        "base_url": settings.base_url,
        "auth_token": settings.anthropic_auth_token,
        "api_key": settings.anthropic_api_key,
    }
    reasoning_runtime = ProviderAgentRuntime(cwd=workspaces["reasoning"], **provider_args)
    act_runtime = ProviderAgentRuntime(cwd=workspaces["act"], **provider_args)
    parsing_runtime = ProviderAgentRuntime(cwd=workspaces["parsing"], **provider_args)

    configured_max_cycles = max_cycles if max_cycles is not None else 20

    return SRCWorkflow(
        reasoning_agent=ReasoningAgent(
            runtime=reasoning_runtime,
            mapper=TestFamilyMapper.from_file(mapping_path or default_mapping_path()),
            feature_engine=FeatureReasoningEngine.from_file(default_reasoning_rule_path()),
            tools=tools,
        ),
        act_agent=ActAgent(
            runtime=act_runtime,
            tools=tools,
        ),
        parsing_agent=ParsingAgent(runtime=parsing_runtime, tools=tools),
        task_tree=TaskTree(),
        state_store=state_store,
        max_cycles=configured_max_cycles,
    )
