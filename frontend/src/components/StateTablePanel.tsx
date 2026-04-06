import type { StateItem, StateNoteRecord, StateTable } from "../types/debug";
import { classNames } from "../utils/format";
import { Panel } from "./Panel";
import { StatusBadge } from "./StatusBadge";

interface StateTablePanelProps {
  stateTable: StateTable;
  selectedEventId: string | null;
}

function StateItemsSection({
  title,
  items,
  selectedEventId,
  latestUpdateEventId,
}: {
  title: string;
  items: StateItem[];
  selectedEventId: string | null;
  latestUpdateEventId: string;
}) {
  return (
    <div className="rounded-xl border border-console-800 bg-console-900/80 p-3">
      <div className="text-xs uppercase tracking-wide text-console-400">{title}</div>
      <div className="mt-3 space-y-3">
        {items.map((item) => {
          const highlight = item.updatedInEventId === latestUpdateEventId || item.updatedInEventId === selectedEventId;
          return (
            <div key={item.id} className={classNames("rounded-xl border p-3", highlight ? "border-accent bg-accent/10" : "border-console-800 bg-console-950/70")}>
              <div className="flex items-center justify-between gap-2">
                <div className="text-sm font-semibold text-slate-100">{item.title}</div>
                {highlight ? <StatusBadge label="新增" tone="accent" /> : null}
              </div>
              <div className="mt-2 text-sm text-slate-300">{item.content}</div>
              <div className="mt-2 text-xs text-slate-400">引用: {item.refs.join(", ") || "-"}</div>
              <div className="mt-1 text-xs text-slate-400">来源: {item.source}</div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

function NotesSection({
  notes,
  selectedEventId,
  latestUpdateEventId,
}: {
  notes: StateNoteRecord[];
  selectedEventId: string | null;
  latestUpdateEventId: string;
}) {
  return (
    <div className="rounded-xl border border-console-800 bg-console-900/80 p-3">
      <div className="text-xs uppercase tracking-wide text-console-400">备注</div>
      <div className="mt-3 space-y-3">
        {notes.map((note) => {
          const highlight = note.updatedInEventId === latestUpdateEventId || note.updatedInEventId === selectedEventId;
          return (
            <div key={note.id} className={classNames("rounded-xl border p-3 text-sm text-slate-300", highlight ? "border-accent bg-accent/10" : "border-console-800 bg-console-950/70")}>
              {note.text}
            </div>
          );
        })}
      </div>
    </div>
  );
}

export function StateTablePanel({ stateTable, selectedEventId }: StateTablePanelProps) {
  return (
    <Panel title="状态表" subtitle="会话运行过程中累积的高价值上下文。">
      <div className="grid gap-4 xl:grid-cols-2">
        <StateItemsSection title="身份信息" items={stateTable.identities} selectedEventId={selectedEventId} latestUpdateEventId={stateTable.latestUpdateEventId} />
        <StateItemsSection title="会话材料" items={stateTable.sessionMaterials} selectedEventId={selectedEventId} latestUpdateEventId={stateTable.latestUpdateEventId} />
        <StateItemsSection title="关键入口" items={stateTable.keyEntrypoints} selectedEventId={selectedEventId} latestUpdateEventId={stateTable.latestUpdateEventId} />
        <StateItemsSection title="流程前置条件" items={stateTable.workflowPrerequisites} selectedEventId={selectedEventId} latestUpdateEventId={stateTable.latestUpdateEventId} />
        <StateItemsSection title="可复用工件" items={stateTable.reusableArtifacts} selectedEventId={selectedEventId} latestUpdateEventId={stateTable.latestUpdateEventId} />
        <StateItemsSection title="会话风险" items={stateTable.sessionRisks} selectedEventId={selectedEventId} latestUpdateEventId={stateTable.latestUpdateEventId} />
      </div>
      <div className="mt-4">
        <NotesSection notes={stateTable.notes} selectedEventId={selectedEventId} latestUpdateEventId={stateTable.latestUpdateEventId} />
      </div>
    </Panel>
  );
}
