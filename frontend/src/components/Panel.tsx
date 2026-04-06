import type { ReactNode } from "react";

import { classNames } from "../utils/format";

interface PanelProps {
  title: string;
  subtitle?: string;
  actions?: ReactNode;
  children: ReactNode;
  className?: string;
}

export function Panel({ title, subtitle, actions, children, className }: PanelProps) {
  return (
    <section className={classNames("rounded-2xl border border-console-800 bg-console-900/90 shadow-panel", className)}>
      <header className="flex items-start justify-between gap-4 border-b border-console-800 px-4 py-3">
        <div>
          <h2 className="text-sm font-semibold uppercase tracking-[0.18em] text-console-400">{title}</h2>
          {subtitle ? <p className="mt-1 text-sm text-slate-300">{subtitle}</p> : null}
        </div>
        {actions ? <div className="shrink-0">{actions}</div> : null}
      </header>
      <div className="p-4">{children}</div>
    </section>
  );
}
