from agents.act import ActAgent
from agents.parsing import ParsingAgent
from agents.reasoning import ReasoningAgent
from core.models import NodeStatus, NodeType
from core.mapping import TestFamilyMapper
from core.state_table import StateTableStore
from core.task_tree import TaskTree
from infra.mcp import PythonMCPTool, ToolRegistry
from reasoning.engine import FeatureReasoningEngine
from tests.fakes import FakeRuntime
from workflow import SRCWorkflow, apply_default_goal


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
    assert result.task_tree.nodes[result.executed_node_id].kind == NodeType.INFO

    pending_test_nodes = [
        node
        for node in result.task_tree.nodes.values()
        if node.kind == NodeType.TEST and node.status == NodeStatus.TODO
    ]
    assert pending_test_nodes
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
    assert "type:test" in result.raw_output


def test_apply_default_goal_appends_flag_objective_once() -> None:
    assert apply_default_goal("http://10.50.1.182:39859/") == "http://10.50.1.182:39859/，拿到flag给我"
    assert apply_default_goal("http://10.50.1.182:39859/,拿到flag给我") == "http://10.50.1.182:39859/,拿到flag给我"
