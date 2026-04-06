import type { ReasoningResult } from "../types/debug";
import { Panel } from "./Panel";
import { StatusBadge } from "./StatusBadge";

interface ReasoningPanelProps {
  reasoningResults: ReasoningResult[];
  selectedEventId: string | null;
}

export function ReasoningPanel({ reasoningResults, selectedEventId }: ReasoningPanelProps) {
  return (
    <Panel title="推理结果" subtitle="展示事实聚合、测试家族映射与建议测试节点。">
      <div className="space-y-4">
        {reasoningResults.map((result) => (
          <article key={result.id} className={`rounded-2xl border p-4 ${result.eventId === selectedEventId ? "border-accent bg-accent/10" : "border-console-800 bg-console-950/70"}`}>
            <div className="flex flex-wrap items-center gap-2">
              <StatusBadge label={result.id} tone="accent" />
              <StatusBadge label={`事件 ${result.eventId}`} tone="neutral" />
            </div>
            <div className="mt-4 grid gap-4 xl:grid-cols-3">
              <div className="rounded-xl border border-console-800 bg-console-900/80 p-3">
                <div className="text-xs uppercase tracking-wide text-console-400">识别功能点</div>
                <div className="mt-3 space-y-3">
                  {result.identifiedFeatures.map((feature) => (
                    <div key={feature.featureId} className="rounded-xl border border-console-800 bg-console-950/70 p-3">
                      <div className="text-sm font-semibold text-slate-100">{feature.title}</div>
                      <div className="mt-1 text-sm text-slate-300">{feature.summary}</div>
                      <div className="mt-2 text-xs text-console-400">事实</div>
                      <div className="mt-1 flex flex-wrap gap-2">{feature.facts.map((fact) => <StatusBadge key={fact} label={fact} tone="neutral" />)}</div>
                    </div>
                  ))}
                </div>
              </div>

              <div className="rounded-xl border border-console-800 bg-console-900/80 p-3">
                <div className="text-xs uppercase tracking-wide text-console-400">测试家族映射</div>
                <div className="mt-3 space-y-3">
                  {result.familyMapping.map((mapping) => (
                    <div key={mapping.featureId} className="rounded-xl border border-console-800 bg-console-950/70 p-3">
                      <div className="flex flex-wrap gap-2">
                        {mapping.familyIds.map((familyId) => <StatusBadge key={familyId} label={familyId} tone={familyId === mapping.primaryFamilyId ? "accent" : "neutral"} />)}
                      </div>
                      <div className="mt-2 text-xs text-slate-400">置信度: {mapping.confidence}</div>
                      <ul className="mt-3 space-y-2 text-sm text-slate-300">
                        {mapping.reasons.map((reason) => <li key={reason} className="rounded-lg border border-console-800 bg-console-900/80 p-2">{reason}</li>)}
                      </ul>
                    </div>
                  ))}
                </div>
              </div>

              <div className="rounded-xl border border-console-800 bg-console-900/80 p-3">
                <div className="text-xs uppercase tracking-wide text-console-400">建议测试节点</div>
                <div className="mt-3 space-y-3">
                  {result.proposedTestNodes.map((proposal) => (
                    <div key={proposal.title} className="rounded-xl border border-console-800 bg-console-950/70 p-3">
                      <div className="text-sm font-semibold text-slate-100">{proposal.title}</div>
                      <div className="mt-2 flex flex-wrap gap-2">
                        {proposal.familyIds.map((familyId) => <StatusBadge key={familyId} label={familyId} tone={familyId === proposal.primaryFamilyId ? "accent" : "neutral"} />)}
                      </div>
                      <div className="mt-2 text-sm text-slate-300">{proposal.rationale}</div>
                      <div className="mt-2 text-xs text-slate-400">创建节点: {proposal.createdNodeId ?? "-"}</div>
                      <div className="mt-1 text-xs text-slate-400">优先级: {proposal.priority}</div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </article>
        ))}
      </div>
    </Panel>
  );
}
