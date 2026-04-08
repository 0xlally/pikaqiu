from __future__ import annotations

import json

from core.models import StateItem, StateTable
from infra.mcp import StateTableQueryMCPTool


def test_state_table_query_tool_returns_filtered_snapshot() -> None:
    table = StateTable(
        identities=[StateItem(title="账号", content="test:test")],
        key_entrypoints=[StateItem(title="API路径", content="/api/login")],
        session_materials=[StateItem(title="JWT", content="eyJ.header.payload")],
        notes=["login endpoint validated"],
    )
    tool = StateTableQueryMCPTool(lambda: table)

    output = tool.run("section=all;keyword=login")

    assert output.exit_code == 0
    payload = json.loads(output.stdout)
    assert payload["query"]["section"] == "all"
    assert payload["query"]["keyword"] == "login"
    result = payload["result"]
    assert result["key_entrypoints"]
    assert result["notes"]


def test_state_table_query_tool_supports_single_section() -> None:
    table = StateTable(
        identities=[StateItem(title="账号", content="test:test")],
        key_entrypoints=[StateItem(title="API路径", content="/api/login")],
    )
    tool = StateTableQueryMCPTool(lambda: table)

    output = tool.run("section=identities")

    payload = json.loads(output.stdout)
    result = payload["result"]
    assert "identities" in result
    assert "key_entrypoints" not in result
    assert result["identities"][0]["content"] == "test:test"
