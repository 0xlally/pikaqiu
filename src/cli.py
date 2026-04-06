from __future__ import annotations

from pathlib import Path
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import typer

from core.models import NodeStatus, NodeType
from workflow import build_default_workflow, default_mapping_path

app = typer.Typer(help="SRC测试系统的命令行入口。")
console = Console()


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
            console.print(Panel(str(error), title="事件错误", border_style="red"))

        agent_output = output.get("agentOutput")
        if isinstance(agent_output, str) and agent_output.strip():
            console.print(Panel(agent_output, title=f"{stage} agent输出", border_style="cyan"))

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

    console.rule("详细动作输出")

    if result.plan.trace:
        console.print(
            Panel(
                result.plan.trace,
                title="reasoning agent 输出",
                border_style="cyan",
            )
        )
    else:
        console.print("reasoning agent 输出: -")

    if result.act_result:
        act_result = result.act_result
        tool_output = _strip_agent_trace(act_result.raw_output)
        agent_trace = _extract_agent_trace(act_result.raw_output)
        stdout, stderr = _split_stdout_stderr(tool_output)

        call_table = Table(title="工具调用详情")
        call_table.add_column("字段")
        call_table.add_column("值")
        call_table.add_row("节点", act_result.node_id)
        call_table.add_row("工具", act_result.tool_name)
        call_table.add_row("退出码", str(act_result.exit_code))
        call_table.add_row("开始", act_result.started_at)
        call_table.add_row("结束", act_result.finished_at)
        call_table.add_row("命令", act_result.command)
        console.print(call_table)

        console.print(
            Panel(
                agent_trace or "-",
                title="act agent 输出（原始）",
                border_style="magenta",
            )
        )
        console.print(
            Panel(
                stdout or "-",
                title="工具 stdout",
                border_style="green",
            )
        )
        console.print(
            Panel(
                stderr or "-",
                title="工具 stderr",
                border_style="red",
            )
        )
    else:
        console.print("act/工具执行结果: -")

    if result.parsed_result and result.parsed_result.state_delta.notes:
        console.print(
            Panel(
                "\n".join(result.parsed_result.state_delta.notes),
                title="parsing agent 输出（原始）",
                border_style="yellow",
            )
        )


if __name__ == "__main__":
    app()
