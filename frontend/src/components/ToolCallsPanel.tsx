import { useState } from "react";

import type { ToolCallRecord } from "../types/debug";
import { copyText, formatDateTime, formatDuration } from "../utils/format";
import { JsonViewer } from "./JsonViewer";
import { Panel } from "./Panel";
import { EventStatusBadge, StatusBadge } from "./StatusBadge";

interface ToolCallsPanelProps {
  toolCalls: ToolCallRecord[];
  selectedToolCallId: string | null;
}

export function ToolCallsPanel({ toolCalls, selectedToolCallId }: ToolCallsPanelProps) {
  const [toolFilter, setToolFilter] = useState<string>("all");
  const [statusFilter, setStatusFilter] = useState<"all" | "success" | "failed" | "running">("all");

  const toolNames = Array.from(new Set(toolCalls.map((call) => call.toolName)));
  const visibleCalls = toolCalls.filter((call) => {
    if (toolFilter !== "all" && call.toolName !== toolFilter) {
      return false;
    }
    if (statusFilter !== "all" && call.status !== statusFilter) {
      return false;
    }
    return true;
  });

  return (
    <Panel title="工具调用" subtitle="展示本次运行中的所有请求与响应记录。">
      <div className="mb-4 flex flex-wrap gap-3">
        <select value={toolFilter} onChange={(event) => setToolFilter(event.target.value)} className="rounded-xl border border-console-800 bg-console-950 px-3 py-2 text-sm text-slate-100">
          <option value="all">全部工具</option>
          {toolNames.map((toolName) => <option key={toolName} value={toolName}>{toolName}</option>)}
        </select>
        <select value={statusFilter} onChange={(event) => setStatusFilter(event.target.value as "all" | "success" | "failed" | "running")} className="rounded-xl border border-console-800 bg-console-950 px-3 py-2 text-sm text-slate-100">
          <option value="all">全部状态</option>
          <option value="success">成功</option>
          <option value="failed">失败</option>
          <option value="running">运行中</option>
        </select>
      </div>
      <div className="space-y-4">
        {visibleCalls.map((call) => (
          <article key={call.id} className={`rounded-2xl border p-4 ${call.id === selectedToolCallId ? "border-accent bg-accent/10" : "border-console-800 bg-console-950/70"}`}>
            <div className="flex flex-wrap items-center justify-between gap-2">
              <div className="flex flex-wrap items-center gap-2">
                <StatusBadge label={call.toolName} tone="warning" />
                <EventStatusBadge status={call.status === "success" ? "success" : call.status === "failed" ? "failed" : "running"} />
                <code className="rounded-lg bg-console-900 px-2 py-1 text-xs text-slate-300">{call.id}</code>
              </div>
              <button type="button" onClick={() => copyText(call)} className="rounded-xl border border-console-800 bg-console-900 px-3 py-2 text-xs text-slate-300 hover:border-console-700">
                复制
              </button>
            </div>
            <div className="mt-3 text-sm font-semibold text-slate-100">{call.title}</div>
            <div className="mt-1 text-sm text-slate-300">{call.summary}</div>
            <div className="mt-3 grid gap-2 text-xs text-slate-400 md:grid-cols-4">
              <div>开始时间: {formatDateTime(call.startedAt)}</div>
              <div>结束时间: {formatDateTime(call.finishedAt)}</div>
              <div>耗时: {formatDuration(call.durationMs)}</div>
              <div>关联节点: {call.relatedNodeId ?? "-"}</div>
            </div>
            {call.error ? <div className="mt-3 rounded-xl border border-danger/40 bg-danger/10 p-3 text-sm text-red-100">{call.error.message}</div> : null}
            <div className="mt-4 grid gap-4 xl:grid-cols-2">
              <div>
                <div className="mb-2 text-xs uppercase tracking-wide text-console-400">请求</div>
                <JsonViewer value={call.request} defaultOpen={false} />
              </div>
              <div>
                <div className="mb-2 text-xs uppercase tracking-wide text-console-400">响应</div>
                <JsonViewer value={call.response} defaultOpen={false} />
              </div>
            </div>
          </article>
        ))}
      </div>
    </Panel>
  );
}
