from __future__ import annotations

from agents.parsing import ParsingAgent
from core.models import ActResult, AgentRuntimeResponse, NodeType, StateItem, StateTable, utc_now_iso
from core.task_tree import TaskTree
from infra.mcp import StateTableQueryMCPTool, ToolRegistry
from tests.fakes import FakeRuntime


class RecordingRuntime:
    def __init__(self) -> None:
        self.requests = []

    def run(self, request):
        self.requests.append(request)
        return AgentRuntimeResponse(
            agent_name=request.agent_name,
            content="record::parsing",
            raw={"provider": "recording"},
        )


def test_parsing_extracts_reusable_materials_into_state_delta() -> None:
    tree = TaskTree()
    node = tree.create_node(
        title="初始侦察",
        node_type=NodeType.INFO,
        source="reasoning",
        description="探测登录与API入口",
    )

    now = utc_now_iso()
    act_result = ActResult(
        node_id=node.id,
        tool_name="python",
        command="print('probe /api/login')",
        exit_code=0,
        raw_output="\n".join(
            [
                "url:http://10.50.1.182:39859/",
                "status:200",
                "body_preview:",
                '{"endpoint":"/api/login","username":"test","password":"test","token":"eyJabc12345.def6789012.ghi3456789"}',
            ]
        ),
        started_at=now,
        finished_at=now,
    )

    parsed = ParsingAgent(runtime=FakeRuntime()).parse(act_result, tree)

    identity_contents = [item.content for item in parsed.state_delta.identities]
    entrypoint_contents = [item.content for item in parsed.state_delta.key_entrypoints]
    session_contents = [item.content for item in parsed.state_delta.session_materials]
    artifact_contents = [item.content for item in parsed.state_delta.reusable_artifacts]

    assert any("test:test" in value for value in identity_contents)
    assert any("/api/login" in value for value in entrypoint_contents)
    assert any(value.startswith("eyJ") for value in session_contents)
    assert any("probe /api/login" in value for value in artifact_contents)


def test_parsing_queries_state_table_when_output_is_sparse() -> None:
    tree = TaskTree()
    node = tree.create_node(
        title="信息补全",
        node_type=NodeType.INFO,
        source="reasoning",
    )
    now = utc_now_iso()
    act_result = ActResult(
        node_id=node.id,
        tool_name="python",
        command="print('short')",
        exit_code=0,
        raw_output="ok",
        started_at=now,
        finished_at=now,
    )

    runtime = RecordingRuntime()
    table = StateTable(
        identities=[StateItem(title="账号", content="test:test")],
        key_entrypoints=[StateItem(title="API路径", content="/api/login")],
    )
    parser = ParsingAgent(
        runtime=runtime,
        tools=ToolRegistry([StateTableQueryMCPTool(lambda: table)]),
    )

    parser.parse(act_result, tree)

    latest_request = runtime.requests[-1]
    assert latest_request.context.get("available_tools") == ["state_table"]
    assert latest_request.context.get("state_table_query_result") is not None
