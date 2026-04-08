from pathlib import Path

import pytest

from agents.reasoning import ReasoningAgent
from core.mapping import TestFamilyMapper
from core.models import AgentRuntimeResponse, FeaturePoint, NodeStatus, NodeType, ParsedActResult, StateItem, StateTable, StateTableDelta
from core.state_table import StateTableStore
from core.task_tree import TaskTree
from infra.mcp import StateTableQueryMCPTool, ToolRegistry
from reasoning.engine import FeatureReasoningEngine
from reasoning.models import ParsingObservation, make_observation_item
from tests.fakes import FakeRuntime


def build_engine() -> FeatureReasoningEngine:
    return FeatureReasoningEngine.from_file(Path("config/reasoning_family_rules.json"))


class RecordingRuntime:
    """用于断言 runtime 请求上下文是否包含任务树快照。"""

    def __init__(self) -> None:
        self.requests = []

    def run(self, request):
        self.requests.append(request)
        return AgentRuntimeResponse(
            agent_name=request.agent_name,
            content=f"record::{request.agent_name}",
            raw={"provider": "recording"},
        )


@pytest.mark.parametrize(
    ("observation", "expected_primary_family", "expected_secondary_families"),
    [
        (
            ParsingObservation(
                discovered_endpoints=[make_observation_item("/api/users/{user_id}", "e1")],
                discovered_actions=[make_observation_item("view user detail", "e2")],
            ),
            "object_access_control",
            [],
        ),
        (
            ParsingObservation(
                discovered_actions=[make_observation_item("edit profile", "e1")],
                discovered_fields=[
                    make_observation_item("nickname", "e2"),
                    make_observation_item("avatar", "e3"),
                    make_observation_item("signature", "e4"),
                    make_observation_item("role", "e5"),
                ],
            ),
            "property_access_control",
            [],
        ),
        (
            ParsingObservation(
                discovered_actions=[make_observation_item("admin export all orders", "e1")],
                discovered_roles=[make_observation_item("admin", "e2")],
                discovered_objects=[make_observation_item("orders", "e3")],
            ),
            "function_access_control",
            ["quota_abuse_logic"],
        ),
        (
            ParsingObservation(
                discovered_flows=[make_observation_item("apply -> approve order", "e1")],
                discovered_actions=[make_observation_item("approve order", "e2")],
            ),
            "workflow_state_logic",
            ["function_access_control"],
        ),
        (
            ParsingObservation(
                discovered_actions=[make_observation_item("send code by sms", "e1")],
                discovered_endpoints=[make_observation_item("/api/send-code", "e2")],
            ),
            "quota_abuse_logic",
            [],
        ),
        (
            ParsingObservation(
                discovered_actions=[make_observation_item("search users", "e1")],
                discovered_fields=[make_observation_item("query", "e2"), make_observation_item("filter", "e3")],
            ),
            "server_input_interpretation",
            [],
        ),
        (
            ParsingObservation(
                discovered_upload_points=[make_observation_item("upload attachment", "e1")],
                discovered_actions=[make_observation_item("preview attachment", "e2")],
            ),
            "file_content_handling",
            [],
        ),
        (
            ParsingObservation(
                discovered_flows=[make_observation_item("login and token refresh flow", "e1")],
                discovered_endpoints=[make_observation_item("/api/token/refresh", "e2")],
            ),
            "auth_session_security",
            [],
        ),
        (
            ParsingObservation(
                discovered_render_points=[make_observation_item("comment markdown display", "e1")],
                discovered_actions=[make_observation_item("render comment preview", "e2")],
            ),
            "client_render_execution",
            ["file_content_handling"],
        ),
        (
            ParsingObservation(
                discovered_callback_points=[make_observation_item("webhook callback url configuration", "e1")],
                discovered_fields=[make_observation_item("callback url", "e2")],
            ),
            "server_outbound_callback",
            [],
        ),
    ],
)
def test_reasoning_engine_maps_feature_cases(
    observation: ParsingObservation,
    expected_primary_family: str,
    expected_secondary_families: list[str],
) -> None:
    decision = build_engine().analyze(observation)

    assert len(decision.identified_features) >= 1
    assert len(decision.family_mapping) >= 1
    assert decision.family_mapping[0].primary_family_id == expected_primary_family
    assert decision.proposed_test_nodes[0].node_type.value == "test"
    assert decision.proposed_test_nodes[0].primary_family_id == expected_primary_family
    assert decision.family_mapping[0].reasons
    for family_id in expected_secondary_families:
        assert family_id in decision.family_mapping[0].family_ids


def test_reasoning_engine_supports_multiple_features_in_one_observation() -> None:
    decision = build_engine().analyze(
        ParsingObservation(
            discovered_actions=[make_observation_item("login", "e1")],
            discovered_callback_points=[make_observation_item("webhook callback url", "e2")],
        )
    )

    primary_families = {item.primary_family_id for item in decision.family_mapping}

    assert len(decision.identified_features) == 2
    assert "auth_session_security" in primary_families
    assert "server_outbound_callback" in primary_families
    assert len(decision.proposed_test_nodes) == 2


def test_reasoning_engine_maps_family_from_typical_feature_example() -> None:
    decision = build_engine().analyze(
        ParsingObservation(
            discovered_pages=[make_observation_item("优惠领取中心", "e1")],
        )
    )

    assert decision.family_mapping
    assert decision.family_mapping[0].primary_family_id == "workflow_state_logic"
    assert any("典型功能点例子" in reason for reason in decision.family_mapping[0].reasons)


def test_reasoning_agent_exposes_structured_observation_entrypoint() -> None:
    engine = build_engine()
    reasoning_agent = ReasoningAgent(
        runtime=FakeRuntime(),
        mapper=TestFamilyMapper.from_file(Path("config/test_family_mapping.json")),
        feature_engine=engine,
    )

    decision = reasoning_agent.analyze_structured_observation(
        ParsingObservation(
            discovered_actions=[make_observation_item("search users", "e1")],
            discovered_fields=[make_observation_item("query", "e2"), make_observation_item("filter", "e3")],
        )
    )

    assert decision.family_mapping[0].primary_family_id == "server_input_interpretation"
    assert decision.proposed_test_nodes[0].family_ids[0] == "server_input_interpretation"


def test_reasoning_agent_plan_feature_reads_task_tree_and_avoids_duplicate_nodes() -> None:
    runtime = RecordingRuntime()
    agent = ReasoningAgent(
        runtime=runtime,
        mapper=TestFamilyMapper.from_file(Path("config/test_family_mapping.json")),
    )
    task_tree = TaskTree()
    feature = FeaturePoint.from_description("Admin login endpoint /api/login exposes username password captcha")

    first_plan = agent.plan_feature(feature, task_tree)
    initial_node_count = len(task_tree.model.nodes)
    second_plan = agent.plan_feature(feature, task_tree)

    assert second_plan.info_node.id == first_plan.info_node.id
    assert len(task_tree.model.nodes) == initial_node_count

    signatures = [
        (node.related_feature_id, node.related_test_family)
        for node in task_tree.model.nodes.values()
        if node.node_type == NodeType.TEST
    ]
    assert len(signatures) == len(set(signatures))

    latest_request = runtime.requests[-1]
    assert "task_tree_snapshot" in latest_request.context
    assert latest_request.context["task_tree_snapshot"]["summary"]["nodeCount"] >= initial_node_count


def test_reasoning_agent_url_only_goal_creates_info_node_first() -> None:
    agent = ReasoningAgent(
        runtime=FakeRuntime(),
        mapper=TestFamilyMapper.from_file(Path("config/test_family_mapping.json")),
    )
    task_tree = TaskTree()
    feature = FeaturePoint.from_description("http://10.50.1.182:39859/，拿到flag给我")

    plan = agent.plan_feature(feature, task_tree)

    assert plan.info_node.node_type == NodeType.INFO
    assert plan.test_nodes == []
    assert plan.recommended_families == []
    assert all(node.node_type != NodeType.TEST for node in task_tree.model.nodes.values())


def test_reasoning_agent_ingest_includes_task_tree_snapshot_context() -> None:
    runtime = RecordingRuntime()
    agent = ReasoningAgent(
        runtime=runtime,
        mapper=TestFamilyMapper.from_file(Path("config/test_family_mapping.json")),
    )
    task_tree = TaskTree()
    source = task_tree.create_node(
        title="功能点：登录",
        node_type=NodeType.INFO,
        source="reasoning",
        related_feature_id="feat-login",
    )
    parsed_result = ParsedActResult(node_id=source.id, summary="status:200", next_status=NodeStatus.DONE)

    agent.ingest_parsed_result(parsed_result, task_tree, StateTableStore())

    latest_request = runtime.requests[-1]
    assert latest_request.context["source_node"]["id"] == source.id
    assert latest_request.context["task_tree_snapshot"]["summary"]["nodeCount"] >= 1


def test_reasoning_agent_creates_post_login_recon_node_when_auth_clean_and_credentials_exist() -> None:
    runtime = RecordingRuntime()
    agent = ReasoningAgent(
        runtime=runtime,
        mapper=TestFamilyMapper.from_file(Path("config/test_family_mapping.json")),
    )
    task_tree = TaskTree()
    feature_info = task_tree.create_node(
        title="功能点：登录",
        node_type=NodeType.INFO,
        source="reasoning",
        related_feature_id="feat-login",
    )
    auth_test = task_tree.create_node(
        title="测试 Authentication Bypass",
        node_type=NodeType.TEST,
        source="reasoning",
        parent_id=feature_info.id,
        related_feature_id="feat-login",
        related_test_family="auth_bypass",
    )

    parsed_result = ParsedActResult(
        node_id=auth_test.id,
        summary="认证测试完成，未发现明显异常。",
        next_status=NodeStatus.DONE,
        state_delta=StateTableDelta(
            identities=[StateItem(title="账号密码线索", content="test:test")],
            key_entrypoints=[StateItem(title="API路径", content="/api/login")],
        ),
    )

    state_store = StateTableStore()
    agent.ingest_parsed_result(parsed_result, task_tree, state_store)

    post_login_nodes = [
        node
        for node in task_tree.model.nodes.values()
        if node.node_type == NodeType.INFO and node.source == "reasoning_post_login"
    ]
    assert post_login_nodes
    assert "登录后侦察" in post_login_nodes[0].title


def test_reasoning_agent_queries_state_table_when_info_is_insufficient() -> None:
    runtime = RecordingRuntime()
    table = StateTable(
        identities=[StateItem(title="账号", content="test:test")],
        key_entrypoints=[StateItem(title="API路径", content="/api/login")],
    )
    tools = ToolRegistry([StateTableQueryMCPTool(lambda: table)])
    agent = ReasoningAgent(
        runtime=runtime,
        mapper=TestFamilyMapper.from_file(Path("config/test_family_mapping.json")),
        tools=tools,
    )
    task_tree = TaskTree()
    feature = FeaturePoint.from_description("http://10.50.1.182:39859/，拿到flag给我")

    agent.plan_feature(feature, task_tree)

    latest_request = runtime.requests[-1]
    assert latest_request.context.get("available_tools") == ["state_table"]
    assert latest_request.context.get("state_table_query_result") is not None


def test_reasoning_agent_hint_drives_planning_for_url_only_goal() -> None:
    agent = ReasoningAgent(
        runtime=FakeRuntime(),
        mapper=TestFamilyMapper.from_file(Path("config/test_family_mapping.json")),
    )
    task_tree = TaskTree()
    feature = FeaturePoint.from_description("http://10.50.1.182:39859/，拿到flag给我")

    plan = agent.plan_feature(
        feature,
        task_tree,
        planning_hint="存在登录与 token 刷新接口，优先继续认证和会话安全规划",
    )

    assert plan.recommended_families
    assert plan.test_nodes
    family_ids = {node.related_test_family for node in plan.test_nodes if node.related_test_family}
    assert "auth_bypass" in family_ids or "auth_session_security" in family_ids


def test_reasoning_agent_ingest_expands_test_nodes_from_hint() -> None:
    runtime = RecordingRuntime()
    agent = ReasoningAgent(
        runtime=runtime,
        mapper=TestFamilyMapper.from_file(Path("config/test_family_mapping.json")),
    )
    task_tree = TaskTree()
    info_node = task_tree.create_node(
        title="功能点：文件中心",
        node_type=NodeType.INFO,
        source="reasoning",
        related_feature_id="feat-file",
    )
    parsed_result = ParsedActResult(node_id=info_node.id, summary="信息收集完成", next_status=NodeStatus.DONE)

    agent.ingest_parsed_result(
        parsed_result,
        task_tree,
        StateTableStore(),
        planning_hint="页面存在上传附件与预览能力，继续围绕上传解析链规划",
    )

    hinted_nodes = [
        node
        for node in task_tree.model.nodes.values()
        if node.node_type == NodeType.TEST and node.source == "reasoning_hint"
    ]
    assert hinted_nodes
    assert any(node.related_test_family == "file_upload" for node in hinted_nodes)


def test_reasoning_agent_writes_high_priority_hint_into_test_nodes() -> None:
    agent = ReasoningAgent(
        runtime=FakeRuntime(),
        mapper=TestFamilyMapper.from_file(Path("config/test_family_mapping.json")),
    )
    task_tree = TaskTree()
    feature = FeaturePoint.from_description("Admin login endpoint /api/login with username password captcha")

    plan = agent.plan_feature(
        feature,
        task_tree,
        planning_hint="优先沿着提示推进认证链路并拿到flag给我",
    )

    assert plan.test_nodes
    assert any(
        any("高优先级提示：" in note for note in node.notes)
        for node in plan.test_nodes
    )


def test_reasoning_agent_hint_guidance_avoids_unlikely_family_expansion() -> None:
    agent = ReasoningAgent(
        runtime=FakeRuntime(),
        mapper=TestFamilyMapper.from_file(Path("config/test_family_mapping.json")),
        feature_engine=build_engine(),
    )
    task_tree = TaskTree()
    feature = FeaturePoint.from_description(
        "Admin login endpoint /api/login?id=1 uses username password captcha token"
    )

    plan = agent.plan_feature(
        feature,
        task_tree,
        planning_hint="优先认证与会话安全，不要无关家族，目标拿到flag",
    )

    family_ids = [item.family.id for item in plan.recommended_families]
    assert family_ids
    assert family_ids[0] in {"auth_bypass", "session_management"}
    assert "file_upload" not in family_ids
