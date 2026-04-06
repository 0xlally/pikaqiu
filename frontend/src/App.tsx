import { type FormEvent, useEffect, useState } from "react";

import { createRun, getLatestRun, getRunById, listRuns, type RunListItem } from "./api/client";
import { EventDetailPanel } from "./components/EventDetailPanel";
import { FilterBar } from "./components/FilterBar";
import { ParsingPanel } from "./components/ParsingPanel";
import { ReasoningPanel } from "./components/ReasoningPanel";
import { RunHeader } from "./components/RunHeader";
import { StateTablePanel } from "./components/StateTablePanel";
import { TaskTreePanel } from "./components/TaskTreePanel";
import { TimelinePanel } from "./components/TimelinePanel";
import { ToolCallsPanel } from "./components/ToolCallsPanel";
import type { NodeStatus, NodeType, RunSummary } from "./types/debug";
import { formatDateTime, searchText } from "./utils/format";

type DebugTab = "tools" | "parsing" | "reasoning" | "state";

const TAB_LABELS: Record<DebugTab, string> = {
  tools: "工具调用",
  parsing: "解析结果",
  reasoning: "推理结果",
  state: "状态表",
};

function runStatusLabel(status: RunSummary["status"]): string {
  if (status === "completed") {
    return "已完成";
  }
  if (status === "failed") {
    return "失败";
  }
  return "运行中";
}

function App() {
  const [run, setRun] = useState<RunSummary | null>(null);
  const [featureDescription, setFeatureDescription] = useState("Admin login endpoint /api/login exposes username password captcha and token-based session handling.");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isLoadingLatest, setIsLoadingLatest] = useState(true);
  const [requestError, setRequestError] = useState<string | null>(null);
  const [runHistory, setRunHistory] = useState<RunListItem[]>([]);

  const [selectedNodeId, setSelectedNodeId] = useState<string | null>(null);
  const [selectedEventId, setSelectedEventId] = useState<string | null>(null);
  const [nodeStatusFilter, setNodeStatusFilter] = useState<NodeStatus | "all">("all");
  const [nodeTypeFilter, setNodeTypeFilter] = useState<NodeType | "all">("all");
  const [search, setSearch] = useState("");
  const [onlyToolCalls, setOnlyToolCalls] = useState(false);
  const [onlyErrors, setOnlyErrors] = useState(false);
  const [onlyReasoning, setOnlyReasoning] = useState(false);
  const [activeTab, setActiveTab] = useState<DebugTab>("tools");

  useEffect(() => {
    let cancelled = false;

    async function loadLatest() {
      setIsLoadingLatest(true);
      try {
        const [latest, history] = await Promise.all([getLatestRun(), listRuns()]);
        if (cancelled) {
          return;
        }
        setRun(latest);
        setRunHistory(history);
      } catch (error) {
        if (cancelled) {
          return;
        }
        setRequestError(error instanceof Error ? error.message : "加载最新运行失败。");
      } finally {
        if (!cancelled) {
          setIsLoadingLatest(false);
        }
      }
    }

    void loadLatest();
    return () => {
      cancelled = true;
    };
  }, []);

  useEffect(() => {
    if (!run) {
      setSelectedNodeId(null);
      setSelectedEventId(null);
      return;
    }
    const latestEvent = run.timeline[run.timeline.length - 1] ?? null;
    setSelectedNodeId(run.currentNodeId);
    setSelectedEventId(latestEvent?.id ?? null);
  }, [run]);

  const selectedNode = run?.nodes.find((node) => node.id === selectedNodeId) ?? null;
  const allEvents = run?.timeline ?? [];

  const filteredTimeline = allEvents.filter((event) => {
    if (selectedNodeId && event.relatedNodeId !== selectedNodeId) {
      return false;
    }
    if (onlyToolCalls && !(event.relatedToolCallId || event.actor === "tool")) {
      return false;
    }
    if (onlyErrors && !(event.status === "failed" || event.eventType === "error")) {
      return false;
    }
    if (onlyReasoning && !(event.actor === "reasoning" || event.eventType === "reasoning_completed")) {
      return false;
    }
    if (search && !searchText(event).includes(search.toLowerCase())) {
      return false;
    }
    return true;
  });

  useEffect(() => {
    if (!selectedEventId && filteredTimeline.length > 0) {
      setSelectedEventId(filteredTimeline[0].id);
      return;
    }
    if (selectedEventId && filteredTimeline.some((event) => event.id === selectedEventId)) {
      return;
    }
    setSelectedEventId(filteredTimeline[0]?.id ?? null);
  }, [filteredTimeline, selectedEventId]);

  const selectedEvent = filteredTimeline.find((event) => event.id === selectedEventId) ?? allEvents.find((event) => event.id === selectedEventId) ?? null;
  const selectedToolCallId = selectedEvent?.relatedToolCallId ?? null;

  function handleSelectNode(nodeId: string | null) {
    if (!run) {
      return;
    }
    setSelectedNodeId(nodeId);
    if (nodeId === null) {
      const latestEvent = run.timeline[run.timeline.length - 1] ?? null;
      setSelectedEventId(latestEvent?.id ?? null);
      return;
    }
    const firstEvent = run.timeline.find((event) => event.relatedNodeId === nodeId);
    setSelectedEventId(firstEvent?.id ?? null);
  }

  function clearTimelineFilters() {
    setSearch("");
    setOnlyToolCalls(false);
    setOnlyErrors(false);
    setOnlyReasoning(false);
  }

  async function handleRunSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const input = featureDescription.trim();
    if (!input) {
      setRequestError("请输入功能描述后再运行。");
      return;
    }

    setIsSubmitting(true);
    setRequestError(null);
    try {
      const nextRun = await createRun(input);
      setRun(nextRun);
      const history = await listRuns();
      setRunHistory(history);
      setActiveTab("tools");
    } catch (error) {
      setRequestError(error instanceof Error ? error.message : "创建运行失败。");
    } finally {
      setIsSubmitting(false);
    }
  }

  async function handleRefreshLatest() {
    setIsLoadingLatest(true);
    setRequestError(null);
    try {
      const [latest, history] = await Promise.all([getLatestRun(), listRuns()]);
      setRun(latest);
      setRunHistory(history);
    } catch (error) {
      setRequestError(error instanceof Error ? error.message : "刷新最新运行失败。");
    } finally {
      setIsLoadingLatest(false);
    }
  }

  async function handleOpenRun(runId: string) {
    setRequestError(null);
    try {
      const detail = await getRunById(runId);
      setRun(detail);
      setActiveTab("tools");
    } catch (error) {
      setRequestError(error instanceof Error ? error.message : "加载指定运行失败。");
    }
  }

  return (
    <div className="min-h-screen bg-console-950 px-4 py-4 text-slate-100">
      <div className="mx-auto max-w-[1800px]">
        <section className="mb-4 rounded-2xl border border-console-800 bg-console-900/95 p-4 shadow-panel">
          <form onSubmit={handleRunSubmit} className="grid gap-3">
            <label htmlFor="feature-description" className="text-sm font-medium text-slate-200">功能描述</label>
            <textarea
              id="feature-description"
              value={featureDescription}
              onChange={(event) => setFeatureDescription(event.target.value)}
              rows={3}
              className="w-full rounded-xl border border-console-800 bg-console-950 px-3 py-2 text-sm text-slate-100 outline-none placeholder:text-console-500 focus:border-accent"
              placeholder="输入要让后端执行分析的真实功能描述"
            />
            <div className="flex flex-wrap items-center gap-3">
              <button
                type="submit"
                disabled={isSubmitting}
                className="rounded-xl border border-accent bg-accent/15 px-4 py-2 text-sm text-teal-100 disabled:cursor-not-allowed disabled:opacity-50"
              >
                {isSubmitting ? "后端执行中..." : "启动真实运行"}
              </button>
              <button
                type="button"
                onClick={() => void handleRefreshLatest()}
                disabled={isLoadingLatest}
                className="rounded-xl border border-console-800 bg-console-950 px-4 py-2 text-sm text-slate-200 disabled:cursor-not-allowed disabled:opacity-50"
              >
                {isLoadingLatest ? "刷新中..." : "加载最新运行"}
              </button>
            </div>

            <div className="mt-1 rounded-xl border border-console-800 bg-console-950/70 p-3">
              <div className="text-xs uppercase tracking-wide text-console-400">最近运行</div>
              <div className="mt-2 flex flex-wrap gap-2">
                {runHistory.length === 0 ? (
                  <span className="text-xs text-slate-400">暂无历史运行</span>
                ) : (
                  runHistory.map((item) => (
                    <button
                      key={item.runId}
                      type="button"
                      onClick={() => void handleOpenRun(item.runId)}
                      className="rounded-xl border border-console-800 bg-console-900 px-3 py-2 text-left text-xs text-slate-200 hover:border-console-700"
                    >
                      <div className="font-medium text-slate-100">{item.runId}</div>
                      <div className="mt-1 text-console-400">{runStatusLabel(item.status)} | {formatDateTime(item.updatedAt)}</div>
                    </button>
                  ))
                )}
              </div>
            </div>
          </form>
          {requestError ? <div className="mt-3 rounded-xl border border-danger/40 bg-danger/10 p-3 text-sm text-red-100">{requestError}</div> : null}
        </section>

        {!run ? (
          <section className="rounded-2xl border border-console-800 bg-console-900/95 p-6 text-sm text-slate-300 shadow-panel">
            暂无运行数据。请先点击“启动真实运行”，前端将调用后端 API 执行并展示返回结果。
          </section>
        ) : (
          <>
            <RunHeader run={run} currentNode={selectedNode} />
            <FilterBar
              search={search}
              onSearchChange={setSearch}
              onlyToolCalls={onlyToolCalls}
              onToggleToolCalls={() => setOnlyToolCalls((value) => !value)}
              onlyErrors={onlyErrors}
              onToggleErrors={() => setOnlyErrors((value) => !value)}
              onlyReasoning={onlyReasoning}
              onToggleReasoning={() => setOnlyReasoning((value) => !value)}
              resultCount={filteredTimeline.length}
              onClear={clearTimelineFilters}
            />

            <div className="grid gap-4 xl:grid-cols-[320px_minmax(0,1fr)_420px]">
              <TaskTreePanel
                run={run}
                selectedNodeId={selectedNodeId}
                onSelectNode={handleSelectNode}
                statusFilter={nodeStatusFilter}
                onStatusFilterChange={setNodeStatusFilter}
                typeFilter={nodeTypeFilter}
                onTypeFilterChange={setNodeTypeFilter}
              />
              <TimelinePanel events={filteredTimeline} selectedEventId={selectedEventId} onSelectEvent={setSelectedEventId} />
              <EventDetailPanel selectedEvent={selectedEvent} selectedNode={selectedNode} />
            </div>

            <div className="mt-4 rounded-2xl border border-console-800 bg-console-900/95 p-3 shadow-panel">
              <div className="mb-3 flex flex-wrap gap-2">
                {(["tools", "parsing", "reasoning", "state"] as DebugTab[]).map((tab) => (
                  <button
                    key={tab}
                    type="button"
                    onClick={() => setActiveTab(tab)}
                    className={`rounded-xl border px-3 py-2 text-sm ${activeTab === tab ? "border-accent bg-accent/15 text-teal-100" : "border-console-800 bg-console-950 text-slate-300"}`}
                  >
                    {TAB_LABELS[tab]}
                  </button>
                ))}
              </div>

              {activeTab === "tools" ? <ToolCallsPanel toolCalls={run.toolCalls} selectedToolCallId={selectedToolCallId} /> : null}
              {activeTab === "parsing" ? <ParsingPanel parsingResults={run.parsingResults} selectedEventId={selectedEventId} /> : null}
              {activeTab === "reasoning" ? <ReasoningPanel reasoningResults={run.reasoningResults} selectedEventId={selectedEventId} /> : null}
              {activeTab === "state" ? <StateTablePanel stateTable={run.stateTable} selectedEventId={selectedEventId} /> : null}
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default App;
