import { useState } from "react";

import type { TaskNode, TimelineEvent } from "../types/debug";
import { copyText, formatDateTime, formatDuration } from "../utils/format";
import { JsonViewer } from "./JsonViewer";
import { Panel } from "./Panel";
import { EventStatusBadge, EventTypeBadge, NodeStatusBadge, NodeTypeBadge, StatusBadge } from "./StatusBadge";

interface EventDetailPanelProps {
  selectedEvent: TimelineEvent | null;
  selectedNode: TaskNode | null;
}

type DetailView = "summary" | "raw" | "parsed";

const DETAIL_VIEW_LABELS: Record<DetailView, string> = {
  summary: "摘要",
  raw: "原始",
  parsed: "解析",
};

const ACTOR_LABELS: Record<string, string> = {
  reasoning: "推理",
  parsing: "解析",
  act: "执行",
  tool: "工具",
  system: "系统",
};

export function EventDetailPanel({ selectedEvent, selectedNode }: EventDetailPanelProps) {
  const [detailView, setDetailView] = useState<DetailView>("summary");

  const view = selectedEvent ?? selectedNode;

  return (
    <Panel
      title="详情"
      subtitle="展示完整事件或节点信息，支持摘要 / 原始 / 解析视图。"
      actions={
        view ? (
          <button type="button" onClick={() => copyText(view)} className="rounded-xl border border-console-800 bg-console-950 px-3 py-2 text-xs text-slate-300 hover:border-console-700">
            复制详情
          </button>
        ) : null
      }
      className="h-full"
    >
      {!view ? <div className="rounded-2xl border border-console-800 bg-console-950/70 p-6 text-sm text-slate-400">请选择节点或事件查看详情。</div> : null}

      {selectedEvent ? (
        <div className="space-y-4">
          <div className="flex flex-wrap gap-2">
            <EventTypeBadge eventType={selectedEvent.eventType} />
            <EventStatusBadge status={selectedEvent.status} />
            <StatusBadge label={ACTOR_LABELS[selectedEvent.actor] ?? selectedEvent.actor} tone={selectedEvent.actor === "reasoning" ? "accent" : selectedEvent.actor === "parsing" ? "info" : selectedEvent.actor === "tool" ? "warning" : "neutral"} />
          </div>

          <div className="rounded-2xl border border-console-800 bg-console-950/70 p-4">
            <div className="text-base font-semibold text-white">{selectedEvent.title}</div>
            <p className="mt-2 text-sm text-slate-300">{selectedEvent.summary}</p>
            <div className="mt-3 grid gap-2 text-xs text-slate-400">
              <div>事件ID: {selectedEvent.id}</div>
              <div>步骤: {selectedEvent.stepIndex}</div>
              <div>关联节点: {selectedEvent.relatedNodeId ?? "-"}</div>
              <div>关联工具: {selectedEvent.relatedToolCallId ?? "-"}</div>
              <div>开始时间: {formatDateTime(selectedEvent.startedAt)}</div>
              <div>结束时间: {formatDateTime(selectedEvent.finishedAt)}</div>
              <div>耗时: {formatDuration(selectedEvent.durationMs)}</div>
            </div>
          </div>

          <div className="flex flex-wrap gap-2">
            {(["summary", "raw", "parsed"] as DetailView[]).map((viewMode) => (
              <button
                key={viewMode}
                type="button"
                onClick={() => setDetailView(viewMode)}
                className={`rounded-xl border px-3 py-2 text-sm ${detailView === viewMode ? "border-accent bg-accent/15 text-teal-100" : "border-console-800 bg-console-950 text-slate-300"}`}
              >
                {DETAIL_VIEW_LABELS[viewMode]}
              </button>
            ))}
          </div>

          {detailView === "summary" ? (
            <div className="space-y-3">
              <div className="rounded-2xl border border-console-800 bg-console-950/70 p-4">
                <div className="text-xs uppercase tracking-wide text-console-400">输入摘要</div>
                <div className="mt-2"><JsonViewer value={selectedEvent.rawInput} defaultOpen={false} /></div>
              </div>
              <div className="rounded-2xl border border-console-800 bg-console-950/70 p-4">
                <div className="text-xs uppercase tracking-wide text-console-400">输出摘要</div>
                <div className="mt-2"><JsonViewer value={selectedEvent.rawOutput} defaultOpen={false} /></div>
              </div>
              {selectedEvent.error ? <div className="rounded-2xl border border-danger/40 bg-danger/10 p-4 text-sm text-red-100">{selectedEvent.error.message}</div> : null}
            </div>
          ) : null}

          {detailView === "raw" ? <JsonViewer value={{ raw_input: selectedEvent.rawInput, raw_output: selectedEvent.rawOutput, error: selectedEvent.error }} /> : null}
          {detailView === "parsed" ? <JsonViewer value={selectedEvent.parsedOutput} /> : null}
        </div>
      ) : null}

      {!selectedEvent && selectedNode ? (
        <div className="space-y-4">
          <div className="flex flex-wrap gap-2">
            <NodeTypeBadge nodeType={selectedNode.nodeType} />
            <NodeStatusBadge status={selectedNode.status} />
          </div>
          <div className="rounded-2xl border border-console-800 bg-console-950/70 p-4">
            <div className="text-base font-semibold text-white">{selectedNode.title}</div>
            <div className="mt-3 grid gap-2 text-xs text-slate-400">
              <div>节点ID: {selectedNode.id}</div>
              <div>来源: {selectedNode.source}</div>
              <div>父节点: {selectedNode.parentId ?? "-"}</div>
              <div>功能点: {selectedNode.sourceFeatureId ?? "-"}</div>
              <div>创建时间: {formatDateTime(selectedNode.createdAt)}</div>
              <div>更新时间: {formatDateTime(selectedNode.updatedAt)}</div>
            </div>
          </div>
          <div className="rounded-2xl border border-console-800 bg-console-950/70 p-4">
            <div className="text-xs uppercase tracking-wide text-console-400">测试家族标签</div>
            <div className="mt-2 flex flex-wrap gap-2">
              {selectedNode.familyIds.length === 0 ? <span className="text-sm text-slate-400">暂无家族标签。</span> : selectedNode.familyIds.map((familyId) => <StatusBadge key={familyId} label={familyId} tone="neutral" />)}
            </div>
          </div>
          <div className="rounded-2xl border border-console-800 bg-console-950/70 p-4">
            <div className="text-xs uppercase tracking-wide text-console-400">备注</div>
            <ul className="mt-2 space-y-2 text-sm text-slate-300">
              {selectedNode.notes.map((note) => <li key={note} className="rounded-xl border border-console-800 bg-console-900/80 p-3">{note}</li>)}
            </ul>
          </div>
          <JsonViewer value={selectedNode} />
        </div>
      ) : null}
    </Panel>
  );
}
