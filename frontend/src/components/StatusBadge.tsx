import type { EventStatus, EventType, NodeStatus, NodeType } from "../types/debug";
import { classNames } from "../utils/format";

interface StatusBadgeProps {
  label: string;
  tone: "success" | "warning" | "danger" | "info" | "neutral" | "accent";
}

function toneClass(tone: StatusBadgeProps["tone"]): string {
  if (tone === "success") {
    return "border-success/40 bg-success/15 text-green-200";
  }
  if (tone === "warning") {
    return "border-warning/40 bg-warning/15 text-amber-100";
  }
  if (tone === "danger") {
    return "border-danger/40 bg-danger/15 text-red-100";
  }
  if (tone === "accent") {
    return "border-accent/40 bg-accent/15 text-teal-100";
  }
  if (tone === "info") {
    return "border-sky-400/40 bg-sky-400/15 text-sky-100";
  }
  return "border-console-700 bg-console-800/80 text-console-300";
}

export function StatusBadge({ label, tone }: StatusBadgeProps) {
  return (
    <span className={classNames("inline-flex items-center rounded-full border px-2 py-0.5 text-[11px] font-medium uppercase tracking-wide", toneClass(tone))}>
      {label}
    </span>
  );
}

function nodeStatusLabel(status: NodeStatus): string {
  if (status === "todo") {
    return "待处理";
  }
  if (status === "doing") {
    return "进行中";
  }
  if (status === "done") {
    return "已完成";
  }
  return "失败";
}

function nodeTypeLabel(nodeType: NodeType): string {
  return nodeType === "test" ? "测试" : "信息";
}

function eventStatusLabel(status: EventStatus): string {
  if (status === "running") {
    return "运行中";
  }
  if (status === "success") {
    return "成功";
  }
  if (status === "failed") {
    return "失败";
  }
  if (status === "retry") {
    return "重试";
  }
  return "信息";
}

function eventTypeLabel(eventType: EventType): string {
  if (eventType === "agent_step_started") {
    return "代理步骤开始";
  }
  if (eventType === "agent_step_finished") {
    return "代理步骤结束";
  }
  if (eventType === "tool_call_started") {
    return "工具调用开始";
  }
  if (eventType === "tool_call_finished") {
    return "工具调用结束";
  }
  if (eventType === "parsing_completed") {
    return "解析完成";
  }
  if (eventType === "reasoning_completed") {
    return "推理完成";
  }
  if (eventType === "node_created") {
    return "节点创建";
  }
  if (eventType === "node_updated") {
    return "节点更新";
  }
  if (eventType === "error") {
    return "错误";
  }
  if (eventType === "retry") {
    return "重试";
  }
  return "未知事件";
}

export function NodeStatusBadge({ status }: { status: NodeStatus }) {
  const tone = status === "done" ? "success" : status === "doing" ? "accent" : status === "failed" ? "danger" : "neutral";
  return <StatusBadge label={nodeStatusLabel(status)} tone={tone} />;
}

export function NodeTypeBadge({ nodeType }: { nodeType: NodeType }) {
  return <StatusBadge label={nodeTypeLabel(nodeType)} tone={nodeType === "test" ? "warning" : "info"} />;
}

export function EventStatusBadge({ status }: { status: EventStatus }) {
  const tone = status === "success" ? "success" : status === "running" ? "accent" : status === "failed" ? "danger" : status === "retry" ? "warning" : "neutral";
  return <StatusBadge label={eventStatusLabel(status)} tone={tone} />;
}

export function EventTypeBadge({ eventType }: { eventType: EventType }) {
  const tone =
    eventType === "tool_call_started" || eventType === "tool_call_finished"
      ? "warning"
      : eventType === "parsing_completed"
        ? "info"
        : eventType === "reasoning_completed"
          ? "accent"
          : eventType === "error"
            ? "danger"
            : "neutral";

  return <StatusBadge label={eventTypeLabel(eventType)} tone={tone} />;
}
