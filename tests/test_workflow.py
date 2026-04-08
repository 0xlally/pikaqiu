from agents.act import ActAgent
from agents.parsing import ParsingAgent
from agents.reasoning import ReasoningAgent
from core.models import ActResult, NodeStatus, NodeType, utc_now_iso
from core.mapping import TestFamilyMapper
from core.state_table import StateTableStore
from core.task_tree import TaskTree
from infra.mcp import PythonMCPTool, ToolRegistry
from reasoning.engine import FeatureReasoningEngine
from tests.fakes import FakeRuntime
from workflow import SRCWorkflow, apply_default_goal


class ScriptedActAgent:
    """用脚本化输出模拟 act 执行结果，避免测试依赖真实网络。"""

    def execute_next(self, task_tree: TaskTree, state_table=None) -> ActResult | None:
        node = task_tree.next_todo(NodeType.INFO) or task_tree.next_todo(NodeType.TEST)
        if node is None:
            return None

        now = utc_now_iso()
        if node.node_type == NodeType.INFO:
            raw_output = "\n".join(
                [
                    "url:http://10.50.1.182:39859/",
                    "status:200",
                    "body_preview:",
                    "<!-- TODO: Delete the testing account (test:test). -->",
                    "<title>Login - Trading Platform</title>",
                ]
            )
        else:
            raw_output = f"type:test\\nfamily:{node.related_test_family or '-'}\\nstatus:200"

        return ActResult(
            node_id=node.id,
            tool_name="python",
            command="print('scripted')",
            exit_code=0,
            raw_output=raw_output,
            agent_output="scripted",
            started_at=now,
            finished_at=now,
        )


def test_demo_workflow_executes_info_node_before_test_node() -> None:
    workflow = SRCWorkflow(
        reasoning_agent=ReasoningAgent(
            runtime=FakeRuntime(),
            mapper=TestFamilyMapper.from_file("config/test_family_mapping.json"),
            feature_engine=FeatureReasoningEngine.from_file("config/reasoning_family_rules.json"),
        ),
        act_agent=ActAgent(
            runtime=FakeRuntime(),
            tools=ToolRegistry([PythonMCPTool()]),
        ),
        parsing_agent=ParsingAgent(runtime=FakeRuntime()),
        task_tree=TaskTree(),
        state_store=StateTableStore(),
    )
    result = workflow.run_demo(
        "Admin login endpoint /api/login exposes username password captcha and token-based session handling."
    )

    assert result.plan.recommended_families
    assert result.executed_node_id is not None
    assert result.parsed_result is not None
    assert result.act_result is not None
    assert result.task_tree.nodes[result.executed_node_id].status == NodeStatus.DONE

    done_info_nodes = [
        node
        for node in result.task_tree.nodes.values()
        if node.kind == NodeType.INFO and node.status == NodeStatus.DONE
    ]
    assert done_info_nodes

    pending_test_nodes = [
        node
        for node in result.task_tree.nodes.values()
        if node.kind == NodeType.TEST and node.status == NodeStatus.TODO
    ]
    assert not pending_test_nodes
    done_test_nodes = [
        node
        for node in result.task_tree.nodes.values()
        if node.kind == NodeType.TEST and node.status == NodeStatus.DONE
    ]
    assert done_test_nodes
    assert result.state_table.key_entries
    assert result.state_table.risk_hints


def test_act_agent_executes_test_node_when_no_info_node_exists() -> None:
    tree = TaskTree()
    test_node = tree.create_node(
        title="测试 access_control",
        node_type=NodeType.TEST,
        source="reasoning",
        related_feature_id="feat-1",
        related_test_family="access_control",
    )
    agent = ActAgent(
        runtime=FakeRuntime(),
        tools=ToolRegistry([PythonMCPTool()]),
    )

    result = agent.execute_next(tree)

    assert result is not None
    assert result.node_id == test_node.id
    assert "[RAG] retriever_called=yes" in result.raw_output
    assert "[ACT] access_control probe started" in result.raw_output


def test_apply_default_goal_appends_flag_objective_once() -> None:
    assert apply_default_goal("http://10.50.1.182:39859/") == "http://10.50.1.182:39859/，拿到flag给我"
    assert apply_default_goal("http://10.50.1.182:39859/,拿到flag给我") == "http://10.50.1.182:39859/,拿到flag给我"


def test_workflow_state_isolated_between_runs() -> None:
    workflow = SRCWorkflow(
        reasoning_agent=ReasoningAgent(
            runtime=FakeRuntime(),
            mapper=TestFamilyMapper.from_file("config/test_family_mapping.json"),
            feature_engine=FeatureReasoningEngine.from_file("config/reasoning_family_rules.json"),
        ),
        act_agent=ActAgent(
            runtime=FakeRuntime(),
            tools=ToolRegistry([PythonMCPTool()]),
        ),
        parsing_agent=ParsingAgent(runtime=FakeRuntime()),
        task_tree=TaskTree(),
        state_store=StateTableStore(),
    )

    first = workflow.run_demo("test feature one")
    second = workflow.run_demo("test feature two")

    assert first.feature_point.id != second.feature_point.id
    assert first.task_tree.nodes != second.task_tree.nodes


def test_workflow_generates_test_nodes_from_parsed_http_evidence() -> None:
    workflow = SRCWorkflow(
        reasoning_agent=ReasoningAgent(
            runtime=FakeRuntime(),
            mapper=TestFamilyMapper.from_file("config/test_family_mapping.json"),
            feature_engine=FeatureReasoningEngine.from_file("config/reasoning_family_rules.json"),
        ),
        act_agent=ScriptedActAgent(),
        parsing_agent=ParsingAgent(runtime=FakeRuntime()),
        task_tree=TaskTree(),
        state_store=StateTableStore(),
    )

    result = workflow.run_demo("http://10.50.1.182:39859/")

    test_nodes = [node for node in result.task_tree.nodes.values() if node.kind == NodeType.TEST]
    assert test_nodes
    assert any(node.status == NodeStatus.DONE for node in test_nodes)

    family_ids = {node.test_family_id for node in test_nodes if node.test_family_id}
    assert "auth_bypass" in family_ids
    assert "session_management" in family_ids


def test_workflow_emits_reasoning_events_after_parsing() -> None:
    workflow = SRCWorkflow(
        reasoning_agent=ReasoningAgent(
            runtime=FakeRuntime(),
            mapper=TestFamilyMapper.from_file("config/test_family_mapping.json"),
            feature_engine=FeatureReasoningEngine.from_file("config/reasoning_family_rules.json"),
        ),
        act_agent=ScriptedActAgent(),
        parsing_agent=ParsingAgent(runtime=FakeRuntime()),
        task_tree=TaskTree(),
        state_store=StateTableStore(),
    )

    events: list[dict[str, object]] = []
    workflow.run_demo_with_events("http://10.50.1.182:39859/", event_callback=events.append)

    stages = [str(item.get("stage")) for item in events]
    assert "parsing:finish" in stages
    assert "reasoning:start" in stages
    assert "reasoning:finish" in stages

    parsing_finish_positions = [idx for idx, stage in enumerate(stages) if stage == "parsing:finish"]
    reasoning_start_positions = [idx for idx, stage in enumerate(stages) if stage == "reasoning:start"]
    reasoning_finish_positions = [idx for idx, stage in enumerate(stages) if stage == "reasoning:finish"]

    matched = False
    for parsing_idx in parsing_finish_positions:
        starts_after = [idx for idx in reasoning_start_positions if idx > parsing_idx]
        if not starts_after:
            continue
        start_idx = starts_after[0]
        finishes_after = [idx for idx in reasoning_finish_positions if idx > start_idx]
        if finishes_after:
            matched = True
            break

    assert matched
