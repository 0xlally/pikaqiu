from __future__ import annotations

from pathlib import Path
from typing import Any

from rich.console import Console
from rich.table import Table
import typer

from core.models import NodeStatus, NodeType
from workflow import build_default_workflow, default_mapping_path

app = typer.Typer(help="SRC测试系统的命令行入口。")
console = Console()


@app.command()
def demo(
    feature_description: str = typer.Argument(..., help="功能点的自然语言描述。"),
    mapping_path: Path = typer.Option(default_mapping_path(), help="测试家族映射配置文件路径。"),
) -> None:
    """运行最小可执行演示。"""
    workflow = build_default_workflow(mapping_path=mapping_path)

    console.rule("实时时间线")

    def on_event(event: dict[str, Any]) -> None:
        step = event.get("stepIndex")
        stage = event.get("stage")
        title = event.get("title")
        status = event.get("status")
        console.print(f"[{step}] {stage} | {title} | status={status}")

        output = event.get("output") or {}
        error = event.get("error")
        if error:
            console.print(f"error: {error}")

        agent_output = output.get("agentOutput")
        if isinstance(agent_output, str) and agent_output.strip():
            console.print(f"{stage} agent输出: {agent_output}")

        if stage == "act:finish" and output:
            tool_name = output.get("toolName")
            exit_code = output.get("exitCode")
            if tool_name:
                console.print(f"tool={tool_name}, exit_code={exit_code}")

    result = workflow.run_demo_with_events(feature_description, event_callback=on_event)

    feature_table = Table(title="功能点")
    feature_table.add_column("字段")
    feature_table.add_column("值")
    feature_table.add_row("名称", result.feature_point.name)
    feature_table.add_row("入口", ", ".join(result.feature_point.entry_points) or "-")
    feature_table.add_row("角色", ", ".join(result.feature_point.roles) or "-")
    feature_table.add_row("关键参数", ", ".join(result.feature_point.key_parameters) or "-")
    console.print(feature_table)

    family_table = Table(title="推荐测试家族")
    family_table.add_column("家族")
    family_table.add_column("分数")
    family_table.add_column("命中词")
    for item in result.plan.recommended_families:
        family_table.add_row(item.family.name, str(item.score), ", ".join(item.matched_terms[:8]) or "-")
    console.print(family_table)

    node_table = Table(title="任务节点")
    node_table.add_column("节点")
    node_table.add_column("类型")
    node_table.add_column("状态")
    node_table.add_column("测试家族")
    for node in result.task_tree.nodes.values():
        node_table.add_row(node.title, node.kind.value, node.status.value, str(node.test_family_id or "-"))
    console.print(node_table)

    pending_nodes = [
        node
        for node in result.task_tree.nodes.values()
        if node.kind == NodeType.TEST and node.status == NodeStatus.TODO
    ]
    pending_table = Table(title="待执行 Test 节点")
    pending_table.add_column("节点")
    pending_table.add_column("描述")
    for node in pending_nodes:
        pending_table.add_row(node.title, node.description)
    console.print(pending_table)

    if result.parsed_result:
        console.print(f"[bold]解析摘要：[/bold] {result.parsed_result.summary}")

    if not pending_nodes:
        if result.plan.recommended_families:
            console.print("[yellow]运行结束：当前没有待执行 test 节点。[/yellow]")
        else:
            console.print("[yellow]运行结束：本轮未命中测试家族，因此未创建 test 节点。[/yellow]")


if __name__ == "__main__":
    app()
