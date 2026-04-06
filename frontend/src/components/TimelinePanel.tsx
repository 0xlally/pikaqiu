import { useState } from "react";

import type { TimelineEvent } from "../types/debug";
import { classNames, formatDateTime, formatDuration, truncateText } from "../utils/format";
import { EventStatusBadge, EventTypeBadge, StatusBadge } from "./StatusBadge";
import { Panel } from "./Panel";

interface TimelinePanelProps {
  events: TimelineEvent[];
  selectedEventId: string | null;
  onSelectEvent: (eventId: string) => void;
}

export function TimelinePanel({ events, selectedEventId, onSelectEvent }: TimelinePanelProps) {
  const [expandedIds, setExpandedIds] = useState<string[]>([]);

  const actorLabelMap: Record<string, string> = {
    reasoning: "推理",
    parsing: "解析",
    act: "执行",
    tool: "工具",
    system: "系统",
  };

  function toggleExpanded(eventId: string) {
    setExpandedIds((current) =>
      current.includes(eventId) ? current.filter((value) => value !== eventId) : [...current, eventId],
    );
  }

  return (
    <Panel title="时间线" subtitle="按时间排序展示 agent 步骤、工具调用和节点变化。" className="h-full">
      <div className="space-y-3">
        {events.map((event) => {
          const expanded = expandedIds.includes(event.id);
          const selected = event.id === selectedEventId;
          const toolEvent = event.relatedToolCallId !== null || event.actor === "tool";

          return (
            <article
              key={event.id}
              className={classNames(
                "rounded-2xl border p-3 transition",
                selected ? "border-accent bg-accent/10" : "border-console-800 bg-console-950/70",
                toolEvent && "border-warning/40",
              )}
            >
              <div className="flex items-start justify-between gap-3">
                <button type="button" onClick={() => onSelectEvent(event.id)} className="flex-1 text-left">
                  <div className="flex flex-wrap items-center gap-2">
                    <StatusBadge label={`步骤 ${event.stepIndex}`} tone="neutral" />
                    <StatusBadge label={actorLabelMap[event.actor] ?? event.actor} tone={event.actor === "reasoning" ? "accent" : event.actor === "parsing" ? "info" : event.actor === "tool" ? "warning" : "neutral"} />
                    <EventTypeBadge eventType={event.eventType} />
                    <EventStatusBadge status={event.status} />
                  </div>
                  <div className="mt-2 text-sm font-semibold text-slate-100">{event.title}</div>
                  <p className="mt-1 text-sm text-slate-300">{truncateText(event.summary, 180)}</p>
                  <div className="mt-2 flex flex-wrap gap-4 text-xs text-slate-400">
                    <span>{formatDateTime(event.startedAt)}</span>
                    <span>{formatDuration(event.durationMs)}</span>
                    <span>关联节点: {event.relatedNodeId ?? "-"}</span>
                    <span>关联工具: {event.relatedToolCallId ?? "-"}</span>
                  </div>
                </button>
                <button type="button" onClick={() => toggleExpanded(event.id)} className="rounded-xl border border-console-800 bg-console-900 px-3 py-2 text-xs text-slate-300 hover:border-console-700">
                  {expanded ? "收起" : "展开"}
                </button>
              </div>

              {expanded ? (
                <div className="mt-3 space-y-2 border-t border-console-800 pt-3 text-sm text-slate-300">
                  <div><span className="text-console-400">输入:</span> {truncateText(JSON.stringify(event.rawInput), 140)}</div>
                  <div><span className="text-console-400">输出:</span> {truncateText(JSON.stringify(event.rawOutput), 140)}</div>
                  {event.error ? <div className="rounded-xl border border-danger/40 bg-danger/10 p-2 text-red-100">{event.error.message}</div> : null}
                </div>
              ) : null}
            </article>
          );
        })}
      </div>
    </Panel>
  );
}
