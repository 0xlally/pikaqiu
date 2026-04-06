import type { NodeStatus, NodeType, RunSummary } from "../types/debug";
import { classNames, formatDateTime } from "../utils/format";
import { Panel } from "./Panel";
import { NodeStatusBadge, NodeTypeBadge, StatusBadge } from "./StatusBadge";

interface TaskTreePanelProps {
  run: RunSummary;
  selectedNodeId: string | null;
  onSelectNode: (nodeId: string | null) => void;
  statusFilter: NodeStatus | "all";
  onStatusFilterChange: (value: NodeStatus | "all") => void;
  typeFilter: NodeType | "all";
  onTypeFilterChange: (value: NodeType | "all") => void;
}

function nodeDepth(run: RunSummary, nodeId: string): number {
  let depth = 0;
  let current = run.nodes.find((node) => node.id === nodeId) ?? null;

  while (current?.parentId) {
    depth += 1;
    current = run.nodes.find((node) => node.id === current?.parentId) ?? null;
  }

  return depth;
}

export function TaskTreePanel({
  run,
  selectedNodeId,
  onSelectNode,
  statusFilter,
  onStatusFilterChange,
  typeFilter,
  onTypeFilterChange,
}: TaskTreePanelProps) {
  const visibleNodes = run.nodes.filter((node) => {
    if (statusFilter !== "all" && node.status !== statusFilter) {
      return false;
    }
    if (typeFilter !== "all" && node.nodeType !== typeFilter) {
      return false;
    }
    return true;
  });

  return (
    <Panel
      title="任务树"
      subtitle="节点列表、状态筛选与父子关系。"
      actions={
        <button type="button" onClick={() => onSelectNode(null)} className="rounded-xl border border-console-800 bg-console-950 px-3 py-2 text-xs text-slate-300 hover:border-console-700">
          清空选择
        </button>
      }
      className="h-full"
    >
      <div className="mb-4 grid gap-3">
        <div className="rounded-xl border border-console-800 bg-console-950/80 p-3">
          <div className="text-xs uppercase tracking-wide text-console-400">当前阶段</div>
          <div className="mt-2 text-sm font-medium text-slate-100">{run.currentStage}</div>
        </div>
        <div className="grid grid-cols-2 gap-3">
          <select value={statusFilter} onChange={(event) => onStatusFilterChange(event.target.value as NodeStatus | "all")} className="rounded-xl border border-console-800 bg-console-950 px-3 py-2 text-sm text-slate-100 outline-none">
            <option value="all">全部状态</option>
            <option value="todo">待处理</option>
            <option value="doing">进行中</option>
            <option value="done">已完成</option>
            <option value="failed">失败</option>
          </select>
          <select value={typeFilter} onChange={(event) => onTypeFilterChange(event.target.value as NodeType | "all")} className="rounded-xl border border-console-800 bg-console-950 px-3 py-2 text-sm text-slate-100 outline-none">
            <option value="all">全部类型</option>
            <option value="info">信息</option>
            <option value="test">测试</option>
          </select>
        </div>
      </div>

      <div className="space-y-3">
        {visibleNodes.map((node) => {
          const isSelected = node.id === selectedNodeId;
          const isRunning = node.id === run.currentNodeId;
          const depth = nodeDepth(run, node.id);

          return (
            <button
              key={node.id}
              type="button"
              onClick={() => onSelectNode(node.id)}
              className={classNames(
                "block w-full rounded-2xl border p-3 text-left transition",
                isSelected ? "border-accent bg-accent/10" : "border-console-800 bg-console-950/70 hover:border-console-700",
                isRunning && "ring-1 ring-accent/70",
              )}
              style={{ marginLeft: `${depth * 12}px` }}
            >
              <div className="flex flex-wrap items-center gap-2">
                <NodeTypeBadge nodeType={node.nodeType} />
                <NodeStatusBadge status={node.status} />
                {isRunning ? <StatusBadge label="当前" tone="accent" /> : null}
              </div>
              <div className="mt-2 text-sm font-semibold text-slate-100">{node.title}</div>
              <div className="mt-2 grid gap-1 text-xs text-slate-400">
                <div>节点ID: {node.id}</div>
                <div>父节点: {node.parentId ?? "-"}</div>
                <div>功能点: {node.sourceFeatureId ?? "-"}</div>
                <div>更新时间: {formatDateTime(node.updatedAt)}</div>
              </div>
              <div className="mt-2 flex flex-wrap gap-2">
                {node.familyIds.length === 0 ? <span className="text-xs text-console-500">暂无家族标签</span> : node.familyIds.map((familyId) => <StatusBadge key={familyId} label={familyId} tone="neutral" />)}
              </div>
            </button>
          );
        })}
      </div>
    </Panel>
  );
}
