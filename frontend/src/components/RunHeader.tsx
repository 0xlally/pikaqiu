import type { RunSummary, TaskNode } from "../types/debug";
import { formatDateTime } from "../utils/format";
import { EventStatusBadge, NodeStatusBadge } from "./StatusBadge";

interface RunHeaderProps {
  run: RunSummary;
  currentNode: TaskNode | null;
}

function stageLabel(stage: RunSummary["currentStage"]): string {
  if (stage === "bootstrap") {
    return "初始化";
  }
  if (stage === "act:info") {
    return "执行:信息";
  }
  if (stage === "parsing:info") {
    return "解析:信息";
  }
  if (stage === "reasoning:feature-mapping") {
    return "推理:功能映射";
  }
  if (stage === "act:test") {
    return "执行:测试";
  }
  return "解析:测试";
}

export function RunHeader({ run, currentNode }: RunHeaderProps) {
  const doneCount = run.nodes.filter((node) => node.status === "done").length;
  const failedCount = run.timeline.filter((event) => event.status === "failed").length;

  return (
    <header className="mb-4 rounded-2xl border border-console-800 bg-console-900/95 p-4 shadow-panel">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <div className="flex flex-wrap items-center gap-2">
            <span className="text-xs uppercase tracking-[0.18em] text-console-400">运行</span>
            <code className="rounded-lg bg-console-950 px-2 py-1 font-mono text-xs text-slate-100">{run.runId}</code>
            <EventStatusBadge status={run.status === "running" ? "running" : run.status === "failed" ? "failed" : "success"} />
          </div>
          <h1 className="mt-2 text-2xl font-semibold text-white">pikaqiu 调试控制台</h1>
          <p className="mt-1 max-w-4xl text-sm text-slate-300">{run.goal}</p>
        </div>
        <div className="rounded-2xl border border-console-800 bg-console-950/80 px-4 py-3">
          <div className="text-xs uppercase tracking-[0.18em] text-console-400">当前节点</div>
          <div className="mt-2 text-sm font-medium text-slate-100">{currentNode?.title ?? "暂无活动节点"}</div>
          {currentNode ? <div className="mt-2"><NodeStatusBadge status={currentNode.status} /></div> : null}
        </div>
      </div>
      <div className="mt-4 grid gap-3 md:grid-cols-5">
        <div className="rounded-2xl border border-console-800 bg-console-950/80 p-3">
          <div className="text-xs uppercase tracking-wide text-console-400">目标</div>
          <div className="mt-2 break-all font-mono text-sm text-slate-100">{run.target}</div>
        </div>
        <div className="rounded-2xl border border-console-800 bg-console-950/80 p-3">
          <div className="text-xs uppercase tracking-wide text-console-400">阶段</div>
          <div className="mt-2 text-sm font-medium text-slate-100">{stageLabel(run.currentStage)}</div>
        </div>
        <div className="rounded-2xl border border-console-800 bg-console-950/80 p-3">
          <div className="text-xs uppercase tracking-wide text-console-400">完成节点</div>
          <div className="mt-2 text-xl font-semibold text-white">{doneCount}/{run.nodes.length}</div>
        </div>
        <div className="rounded-2xl border border-console-800 bg-console-950/80 p-3">
          <div className="text-xs uppercase tracking-wide text-console-400">错误数量</div>
          <div className="mt-2 text-xl font-semibold text-white">{failedCount}</div>
        </div>
        <div className="rounded-2xl border border-console-800 bg-console-950/80 p-3">
          <div className="text-xs uppercase tracking-wide text-console-400">更新时间</div>
          <div className="mt-2 text-sm font-medium text-slate-100">{formatDateTime(run.updatedAt)}</div>
        </div>
      </div>
    </header>
  );
}
