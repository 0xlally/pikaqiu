from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

from agents.act import ActAgent
from agents.parsing import ParsingAgent
from agents.reasoning import ReasoningAgent
from core.mapping import TestFamilyMapper
from core.models import DemoRunResult, FeaturePoint, NodeType, StateTable, utc_now_iso
from core.state_table import StateTableStore
from core.task_tree import TaskTree
from infra.mcp import BashMCPTool, PythonMCPTool, ToolRegistry
from reasoning.engine import FeatureReasoningEngine, default_reasoning_rule_path
from runtime.provider import ProviderAgentRuntime
from settings import load_settings


DEFAULT_GOAL_SUFFIX = "拿到flag给我"


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
    ) -> None:
        self.reasoning_agent = reasoning_agent
        self.act_agent = act_agent
        self.parsing_agent = parsing_agent
        self.task_tree = task_tree or TaskTree()
        self.state_store = state_store or StateTableStore()

    def run_demo(self, feature_description: str) -> DemoRunResult:
        """执行一个最小演示链路。"""
        return self.run_demo_with_events(feature_description)

    def run_demo_with_events(
        self,
        feature_description: str,
        event_callback: Callable[[dict[str, Any]], None] | None = None,
    ) -> DemoRunResult:
        """执行演示链路，并在关键步骤发出实时事件。"""
        effective_description = apply_default_goal(feature_description)
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
            input_data={"featureDescription": effective_description},
        )

        feature = FeaturePoint.from_description(effective_description)
        plan = self.reasoning_agent.plan_feature(feature, self.task_tree)

        emit(
            stage="reasoning:finish",
            title="完成功能点推理",
            status="success",
            output_data={
                "featureName": feature.name,
                "entryPoints": feature.entry_points,
                "recommendedFamilyCount": len(plan.recommended_families),
                "agentOutput": plan.trace,
            },
        )

        next_node = self.task_tree.next_todo(NodeType.INFO) or self.task_tree.next_todo(NodeType.TEST)
        emit(
            stage="act:start",
            title="开始执行节点",
            status="running",
            input_data={
                "nodeId": next_node.id if next_node else None,
                "nodeTitle": next_node.title if next_node else None,
                "nodeType": next_node.node_type.value if next_node else None,
            },
        )

        act_result = self.act_agent.execute_next(self.task_tree)

        if act_result is None:
            emit(
                stage="act:finish",
                title="无可执行节点",
                status="success",
                output_data={"message": "当前没有可执行节点"},
            )

        parsed_result = None
        executed_node_id = None
        if act_result is not None:
            emit(
                stage="act:finish",
                title="节点执行完成",
                status="success" if act_result.exit_code == 0 else "failed",
                output_data={
                    "nodeId": act_result.node_id,
                    "toolName": act_result.tool_name,
                    "command": act_result.command,
                    "exitCode": act_result.exit_code,
                    "rawOutput": act_result.raw_output,
                },
            )

            emit(
                stage="parsing:start",
                title="开始解析执行结果",
                status="running",
                input_data={"nodeId": act_result.node_id},
            )

            parsed_result = self.parsing_agent.parse(act_result, self.task_tree)
            self.reasoning_agent.ingest_parsed_result(parsed_result, self.task_tree, self.state_store)
            executed_node_id = act_result.node_id

            emit(
                stage="parsing:finish",
                title="解析完成",
                status="success",
                output_data={
                    "summary": parsed_result.summary,
                    "nextStatus": parsed_result.next_status.value,
                    "evidenceCount": len(parsed_result.evidence),
                    "conclusionCount": len(parsed_result.conclusions),
                },
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
            output_data={"pendingTestNodes": pending_test_count},
        )

        return DemoRunResult(
            feature_point=feature,
            plan=plan,
            executed_node_id=executed_node_id,
            act_result=act_result,
            parsed_result=parsed_result,
            state_table=self.state_store.model,
            task_tree=self.task_tree.model,
        )


def build_default_workflow(mapping_path: str | Path | None = None) -> SRCWorkflow:
    """构建默认工作流（直连 provider）。"""
    settings = load_settings()
    tools = ToolRegistry([PythonMCPTool(), BashMCPTool()])
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

    return SRCWorkflow(
        reasoning_agent=ReasoningAgent(
            runtime=reasoning_runtime,
            mapper=TestFamilyMapper.from_file(mapping_path or default_mapping_path()),
            feature_engine=FeatureReasoningEngine.from_file(default_reasoning_rule_path()),
        ),
        act_agent=ActAgent(
            runtime=act_runtime,
            tools=tools,
        ),
        parsing_agent=ParsingAgent(runtime=parsing_runtime),
        task_tree=TaskTree(),
        state_store=StateTableStore(StateTable()),
    )
