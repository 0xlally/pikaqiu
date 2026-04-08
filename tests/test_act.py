from __future__ import annotations

from agents.act import ActAgent
from core.models import AgentRuntimeResponse, NodeType, StateItem, StateTable
from core.task_tree import TaskTree
from infra.mcp import PythonMCPTool, StateTableQueryMCPTool, ToolRegistry


class ScriptedRuntime:
    def __init__(self, content: str) -> None:
        self.content = content
        self.requests = []

    def run(self, request):
        self.requests.append(request)
        return AgentRuntimeResponse(
            agent_name=request.agent_name,
            content=self.content,
            raw={"provider": "scripted"},
        )


def test_act_rejects_test_command_with_unknown_endpoint() -> None:
    tree = TaskTree()
    tree.create_node(
        title="测试认证链路",
        node_type=NodeType.TEST,
        source="reasoning",
        related_feature_id="feat-login",
        related_test_family="auth_bypass",
        description="基于 /api/login 进行认证测试",
    )

    runtime = ScriptedRuntime(
        '{"tool_name":"python","command":"print(\'try /admin/panel\')"}'
    )
    agent = ActAgent(runtime=runtime, tools=ToolRegistry([PythonMCPTool()]))

    result = agent.execute_next(tree)

    assert result is not None
    assert "fallback execution path used" in result.raw_output
    assert "/admin/panel" not in result.command


def test_act_accepts_test_command_with_known_endpoint() -> None:
    tree = TaskTree()
    tree.create_node(
        title="测试认证链路",
        node_type=NodeType.TEST,
        source="reasoning",
        related_feature_id="feat-login",
        related_test_family="auth_bypass",
        description="基于 /api/login 进行认证测试",
    )

    runtime = ScriptedRuntime(
        '{"tool_name":"python","command":"print(\'/api/login\')"}'
    )
    agent = ActAgent(runtime=runtime, tools=ToolRegistry([PythonMCPTool()]))

    result = agent.execute_next(tree)

    assert result is not None
    assert "/api/login" in result.command
    assert "fallback execution path used" not in result.raw_output
    assert "/api/login" in result.raw_output


def test_act_context_includes_mutable_parameters_for_access_control() -> None:
    tree = TaskTree()
    tree.create_node(
        title="测试越权接口",
        node_type=NodeType.TEST,
        source="reasoning",
        related_feature_id="feat-acl",
        related_test_family="object_access_control",
        description="GET /api/orders/{order_id}?user_id=1001&tenant_id=t1",
        notes=["尝试替换 user_id, tenant_id, order_id 观察数据边界"],
    )

    runtime = ScriptedRuntime(
        '{"tool_name":"python","command":"print(\'/api/orders\')"}'
    )
    agent = ActAgent(runtime=runtime, tools=ToolRegistry([PythonMCPTool()]))

    result = agent.execute_next(tree)

    assert result is not None
    assert runtime.requests
    context = runtime.requests[-1].context
    mutable = context.get("mutable_parameters") or {}
    discovered = mutable.get("discovered") or []
    family_priority = mutable.get("family_priority") or []
    recommended = mutable.get("recommended_for_this_node") or []

    assert "order_id" in discovered
    assert "user_id" in discovered
    assert "tenant_id" in discovered
    assert "user_id" in family_priority
    assert "tenant_id" in family_priority
    assert "order_id" in recommended


def test_act_context_includes_state_table_snapshot() -> None:
    tree = TaskTree()
    tree.create_node(
        title="测试认证链路",
        node_type=NodeType.TEST,
        source="reasoning",
        related_feature_id="feat-auth",
        related_test_family="auth_session_security",
        description="基于 /api/login 与 /api/token/refresh 验证会话",
    )

    runtime = ScriptedRuntime(
        '{"tool_name":"python","command":"print(\'/api/login\')"}'
    )
    agent = ActAgent(runtime=runtime, tools=ToolRegistry([PythonMCPTool()]))
    state_table = StateTable(
        identities=[StateItem(title="账号", content="test:test", refs=["e-cred"])],
        key_entrypoints=[StateItem(title="API路径", content="/api/login", refs=["e-api"])],
        session_materials=[StateItem(title="JWT线索", content="eyJ.header.payload", refs=["e-jwt"])],
    )

    result = agent.execute_next(tree, state_table)

    assert result is not None
    context = runtime.requests[-1].context
    snapshot = context.get("state_table_snapshot") or {}
    assert snapshot
    assert snapshot.get("identities")
    assert snapshot.get("key_entrypoints")
    assert snapshot.get("session_materials")


def test_act_uses_state_table_tool_when_info_is_insufficient() -> None:
    tree = TaskTree()
    tree.create_node(
        title="测试认证链路",
        node_type=NodeType.TEST,
        source="reasoning",
        related_feature_id="feat-auth",
        related_test_family="auth_session_security",
        description="登录后继续收集信息",
    )

    runtime = ScriptedRuntime("not-json-response")
    state_table = StateTable(
        identities=[StateItem(title="账号", content="test:test", refs=["e-cred"])],
        key_entrypoints=[StateItem(title="API路径", content="/api/login", refs=["e-api"])],
    )
    agent = ActAgent(
        runtime=runtime,
        tools=ToolRegistry([PythonMCPTool(), StateTableQueryMCPTool(lambda: state_table)]),
    )

    result = agent.execute_next(tree, state_table)

    assert result is not None
    assert result.tool_name == "state_table"
    assert result.exit_code == 0
    assert "query" in result.raw_output


def test_act_includes_rag_family_techniques_for_test_node() -> None:
    tree = TaskTree()
    tree.create_node(
        title="测试对象越权",
        node_type=NodeType.TEST,
        source="reasoning",
        related_feature_id="feat-idor",
        related_test_family="object_access_control",
        description="围绕 /api/orders/{order_id} 做 ID 替换测试",
    )

    calls: list[tuple[str, str, str]] = []

    def fake_rag_retriever(family_id: str, node_title: str, node_description: str):
        calls.append((family_id, node_title, node_description))
        return [
            {
                "id": "rag\\vulnerabilities\\idor.md::chunk::1",
                "doc_id": "rag\\vulnerabilities\\idor.md",
                "score": 1.9,
                "snippet": "Two-account test for IDOR: Account B replays Account A resource ID.",
                "query": "object_access_control exploit technique",
            }
        ]

    runtime = ScriptedRuntime(
        '{"tool_name":"python","command":"print(\'/api/orders\')"}'
    )
    agent = ActAgent(
        runtime=runtime,
        tools=ToolRegistry([PythonMCPTool()]),
        rag_retriever=fake_rag_retriever,
    )

    result = agent.execute_next(tree)

    assert result is not None
    assert calls
    assert calls[0][0] == "object_access_control"
    assert "[RAG] retriever_called=yes" in result.raw_output
    assert "[RAG] family_id=object_access_control" in result.raw_output

    context = runtime.requests[-1].context
    rag_techniques = context.get("family_rag_techniques") or []
    assert rag_techniques
    assert "IDOR" in rag_techniques[0]["snippet"]


def test_act_skips_rag_retrieval_for_info_node() -> None:
    tree = TaskTree()
    tree.create_node(
        title="登录后信息收集",
        node_type=NodeType.INFO,
        source="reasoning",
        description="先探测 /api/login",
    )

    calls = {"count": 0}

    def fake_rag_retriever(family_id: str, node_title: str, node_description: str):
        calls["count"] += 1
        return []

    runtime = ScriptedRuntime(
        '{"tool_name":"python","command":"print(\'/api/login\')"}'
    )
    agent = ActAgent(
        runtime=runtime,
        tools=ToolRegistry([PythonMCPTool()]),
        rag_retriever=fake_rag_retriever,
    )

    result = agent.execute_next(tree)

    assert result is not None
    assert calls["count"] == 0
    context = runtime.requests[-1].context
    assert context.get("family_rag_techniques") == []


def test_act_handles_url_with_chinese_punctuation_in_notes() -> None:
    tree = TaskTree()
    tree.create_node(
        title="测试认证链路",
        node_type=NodeType.TEST,
        source="reasoning",
        related_feature_id="feat-auth",
        related_test_family="auth_bypass",
        description="基于目标地址进行认证测试",
        notes=["http://10.50.1.182:38921，拿到flag给我\n上下文（JSON）：{...}"],
    )

    runtime = ScriptedRuntime(
        '{"tool_name":"python","command":"print(\'/api/login\')"}'
    )
    agent = ActAgent(runtime=runtime, tools=ToolRegistry([PythonMCPTool()]))

    result = agent.execute_next(tree)

    assert result is not None
    assert runtime.requests


def test_act_parses_command_json_from_verbose_trace() -> None:
    tree = TaskTree()
    tree.create_node(
        title="测试认证链路",
        node_type=NodeType.TEST,
        source="reasoning",
        related_feature_id="feat-auth",
        related_test_family="auth_bypass",
        description="基于 /api/login 进行认证测试",
    )

    runtime = ScriptedRuntime(
        "\n".join(
            [
                "这里先输出一些分析文字。",
                '{"node_id":"x","node_type":"test"}',
                "最终动作如下：",
                '{"tool_name":"python","command":"print(\\"ok\\")"}',
            ]
        )
    )
    agent = ActAgent(runtime=runtime, tools=ToolRegistry([PythonMCPTool()]))

    result = agent.execute_next(tree)

    assert result is not None
    assert result.command == 'print("ok")'
    assert result.raw_output.strip().endswith("ok")
    assert "[RAG] retriever_called=yes" in result.raw_output


def test_act_passes_priority_hints_from_ancestor_info_node() -> None:
    tree = TaskTree()
    info = tree.create_node(
        title="功能点：订单中心",
        node_type=NodeType.INFO,
        source="reasoning",
        related_feature_id="feat-order",
        notes=["高优先级提示：跟随提示优先改 order_id，最终拿到flag给我"],
    )
    tree.create_node(
        title="测试对象越权",
        node_type=NodeType.TEST,
        source="reasoning",
        parent_id=info.id,
        related_feature_id="feat-order",
        related_test_family="object_access_control",
        description="围绕 /api/orders/{order_id} 做对象替换",
    )

    runtime = ScriptedRuntime(
        '{"tool_name":"python","command":"print(\"/api/orders\")"}'
    )
    agent = ActAgent(runtime=runtime, tools=ToolRegistry([PythonMCPTool()]))

    result = agent.execute_next(tree)

    assert result is not None
    context = runtime.requests[-1].context
    hints = context.get("priority_hints") or []
    assert hints
    assert any("拿到flag" in hint for hint in hints)


def test_act_does_not_reuse_example_hint_url_as_runtime_target() -> None:
    tree = TaskTree()
    tree.create_node(
        title="测试对象越权",
        node_type=NodeType.TEST,
        source="reasoning",
        related_feature_id="feat-acl",
        related_test_family="access_control",
        description="围绕订单越权做对象访问测试",
        notes=["高优先级提示：参考上一次成功样例 http://10.10.10.10:18080，仅作为示例"],
    )

    runtime = ScriptedRuntime(
        '{"tool_name":"python","command":"print(\"/orders\")"}'
    )
    agent = ActAgent(runtime=runtime, tools=ToolRegistry([PythonMCPTool()]))

    result = agent.execute_next(tree)

    assert result is not None
    assert "BASE_URL = 'http://127.0.0.1'" in result.command
    assert "10.10.10.10:18080" not in result.command
