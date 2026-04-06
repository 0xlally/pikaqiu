import type { ParsingResult } from "../types/debug";
import { Panel } from "./Panel";
import { StatusBadge } from "./StatusBadge";

interface ParsingPanelProps {
  parsingResults: ParsingResult[];
  selectedEventId: string | null;
}

export function ParsingPanel({ parsingResults, selectedEventId }: ParsingPanelProps) {
  return (
    <Panel title="解析结果" subtitle="展示 parsing agent 抽取的结构化事实及其证据来源。">
      <div className="space-y-4">
        {parsingResults.map((result) => (
          <article key={result.id} className={`rounded-2xl border p-4 ${result.eventId === selectedEventId ? "border-accent bg-accent/10" : "border-console-800 bg-console-950/70"}`}>
            <div className="text-sm font-semibold text-slate-100">{result.summary}</div>
            <div className="mt-2 flex flex-wrap gap-2">
              <StatusBadge label={result.id} tone="info" />
              <StatusBadge label={`事件 ${result.eventId}`} tone="neutral" />
              <StatusBadge label={`节点 ${result.relatedNodeId}`} tone="neutral" />
            </div>
            <div className="mt-4 grid gap-4 xl:grid-cols-2">
              {Object.entries(result.factsByType).map(([section, facts]) => (
                <div key={section} className="rounded-xl border border-console-800 bg-console-900/80 p-3">
                  <div className="flex items-center justify-between gap-2">
                    <div className="text-xs uppercase tracking-wide text-console-400">{section}</div>
                    <StatusBadge label={`${facts.length}`} tone="neutral" />
                  </div>
                  <ul className="mt-3 space-y-2 text-sm text-slate-300">
                    {facts.map((fact) => (
                      <li key={fact.id} className="rounded-xl border border-console-800 bg-console-950/70 p-3">
                        <div>{fact.text}</div>
                        <div className="mt-2 text-xs text-slate-400">来源事件: {fact.sourceEventId}</div>
                        <div className="mt-1 text-xs text-slate-400">工具调用: {fact.sourceToolCallId ?? "-"}</div>
                        <div className="mt-1 text-xs text-slate-400">证据: {fact.evidenceRefs.join(", ") || "-"}</div>
                      </li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
            <div className="mt-4 rounded-xl border border-console-800 bg-console-900/80 p-3">
              <div className="text-xs uppercase tracking-wide text-console-400">备注</div>
              <ul className="mt-3 space-y-2 text-sm text-slate-300">
                {result.notes.map((note) => (
                  <li key={note.id} className="rounded-xl border border-console-800 bg-console-950/70 p-3">
                    <div>{note.text}</div>
                    <div className="mt-2 text-xs text-slate-400">来源事件: {note.sourceEventId}</div>
                    <div className="mt-1 text-xs text-slate-400">证据: {note.evidenceRefs.join(", ")}</div>
                  </li>
                ))}
              </ul>
            </div>
          </article>
        ))}
      </div>
    </Panel>
  );
}
