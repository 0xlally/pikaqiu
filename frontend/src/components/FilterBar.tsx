interface FilterBarProps {
  search: string;
  onSearchChange: (value: string) => void;
  onlyToolCalls: boolean;
  onToggleToolCalls: () => void;
  onlyErrors: boolean;
  onToggleErrors: () => void;
  onlyReasoning: boolean;
  onToggleReasoning: () => void;
  resultCount: number;
  onClear: () => void;
}

function ToggleButton({
  active,
  label,
  onClick,
}: {
  active: boolean;
  label: string;
  onClick: () => void;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={`rounded-xl border px-3 py-2 text-sm transition ${
        active ? "border-accent bg-accent/15 text-teal-100" : "border-console-800 bg-console-900 text-slate-300 hover:border-console-700"
      }`}
    >
      {label}
    </button>
  );
}

export function FilterBar({
  search,
  onSearchChange,
  onlyToolCalls,
  onToggleToolCalls,
  onlyErrors,
  onToggleErrors,
  onlyReasoning,
  onToggleReasoning,
  resultCount,
  onClear,
}: FilterBarProps) {
  return (
    <div className="mb-4 flex flex-wrap items-center gap-3 rounded-2xl border border-console-800 bg-console-900/90 p-3 shadow-panel">
      <input
        value={search}
        onChange={(event) => onSearchChange(event.target.value)}
        placeholder="搜索 user_id / token / upload / webhook"
        className="min-w-[260px] flex-1 rounded-xl border border-console-800 bg-console-950 px-3 py-2 text-sm text-slate-100 outline-none placeholder:text-console-500 focus:border-accent"
      />
      <ToggleButton active={onlyToolCalls} label="仅工具调用" onClick={onToggleToolCalls} />
      <ToggleButton active={onlyErrors} label="仅错误" onClick={onToggleErrors} />
      <ToggleButton active={onlyReasoning} label="仅推理" onClick={onToggleReasoning} />
      <div className="rounded-xl border border-console-800 bg-console-950 px-3 py-2 text-sm text-slate-300">可见事件：{resultCount}</div>
      <button type="button" onClick={onClear} className="rounded-xl border border-console-800 bg-console-950 px-3 py-2 text-sm text-slate-300 hover:border-console-700">
        清空筛选
      </button>
    </div>
  );
}
