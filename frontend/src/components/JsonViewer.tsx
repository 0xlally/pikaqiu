interface JsonViewerProps {
  value: unknown;
  defaultOpen?: boolean;
}

function renderPrimitive(value: unknown) {
  if (typeof value === "string") {
    return <pre className="whitespace-pre-wrap break-words text-sm text-slate-100">{value}</pre>;
  }

  return <code className="text-sm text-emerald-200">{JSON.stringify(value)}</code>;
}

export function JsonViewer({ value, defaultOpen = true }: JsonViewerProps) {
  if (value === null || typeof value !== "object") {
    return <div className="rounded-xl border border-console-800 bg-console-950/70 p-3">{renderPrimitive(value)}</div>;
  }

  if (Array.isArray(value)) {
    return (
      <details open={defaultOpen} className="rounded-xl border border-console-800 bg-console-950/70 p-3">
        <summary className="cursor-pointer text-sm font-medium text-slate-200">数组[{value.length}]</summary>
        <div className="mt-3 space-y-3 pl-1">
          {value.map((item, index) => (
            <div key={index}>
              <div className="mb-1 text-xs uppercase tracking-wide text-console-400">[{index}]</div>
              <JsonViewer value={item} defaultOpen={false} />
            </div>
          ))}
        </div>
      </details>
    );
  }

  return (
    <details open={defaultOpen} className="rounded-xl border border-console-800 bg-console-950/70 p-3">
      <summary className="cursor-pointer text-sm font-medium text-slate-200">对象</summary>
      <div className="mt-3 space-y-3 pl-1">
        {Object.entries(value).map(([key, item]) => (
          <div key={key}>
            <div className="mb-1 text-xs uppercase tracking-wide text-console-400">{key}</div>
            <JsonViewer value={item} defaultOpen={false} />
          </div>
        ))}
      </div>
    </details>
  );
}
