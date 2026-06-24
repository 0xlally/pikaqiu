import React, { useEffect, useRef, useState, useTransition } from "react";
import { createRoot } from "react-dom/client";
import {
  Brain,
  CheckCircle,
  Circuitry,
  ClockCounterClockwise,
  CompassTool,
  Database,
  FlagBanner,
  GearSix,
  Graph,
  Lightning,
  MagnifyingGlass,
  Pause,
  Play,
  Plus,
  Pulse,
  ShieldCheck,
  TerminalWindow,
  Trash,
  WarningCircle
} from "@phosphor-icons/react";
import { api, ApiError } from "./api";
import type {
  AppTab,
  AgentSlot,
  Bootstrap,
  Config,
  Event,
  ExperienceCraft,
  ExperienceCraftDetail,
  ExperimentRecord,
  KnowledgeItem,
  Mission,
  MissionDetail,
  ObserverMessage,
  Skill
} from "./types";
import {
  compact,
  eventLabel,
  eventTone,
  formatTime,
  groupFlow,
  isActiveMission,
  listify,
  percentage,
  relativeTime,
  safeJson,
  statusTone,
  toText
} from "./utils";
import "./styles.css";

const tabs: { id: AppTab; label: string }[] = [
  { id: "overview", label: "总览" },
  { id: "timeline", label: "时间线" },
  { id: "observer", label: "Observer" },
  { id: "memory", label: "记忆" },
  { id: "knowledge", label: "知识库" }
];

const tabButtonId = (tab: AppTab) => `mission-tab-${tab}`;
const tabPanelId = (tab: AppTab) => `mission-panel-${tab}`;

type ObserverDecisionView = Record<string, unknown>;
type ObserverObservationView = Record<string, unknown>;

const OBSERVER_DECISION_LABELS: Record<string, string> = {
  OK: "正常推进",
  WATCH: "观察",
  L1: "工具错误",
  L2: "证据不足",
  L3: "方向偏离",
  L4: "重复/偏差",
  ENV: "环境问题"
};

function missionHref(id: string) {
  return `/missions/${encodeURIComponent(id)}`;
}

function asRecord(value: unknown): Record<string, unknown> {
  return value && typeof value === "object" && !Array.isArray(value) ? (value as Record<string, unknown>) : {};
}

function asStringList(value: unknown): string[] {
  if (!value) return [];
  if (Array.isArray(value)) return value.map((item) => compact(item, 220)).filter(Boolean);
  if (typeof value === "object") {
    return Object.entries(value as Record<string, unknown>)
      .map(([key, item]) => `${key}: ${compact(item, 180)}`)
      .filter(Boolean);
  }
  const text = toText(value).trim();
  return text ? [text] : [];
}

function parseJsonObject(text: string): Record<string, unknown> {
  if (!text.trim()) return {};
  try {
    const parsed = JSON.parse(text);
    return asRecord(parsed);
  } catch {
    return {};
  }
}

function readJsonStringField(text: string, key: string): string {
  const match = text.match(new RegExp(`"${key}"\\s*:\\s*"((?:\\\\.|[^"\\\\])*)"`));
  if (!match) return "";
  try {
    return JSON.parse(`"${match[1]}"`);
  } catch {
    return match[1].replace(/\\"/g, '"');
  }
}

function readJsonNumberField(text: string, key: string): number | undefined {
  const match = text.match(new RegExp(`"${key}"\\s*:\\s*(-?\\d+)`));
  return match ? Number(match[1]) : undefined;
}

function parseTruncatedObservation(text: string): ObserverObservationView {
  if (!text.trim().startsWith("{")) return {};
  const mission = {
    target: readJsonStringField(text, "target"),
    goal: readJsonStringField(text, "goal"),
    scope: readJsonStringField(text, "scope"),
    status: readJsonStringField(text, "status")
  };
  const observation: ObserverObservationView = {
    phase: readJsonStringField(text, "phase")
  };
  const llmCallCount = readJsonNumberField(text, "llm_call_count");
  const stallRounds = readJsonNumberField(text, "stall_rounds");
  if (Object.values(mission).some(Boolean)) observation.mission = mission;
  if (llmCallCount !== undefined) observation.llm_call_count = llmCallCount;
  if (stallRounds !== undefined) observation.stall_rounds = stallRounds;
  return observation;
}

function observerDecisionFromMetadata(metadata: Record<string, unknown>, content = ""): ObserverDecisionView {
  const direct = asRecord(metadata.decision);
  if (Object.keys(direct).length) return direct;
  const observer = asRecord(metadata.observer);
  if (Object.keys(observer).length) return observer;
  return parseJsonObject(content);
}

function observerObservationFromMessage(message: ObserverMessage): ObserverObservationView {
  const metadata = asRecord(message.metadata);
  const parsed = parseJsonObject(message.content || "");
  const observation = Object.keys(parsed).length
    ? parsed
    : parseTruncatedObservation(message.content || "");
  const storedObservation = asRecord(metadata.observation);
  const merged = Object.keys(observation).length ? observation : storedObservation;
  if (!merged.phase && metadata.phase) merged.phase = metadata.phase;
  if (!Object.keys(asRecord(merged.rule_observation)).length && metadata.rule_decision) {
    merged.rule_observation = metadata.rule_decision;
  }
  return merged;
}

function observerVerdictLabel(verdict: unknown): string {
  const value = String(verdict || "OK").toUpperCase();
  const label = OBSERVER_DECISION_LABELS[value] || value;
  return value === label ? value : `${value} · ${label}`;
}

function observerVerdictClass(verdict: unknown): string {
  const value = String(verdict || "OK").toUpperCase();
  if (value === "OK") return "ok";
  if (value === "WATCH") return "watch";
  if (value === "ENV") return "env";
  if (value.startsWith("L")) return "interrupt";
  return "neutral";
}

function observerMessageTone(message: ObserverMessage): string {
  if (message.type === "decision") {
    return observerVerdictClass(observerDecisionFromMetadata(asRecord(message.metadata), message.content).verdict);
  }
  if (message.type === "observation") return "observation";
  if (message.type === "tool") return "tool";
  if (message.type === "think") return "think";
  return "neutral";
}

function observerPrimaryText(decision: ObserverDecisionView): string {
  return toText(
    decision.guidance ||
      decision.next_verification ||
      decision.rationale ||
      decision.primary_hypothesis ||
      "暂无纠偏建议"
  );
}

function observerDecisionItems(decision: ObserverDecisionView): [string, unknown][] {
  const items: [string, unknown][] = [
    ["判断理由", decision.rationale],
    ["下一步验证", decision.next_verification],
    ["需要补齐", decision.required_evidence],
    ["主假设", decision.primary_hypothesis],
    ["阻塞前提", decision.blocked_prerequisite],
    ["Skill 信号", decision.skill_signal]
  ];
  return items.filter(([, value]) => toText(value).trim());
}

function observerMemoryPatchItems(value: unknown): { key: string; items: string[] }[] {
  return Object.entries(asRecord(value))
    .map(([key, item]) => ({ key, items: asStringList(item) }))
    .filter((group) => group.items.length);
}

function observerToolCallItems(value: unknown): Record<string, unknown>[] {
  return Array.isArray(value) ? value.map(asRecord).filter((item) => Object.keys(item).length) : [];
}

function observerMemorySummary(value: unknown): string {
  const memory = asRecord(value);
  const summary = toText(memory.summary || "").trim();
  const findings = asStringList(memory.findings);
  const leads = asStringList(memory.leads);
  if (summary) return compact(summary, 220);
  if (findings.length) return compact(findings[0], 220);
  if (leads.length) return compact(leads[0], 220);
  return "暂无稳定摘要";
}

const configFields = [
  { key: "mock", label: "Mock 模式", type: "checkbox", section: "运行模式" },
  { key: "llm_base_url", label: "主模型 API 地址", type: "text", section: "主模型" },
  { key: "llm_api_key", label: "主模型 API Key", type: "password", section: "主模型" },
  { key: "llm_model", label: "主模型", type: "text", section: "主模型" },
  { key: "llm_timeout_sec", label: "模型超时秒数", type: "number", section: "主模型" },
  { key: "llm_reasoning_effort", label: "推理强度", type: "text", section: "主模型" },
  { key: "llm_use_responses_api", label: "Responses API", type: "checkbox", section: "主模型" },
  { key: "llm_disable_response_storage", label: "禁用响应存储", type: "checkbox", section: "主模型" },
  { key: "observer_base_url", label: "Observer API 地址", type: "text", section: "Observer" },
  { key: "observer_api_key", label: "Observer API Key", type: "password", section: "Observer" },
  { key: "observer_model", label: "Observer 模型", type: "text", section: "Observer" },
  { key: "observer_reasoning_effort", label: "Observer 推理强度", type: "text", section: "Observer" },
  { key: "compression_base_url", label: "压缩模型 API 地址", type: "text", section: "压缩模型" },
  { key: "compression_api_key", label: "压缩模型 API Key", type: "password", section: "压缩模型" },
  { key: "compression_model", label: "压缩模型", type: "text", section: "压缩模型" },
  { key: "compression_reasoning_effort", label: "压缩推理强度", type: "text", section: "压缩模型" },
  { key: "compression_timeout_sec", label: "压缩超时秒数", type: "number", section: "压缩模型" },
  { key: "compression_use_responses_api", label: "压缩 Responses API", type: "checkbox", section: "压缩模型" },
  { key: "compression_disable_response_storage", label: "压缩禁用响应存储", type: "checkbox", section: "压缩模型" },
  { key: "initial_rounds", label: "默认轮数", type: "number", section: "Agent 参数" },
  { key: "initial_commands", label: "每轮命令数", type: "number", section: "Agent 参数" },
  { key: "command_timeout_sec", label: "命令超时秒数", type: "number", section: "Agent 参数" },
  { key: "stdout_limit", label: "输出截断长度", type: "number", section: "Agent 参数" },
  { key: "memory_compress_interval", label: "记忆压缩轮次（主模型调用）", type: "number", section: "Agent 参数" },
  { key: "knowledge_top_k", label: "知识库检索数", type: "number", section: "Agent 参数" },
  { key: "skills_dir", label: "Skills 目录", type: "text", section: "Agent 参数" },
  { key: "skills_auto_use", label: "自动启用 Skill", type: "checkbox", section: "Agent 参数" }
] as const;

function App() {
  const isSettings = window.location.pathname.endsWith("/settings.html");
  const missionMatch = window.location.pathname.match(/^\/missions\/([^/?#]+)/);
  if (isSettings) return <SettingsPage />;
  if (missionMatch) return <MissionDetailPage missionId={decodeURIComponent(missionMatch[1])} />;
  return <MissionControl />;
}

function MissionControl() {
  const [bootstrap, setBootstrap] = useState<Bootstrap | null>(null);
  const [agentSlots, setAgentSlots] = useState<AgentSlot[]>([]);
  const [missions, setMissions] = useState<Mission[]>([]);
  const [experiments, setExperiments] = useState<ExperimentRecord[]>([]);
  const [skills, setSkills] = useState<Skill[]>([]);
  const [loading, setLoading] = useState(true);
  const [notice, setNotice] = useState("");
  const [error, setError] = useState("");
  const [isPending, startTransition] = useTransition();

  useEffect(() => {
    let cancelled = false;
    async function boot() {
      try {
        const [bootData, missionData, experimentData, skillData] = await Promise.all([
          api.bootstrap(),
          api.missions(),
          api.experiments(),
          api.skills()
        ]);
        if (cancelled) return;
        setBootstrap(bootData);
        setAgentSlots(missionData.agent_slots || bootData.agent_slots || []);
        setMissions(missionData.missions || []);
        setExperiments(experimentData.records || []);
        setSkills(skillData.skills || []);
      } catch (err) {
        if (!cancelled) setError(readError(err));
      } finally {
        if (!cancelled) setLoading(false);
      }
    }
    boot();
    return () => {
      cancelled = true;
    };
  }, []);

  useEffect(() => {
    let disposed = false;
    async function refresh() {
      try {
        const [missionData, experimentData] = await Promise.all([api.missions(), api.experiments()]);
        if (disposed) return;
        startTransition(() => {
          setMissions(missionData.missions || []);
          setAgentSlots(missionData.agent_slots || []);
          setExperiments(experimentData.records || []);
        });
      } catch (err) {
        if (!disposed) setError(readError(err));
      }
    }
    const timer = window.setInterval(refresh, 3000);
    return () => {
      disposed = true;
      window.clearInterval(timer);
    };
  }, []);

  const runningCount = missions.filter((mission) => isActiveMission(mission)).length;
  const activeAgentCount = agentSlots.filter((slot) => slot.status === "running").length;
  const flagCount = missions.reduce((sum, mission) => sum + (mission.captured_flag_count || 0), 0);

  async function refreshAll() {
    const [missionData, experimentData] = await Promise.all([api.missions(), api.experiments()]);
    setMissions(missionData.missions || []);
    setAgentSlots(missionData.agent_slots || []);
    setExperiments(experimentData.records || []);
  }

  async function handleCreated(id: string) {
    setNotice("任务已创建，正在进入队列。");
    await refreshAll();
    window.location.href = missionHref(id);
  }

  return (
    <div className="app-shell mission-shell">
      <Atmosphere />
      <Header bootstrap={bootstrap} active="missions" />
      <main className="command-center">
        <DashboardStrip
          loading={loading || isPending}
          model={bootstrap?.model}
          runningCount={agentSlots.length ? activeAgentCount : runningCount}
          flagCount={flagCount}
          missionCount={missions.length}
          knowledgeDocs={bootstrap?.knowledge?.total_docs || bootstrap?.knowledge?.total_chunks || 0}
        />

        {notice ? <InlineNotice tone="ok" message={notice} onClose={() => setNotice("")} /> : null}
        {error ? <InlineNotice tone="bad" message={error} actionLabel="重新同步" onAction={refreshAll} onClose={() => setError("")} /> : null}

        <section className="mission-home-grid">
          <aside className="mission-home-fleet">
            <AgentFleetPanel bootstrap={bootstrap} agentSlots={agentSlots} />
          </aside>

          <div className="mission-home-main">
            <MissionList missions={missions} onSelect={(id) => window.location.assign(missionHref(id))} />
          </div>

          <aside className="mission-home-side">
            <MissionLaunch
              defaults={bootstrap?.defaults}
              skills={skills}
              hasMissions={missions.length > 0}
              onCreated={handleCreated}
              onError={setError}
            />
            <RuntimeOverviewPanel bootstrap={bootstrap} skills={skills} experiments={experiments} />
          </aside>
        </section>
      </main>
    </div>
  );
}

function MissionDetailPage({ missionId }: { missionId: string }) {
  const [bootstrap, setBootstrap] = useState<Bootstrap | null>(null);
  const [agentSlots, setAgentSlots] = useState<AgentSlot[]>([]);
  const [missions, setMissions] = useState<Mission[]>([]);
  const [experiments, setExperiments] = useState<ExperimentRecord[]>([]);
  const [skills, setSkills] = useState<Skill[]>([]);
  const [detail, setDetail] = useState<MissionDetail | null>(null);
  const [activeTab, setActiveTab] = useState<AppTab>("timeline");
  const [loading, setLoading] = useState(true);
  const [detailLoading, setDetailLoading] = useState(false);
  const [notice, setNotice] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    let cancelled = false;
    async function boot() {
      try {
        const [bootData, missionData, experimentData, skillData] = await Promise.all([
          api.bootstrap(),
          api.missions(),
          api.experiments(),
          api.skills()
        ]);
        if (cancelled) return;
        setBootstrap(bootData);
        setAgentSlots(missionData.agent_slots || bootData.agent_slots || []);
        setMissions(missionData.missions || []);
        setExperiments(experimentData.records || []);
        setSkills(skillData.skills || []);
      } catch (err) {
        if (!cancelled) setError(readError(err));
      } finally {
        if (!cancelled) setLoading(false);
      }
    }
    boot();
    return () => {
      cancelled = true;
    };
  }, []);

  useEffect(() => {
    let disposed = false;
    async function loadDetail(showLoading: boolean) {
      if (showLoading) setDetailLoading(true);
      try {
        const [missionData, experimentData, nextDetail] = await Promise.all([
          api.missions(),
          api.experiments(),
          api.missionDetail(missionId)
        ]);
        if (disposed) return;
        setMissions(missionData.missions || []);
        setAgentSlots(missionData.agent_slots || []);
        setExperiments(experimentData.records || []);
        setDetail(nextDetail);
      } catch (err) {
        if (!disposed) setError(readError(err));
      } finally {
        if (!disposed && showLoading) setDetailLoading(false);
      }
    }
    loadDetail(true);
    const timer = window.setInterval(() => loadDetail(false), 3000);
    return () => {
      disposed = true;
      window.clearInterval(timer);
    };
  }, [missionId]);

  const mission = detail?.mission || missions.find((item) => item.id === missionId) || null;
  async function refreshAll() {
    const [missionData, experimentData, nextDetail] = await Promise.all([
      api.missions(),
      api.experiments(),
      api.missionDetail(missionId)
    ]);
    setMissions(missionData.missions || []);
    setAgentSlots(missionData.agent_slots || []);
    setExperiments(experimentData.records || []);
    setDetail(nextDetail);
  }

  async function missionAction(action: "stop" | "resume" | "delete") {
    if (!mission) return;
    setError("");
    try {
      if (action === "stop") await api.stopMission(mission.id);
      if (action === "resume") await api.resumeMission(mission.id);
      if (action === "delete") {
        const ok = window.confirm(`删除任务 ${mission.name}？该操作不会停止运行中的任务。`);
        if (!ok) return;
        await api.deleteMission(mission.id);
        window.location.href = "/";
        return;
      }
      setNotice(action === "stop" ? "停止请求已发送。" : "任务已请求继续。");
      await refreshAll();
    } catch (err) {
      setError(readError(err));
    }
  }

  function handleTabKeyDown(event: React.KeyboardEvent<HTMLButtonElement>, tabId: AppTab) {
    const currentIndex = tabs.findIndex((tab) => tab.id === tabId);
    const lastIndex = tabs.length - 1;
    let nextIndex = currentIndex;
    if (event.key === "ArrowRight") nextIndex = currentIndex === lastIndex ? 0 : currentIndex + 1;
    if (event.key === "ArrowLeft") nextIndex = currentIndex === 0 ? lastIndex : currentIndex - 1;
    if (event.key === "Home") nextIndex = 0;
    if (event.key === "End") nextIndex = lastIndex;
    if (nextIndex === currentIndex) return;
    event.preventDefault();
    const nextTab = tabs[nextIndex];
    setActiveTab(nextTab.id);
    window.requestAnimationFrame(() => document.getElementById(tabButtonId(nextTab.id))?.focus());
  }

  return (
    <div className="app-shell mission-shell detail-shell">
      <Atmosphere />
      <Header bootstrap={bootstrap} active="missions" />
      <main className="mission-detail-page">
        <div className="detail-back-row">
          <a className="ghost-button" href="/">
            返回实例总览
          </a>
          <span>{detailLoading ? "同步中" : loading ? "加载中" : "自动刷新 · 3s"}</span>
        </div>

        {notice ? <InlineNotice tone="ok" message={notice} onClose={() => setNotice("")} /> : null}
        {error ? <InlineNotice tone="bad" message={error} actionLabel="重新同步" onAction={refreshAll} onClose={() => setError("")} /> : null}

        <section className="mission-detail-top">
          <MissionDetailHeader
            mission={mission}
            detail={detail}
            detailLoading={detailLoading}
            onStop={() => void missionAction("stop")}
            onResume={() => void missionAction("resume")}
            onDelete={() => void missionAction("delete")}
          />

          <div className="tabs" role="tablist" aria-label="任务视图">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                id={tabButtonId(tab.id)}
                type="button"
                role="tab"
                aria-selected={activeTab === tab.id}
                aria-controls={tabPanelId(tab.id)}
                tabIndex={activeTab === tab.id ? 0 : -1}
                className={activeTab === tab.id ? "tab active" : "tab"}
                onClick={() => setActiveTab(tab.id)}
                onKeyDown={(event) => handleTabKeyDown(event, tab.id)}
              >
                {tab.label}
              </button>
            ))}
          </div>
        </section>

        <section className="mission-detail-grid">
          <div className="detail-content-column">
            <MissionPane
              tab={activeTab}
              detail={detail}
              experiments={experiments}
              onError={setError}
              onNotice={setNotice}
              onRefresh={refreshAll}
            />
          </div>
          <aside className="detail-side-column">
            <LiveAgentPanel agentSlots={agentSlots} missionId={missionId} />
            <LiveSummaryPanel detail={detail} mission={mission} />
          </aside>
        </section>
      </main>
    </div>
  );
}

function Header({ bootstrap, active }: { bootstrap: Bootstrap | null; active: "missions" | "settings" }) {
  return (
    <header className="topbar">
      <a className="brand" href="/">
        <span className="brand-mark">PQ</span>
        <span>
          <strong>PikaQiu</strong>
          <small>Mission Control</small>
        </span>
      </a>
      <nav className="nav">
        <a className={active === "missions" ? "active" : ""} href="/">
          任务
        </a>
        <a className={active === "settings" ? "active" : ""} href="/settings.html">
          配置
        </a>
      </nav>
      <div className="top-status" aria-label="运行状态">
        <span className="live-dot" />
        <span>{bootstrap?.llm_mode || "loading"}</span>
        <span className="divider" />
        <span>{bootstrap?.model || "model pending"}</span>
      </div>
    </header>
  );
}

function Atmosphere() {
  return (
    <div className="atmosphere" aria-hidden="true">
      <span className="orb orb-a" />
      <span className="orb orb-b" />
      <span className="grid-glow" />
    </div>
  );
}

function DashboardStrip({
  loading,
  model,
  runningCount,
  flagCount,
  missionCount,
  knowledgeDocs
}: {
  loading: boolean;
  model?: string;
  runningCount: number;
  flagCount: number;
  missionCount: number;
  knowledgeDocs: number;
}) {
  const metrics = [
    { label: "模型", value: model || "未就绪", icon: <Brain /> },
    { label: "运行任务", value: String(runningCount), icon: <Pulse /> },
    { label: "累计 Flag", value: String(flagCount), icon: <FlagBanner /> },
    { label: "任务记录", value: String(missionCount), icon: <Graph /> },
    { label: "知识条目", value: String(knowledgeDocs), icon: <Database /> }
  ];
  return (
    <section className={loading ? "dashboard-strip loading" : "dashboard-strip"}>
      {metrics.map((metric) => (
        <div className="metric" key={metric.label}>
          <span className="metric-icon">{metric.icon}</span>
          <span className="metric-label">{metric.label}</span>
          <strong>{metric.value}</strong>
        </div>
      ))}
    </section>
  );
}

function MissionLaunch({
  defaults,
  skills,
  hasMissions,
  onCreated,
  onError
}: {
  defaults?: Bootstrap["defaults"];
  skills: Skill[];
  hasMissions: boolean;
  onCreated: (id: string) => Promise<void>;
  onError: (message: string) => void;
}) {
  const [submitting, setSubmitting] = useState(false);
  const [selectedSkills, setSelectedSkills] = useState<string[]>([]);
  const [skillDialogOpen, setSkillDialogOpen] = useState(false);
  const [expanded, setExpanded] = useState(() => !hasMissions);
  const autoCollapsed = useRef(false);

  useEffect(() => {
    if (hasMissions && !autoCollapsed.current) {
      autoCollapsed.current = true;
      setExpanded(false);
    }
  }, [hasMissions]);

  async function submit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSubmitting(true);
    onError("");
    const formElement = event.currentTarget;
    const form = new FormData(formElement);
    const payload = {
      name: String(form.get("name") || "Pentest"),
      target: String(form.get("target") || "").trim(),
      goal: String(form.get("goal") || "").trim(),
      max_rounds: Number(form.get("max_rounds") || defaults?.max_rounds || 4),
      max_commands: Number(form.get("max_commands") || defaults?.max_commands || 64),
      command_timeout_sec: Number(form.get("command_timeout_sec") || defaults?.command_timeout_sec || 300),
      expected_flags: Number(form.get("expected_flags") || 1),
      skills: selectedSkills
    };
    try {
      const response = await api.createMission(payload);
      formElement.reset();
      setSelectedSkills([]);
      await onCreated(response.mission_id);
    } catch (err) {
      onError(readError(err));
    } finally {
      setSubmitting(false);
    }
  }

  function toggleSkill(id: string) {
    setSelectedSkills((current) => (current.includes(id) ? current.filter((item) => item !== id) : [...current, id]));
  }

  const selectedSkillNames = selectedSkills
    .map((id) => skills.find((skill) => skill.id === id)?.name || id)
    .join("、");

  return (
    <details className="panel launch-panel" open={expanded} onToggle={(event) => setExpanded(event.currentTarget.open)}>
      <summary className="panel-heading">
        <span className="panel-icon">
          <Plus />
        </span>
        <div>
          <h2>发起任务</h2>
          <p>定义目标、范围和终止条件。</p>
        </div>
        <span className="summary-action">{expanded ? "收起" : "展开"}</span>
      </summary>
      <form className="mission-form" onSubmit={submit}>
        <label>
          任务名
          <input name="name" defaultValue="Pentest" required />
        </label>
        <label>
          目标地址
          <input name="target" placeholder="http://127.0.0.1:8080" required />
        </label>
        <label>
          目标说明
          <textarea name="goal" rows={3} placeholder="例如：找到并提交所有 flag，记录可复现路径。" required />
        </label>
        <div className="form-grid">
          <label>
            最大轮数
            <input name="max_rounds" type="number" min={1} max={200} defaultValue={defaults?.max_rounds || 4} />
          </label>
          <label>
            每轮命令
            <input name="max_commands" type="number" min={1} max={500} defaultValue={defaults?.max_commands || 64} />
          </label>
          <label>
            超时秒数
            <input
              name="command_timeout_sec"
              type="number"
              min={5}
              max={600}
              defaultValue={defaults?.command_timeout_sec || 300}
            />
          </label>
          <label>
            Flag 数量
            <input name="expected_flags" type="number" min={1} max={50} defaultValue={1} />
          </label>
        </div>
        {skills.length ? (
          <div className="skill-select-summary">
            <div>
              <span>Skills</span>
              <strong>{selectedSkills.length ? `${selectedSkills.length} 个已选择` : "默认自动判断"}</strong>
              <p>{selectedSkills.length ? selectedSkillNames : "不手动指定时，主 Agent 会按任务目标自动选择可用 Skill。"}</p>
            </div>
            <button type="button" className="ghost-button slim" onClick={() => setSkillDialogOpen(true)}>
              选择 Skill
            </button>
          </div>
        ) : null}
        <button className="primary-button" type="submit" disabled={submitting}>
          <Lightning weight="fill" />
          {submitting ? "创建中" : "启动任务"}
        </button>
      </form>
      {skillDialogOpen ? (
        <SkillPickerDialog
          skills={skills}
          selectedSkills={selectedSkills}
          onToggle={toggleSkill}
          onClear={() => setSelectedSkills([])}
          onClose={() => setSkillDialogOpen(false)}
        />
      ) : null}
    </details>
  );
}

function SkillPickerDialog({
  skills,
  selectedSkills,
  onToggle,
  onClear,
  onClose
}: {
  skills: Skill[];
  selectedSkills: string[];
  onToggle: (id: string) => void;
  onClear: () => void;
  onClose: () => void;
}) {
  return (
    <div className="modal-backdrop" role="presentation" onMouseDown={onClose}>
      <section
        className="skill-dialog"
        role="dialog"
        aria-modal="true"
        aria-labelledby="skill-dialog-title"
        onMouseDown={(event) => event.stopPropagation()}
      >
        <header className="skill-dialog-head">
          <div>
            <h2 id="skill-dialog-title">选择任务 Skill</h2>
            <p>可手动指定主 Agent 起步时加载的能力；留空则保持自动判断。</p>
          </div>
          <button type="button" className="ghost-button slim" onClick={onClose}>
            关闭
          </button>
        </header>
        <div className="skill-dialog-list">
          {skills.map((skill) => {
            const selected = selectedSkills.includes(skill.id);
            const tags = skill.tags?.length ? skill.tags.slice(0, 4).join(" / ") : "未标注标签";
            return (
              <button
                key={skill.id}
                type="button"
                className={selected ? "skill-option selected" : "skill-option"}
                onClick={() => onToggle(skill.id)}
                aria-pressed={selected}
              >
                <span className="skill-option-check">{selected ? "已选" : "可选"}</span>
                <strong>{skill.name || skill.id}</strong>
                <small>{tags}</small>
                <p>{skill.description || "该 Skill 暂无描述。"}</p>
              </button>
            );
          })}
        </div>
        <footer className="skill-dialog-actions">
          <button type="button" className="ghost-button" onClick={onClear} disabled={!selectedSkills.length}>
            清空选择
          </button>
          <button type="button" className="primary-button" onClick={onClose}>
            确认选择 {selectedSkills.length ? `(${selectedSkills.length})` : ""}
          </button>
        </footer>
      </section>
    </div>
  );
}

function MissionList({
  missions,
  onSelect
}: {
  missions: Mission[];
  onSelect: (id: string) => void;
}) {
  return (
    <section className="panel mission-list-panel">
      <div className="panel-heading compact">
        <span className="panel-icon">
          <CompassTool />
        </span>
        <div>
          <h2>任务队列</h2>
          <p>{missions.length ? `${missions.length} 条记录` : "等待首个目标"}</p>
        </div>
      </div>
      <div className="mission-list">
        {missions.length ? (
          missions.map((mission) => (
            <button
              key={mission.id}
              type="button"
              className="mission-card"
              aria-label={`${mission.name}，状态 ${mission.status}，目标 ${mission.target}，${relativeTime(mission.updated_at)}${mission.captured_flag_count ? `，${mission.captured_flag_count} 个 flag` : ""}`}
              onClick={() => onSelect(mission.id)}
            >
              <span className={`status-badge ${statusTone(mission.status)}`}>{mission.status}</span>
              <strong>{mission.name}</strong>
              <span className="mission-target">{mission.target}</span>
              <span className="mission-meta">
                <ClockCounterClockwise />
                {relativeTime(mission.updated_at)}
                {mission.captured_flag_count ? ` · ${mission.captured_flag_count} flag` : ""}
              </span>
              <span className="mission-open-hint">打开实例详情</span>
            </button>
          ))
        ) : (
          <EmptyState title="暂无任务" body="展开上方表单创建目标，任务启动后这里会显示状态、目标和最近更新。" compact />
        )}
      </div>
    </section>
  );
}

function MissionDetailHeader({
  mission,
  detail,
  detailLoading,
  onStop,
  onResume,
  onDelete
}: {
  mission: Mission | null;
  detail: MissionDetail | null;
  detailLoading: boolean;
  onStop: () => void;
  onResume: () => void;
  onDelete: () => void;
}) {
  if (!mission) {
    return (
      <section className="mission-hero empty-hero">
        <div>
          <p className="kicker">NO MISSION SELECTED</p>
          <h1>选择一个任务，或发起新的攻防流程。</h1>
          <p>页面会自动轮询后端，将命令、Observer 审核和记忆整理到同一条时间线。</p>
        </div>
      </section>
    );
  }
  const currentRound = Math.max(
    0,
    ...(detail?.rounds.map((round) => round.round_no) || []),
    ...(detail?.events.map((event) => event.round_no).filter((roundNo) => roundNo > 0) || [])
  );
  const progress = mission.status === "done" ? 100 : percentage(currentRound, mission.max_rounds);
  const active = isActiveMission(mission, detail?.thread_alive);
  return (
    <section className="mission-hero">
      <div className="mission-title-block">
        <p className="kicker">{mission.id}</p>
        <h1>{mission.name}</h1>
        <p>{mission.goal || "未填写目标说明。"}</p>
        <div className="hero-tags">
          <span>{mission.target}</span>
          <span>{mission.model}</span>
          <span>{formatTime(mission.updated_at)}</span>
        </div>
      </div>
      <div className="mission-command-card">
        <div className="command-copy">
          <span className={`status-badge ${statusTone(mission.status)}`}>{mission.status}</span>
          <strong>
            R{String(currentRound).padStart(2, "0")} / {mission.max_rounds}
          </strong>
          <div className="progress-line" aria-label={`任务进度 ${progress}%`}>
            <span style={{ width: `${progress}%` }} />
          </div>
          <small>{detail?.thread_alive ? "worker alive" : detailLoading ? "同步中" : `worker idle · ${progress}%`}</small>
        </div>
        <div className="action-row">
          <button type="button" className="ghost-button" onClick={onResume} disabled={active}>
            <Play />
            继续
          </button>
          <button type="button" className="ghost-button" onClick={onStop} disabled={!active}>
            <Pause />
            停止
          </button>
          <button type="button" className="danger-button" onClick={onDelete} disabled={active}>
            <Trash />
            删除
          </button>
        </div>
      </div>
    </section>
  );
}

function RuntimeOverviewPanel({
  bootstrap,
  skills,
  experiments
}: {
  bootstrap: Bootstrap | null;
  skills: Skill[];
  experiments: ExperimentRecord[];
}) {
  const knowledgeStatus = bootstrap?.knowledge?.rag?.available
    ? `${bootstrap.knowledge.rag.total_chunks || 0} chunks`
    : bootstrap?.knowledge?.status || bootstrap?.knowledge?.search_backend || "未加载";
  const loadedEnabledSkills = skills.filter((skill) => skill.enabled).length;
  const enabledSkills = Math.max(Number(bootstrap?.skills?.enabled || 0), loadedEnabledSkills);
  const totalSkills = Math.max(Number(bootstrap?.skills?.total || 0), skills.length);
  const success = experiments.filter((item) => item.outcome === "success").length;
  return (
    <section className="panel runtime-overview" aria-label="运行环境摘要">
      <div className="panel-heading compact">
        <span className="panel-icon">
          <Database />
        </span>
        <div>
          <h2>运行环境</h2>
          <p>沙箱、知识库和 Skill 状态。</p>
        </div>
      </div>
      <div className="runtime-overview-grid">
        <RuntimeLine label="工作目录" value={bootstrap?.sandbox_workdir || "未加载"} />
        <RuntimeLine label="知识库" value={knowledgeStatus} />
        <RuntimeLine label="Skills" value={`${enabledSkills}/${totalSkills} enabled`} />
        <RuntimeLine label="归档成功" value={`${success}/${experiments.length}`} />
      </div>
    </section>
  );
}

function AgentFleetPanel({
  bootstrap,
  agentSlots,
  currentMissionId
}: {
  bootstrap: Bootstrap | null;
  agentSlots: AgentSlot[];
  currentMissionId?: string;
}) {
  const slots = agentSlots.length ? agentSlots : bootstrap?.agent_slots || [];
  return (
    <section className="panel agent-fleet-panel" aria-label="Agent 槽位">
      <div className="panel-heading compact">
        <span className="panel-icon">
          <Circuitry />
        </span>
        <div>
          <h2>Agent 编队</h2>
          <p>{slots.length ? `${slots.length} 个沙箱槽位` : "等待后端同步槽位"}</p>
        </div>
      </div>
      <div className="agent-fleet-list">
        {slots.map((slot) => (
          <AgentSlotCard key={slot.agent_id || slot.slot} slot={slot} currentMissionId={currentMissionId} />
        ))}
        {!slots.length ? <EmptyState compact title="暂无 Agent 槽" body="启动后端后，这里会显示最多五个并行 Agent。" /> : null}
      </div>
    </section>
  );
}

function AgentSlotCard({ slot, currentMissionId }: { slot: AgentSlot; currentMissionId?: string }) {
  const running = slot.status === "running";
  const isCurrent = Boolean(currentMissionId && slot.mission_id === currentMissionId);
  const linked = Boolean(slot.mission_id);
  const reason =
    slot.status_reason === "flag_captured"
      ? `空闲 · ${slot.captured_flag_count} flag`
      : slot.status_reason === "not_started"
        ? "空闲 · 未启动"
        : running
          ? "运行中"
          : "空闲";
  const title = slot.mission_name || "等待任务";
  const target = slot.target || "暂无目标";
  const container = slot.container || "未绑定沙箱";
  const className = [
    "agent-slot",
    running ? "running" : "idle",
    isCurrent ? "current" : "",
    linked ? "linked" : ""
  ].filter(Boolean).join(" ");
  const body = (
    <>
      <div className="agent-slot-head">
        <span className="agent-index">A{slot.slot}</span>
        <span className={`status-badge ${running ? "live" : slot.captured_flag_count ? "ok" : "idle"}`}>{reason}</span>
      </div>
      <div className="agent-slot-body">
        <strong title={title}>{title}</strong>
        <small title={target}>{target}</small>
      </div>
      <div className="agent-slot-foot">
        <em title={container}>{container}</em>
        <span>{slot.captured_flag_count || 0} flag</span>
      </div>
    </>
  );
  if (linked) {
    return (
      <a className={className} href={missionHref(slot.mission_id)} aria-current={isCurrent ? "page" : undefined}>
        {body}
      </a>
    );
  }
  return (
    <article className={className}>
      {body}
    </article>
  );
}

function LiveAgentPanel({ agentSlots, missionId }: { agentSlots: AgentSlot[]; missionId: string }) {
  const current = agentSlots.find((slot) => slot.mission_id === missionId);
  return (
    <section className="panel live-agent-panel">
      <div className="section-title">
        <Circuitry />
        <div>
          <h2>当前 Agent</h2>
          <p>{current ? `A${current.slot} · ${current.container}` : "尚未绑定运行槽位"}</p>
        </div>
      </div>
      {current ? (
        <div className="agent-large-card">
          <span className={`status-badge ${current.status === "running" ? "live" : "idle"}`}>{current.status}</span>
          <strong>A{current.slot}</strong>
          <p>{current.status_reason || "等待状态更新"}</p>
          <small>{current.target || current.container}</small>
        </div>
      ) : (
        <EmptyState compact title="Agent 空闲或未启动" body="实例进入队列后会在这里显示绑定的沙箱和槽位。" />
      )}
    </section>
  );
}

function LiveSummaryPanel({ detail, mission }: { detail: MissionDetail | null; mission: Mission | null }) {
  const latest = detail?.observer?.latest_decision || {};
  const latestEvents = detail?.events.slice(-3).reverse() || [];
  return (
    <section className="panel live-summary-panel">
      <div className="section-title">
        <ShieldCheck />
        <div>
          <h2>实时摘要</h2>
          <p>{mission ? `${mission.status} · ${formatTime(mission.updated_at)}` : "等待实例数据"}</p>
        </div>
      </div>
      <div className="brief-grid single">
        <BriefItem label="Memory" value={detail?.memory.summary || "暂无记忆摘要。"} />
        <BriefItem label="Observer" value={toText(latest.verdict || latest.rationale || "暂无审核结论")} />
        <BriefItem label="Flag" value={`${detail?.captured_flag_count || 0} / ${mission?.expected_flags || 1}`} mono />
      </div>
      <div className="mini-event-stack">
        {latestEvents.length ? (
          latestEvents.map((event) => (
            <article key={event.id} className="mini-event">
              <span className="trace-type">{eventLabel(event.type)}</span>
              <strong>{event.title || compact(event.command || event.content, 96)}</strong>
              <small>R{event.round_no} · {formatTime(event.ended_at || event.started_at)}</small>
            </article>
          ))
        ) : (
          <p className="muted">暂无最近事件。</p>
        )}
      </div>
    </section>
  );
}

function MissionPane({
  tab,
  detail,
  experiments,
  onError,
  onNotice,
  onRefresh
}: {
  tab: AppTab;
  detail: MissionDetail | null;
  experiments: ExperimentRecord[];
  onError: (message: string) => void;
  onNotice: (message: string) => void;
  onRefresh: () => Promise<void>;
}) {
  let content: React.ReactNode;
  if (!detail) {
    content = (
      <EmptyState
        title="等待任务数据"
        body="选择左侧任务，或展开发起任务表单创建新目标。这里会显示总览、时间线、Observer、记忆和知识库。"
        large
      />
    );
  } else if (tab === "overview") {
    content = <OverviewTab detail={detail} experiments={experiments} onError={onError} onNotice={onNotice} onRefresh={onRefresh} />;
  } else if (tab === "timeline") {
    content = <TimelineTab detail={detail} prominent />;
  } else if (tab === "observer") {
    content = <ObserverTab detail={detail} />;
  } else if (tab === "memory") {
    content = <MemoryTab detail={detail} />;
  } else {
    content = <KnowledgeTab mission={detail.mission} onError={onError} onNotice={onNotice} />;
  }
  return (
    <div
      className="tab-panel-scroll"
      id={tabPanelId(tab)}
      role="tabpanel"
      aria-labelledby={tabButtonId(tab)}
      tabIndex={0}
    >
      {content}
    </div>
  );
}

function OverviewTab({
  detail,
  experiments,
  onError,
  onNotice,
  onRefresh
}: {
  detail: MissionDetail;
  experiments: ExperimentRecord[];
  onError: (message: string) => void;
  onNotice: (message: string) => void;
  onRefresh: () => Promise<void>;
}) {
  const { mission, memory, events, rounds } = detail;
  const latestEvents = events.slice(-6).reverse();
  const experiment = detail.experiment || experiments.find((record) => record.mission_id === mission.id) || null;
  return (
    <div className="tab-grid overview-grid">
      <div className="overview-main">
        <section className="panel judgement-panel">
          <div className="section-title">
            <ShieldCheck />
            <div>
              <h2>当前判断</h2>
              <p>目标、阻塞点和下一步压缩成可读指挥面板。</p>
            </div>
          </div>
          <div className="brief-grid">
            <BriefItem label="摘要" value={memory.summary || "暂未形成稳定摘要。"} />
            <BriefItem label="当前线索" value={String(memory.leads?.[0] || "暂无")} />
            <BriefItem label="最近发现" value={String(memory.findings?.[0] || "暂无")} />
            <BriefItem label="任务状态" value={mission.error_message || "未阻塞"} />
          </div>
        </section>

        <section className="panel recent-activity-panel">
          <div className="section-title">
            <TerminalWindow />
            <div>
              <h2>最近活动</h2>
              <p>{rounds.length} 条模型轮次，{events.length} 条事件。</p>
            </div>
          </div>
          <EventStream events={latestEvents} />
        </section>
      </div>

      <div className="overview-side">
        <section className="panel flag-panel">
          <div className="section-title">
            <FlagBanner />
            <div>
              <h2>Flag 状态</h2>
              <p>{detail.captured_flag_count} / {mission.expected_flags || 1}</p>
            </div>
          </div>
          <div className="flag-stack">
            {detail.captured_flags.length ? (
              detail.captured_flags.map((flag) => (
                <code className="flag-chip" key={flag}>
                  {flag}
                </code>
              ))
            ) : (
              <EmptyState title="尚未捕获 Flag" body="捕获后会在这里固定显示。" />
            )}
          </div>
        </section>

        <HumanCollaborationPanel detail={detail} onError={onError} onNotice={onNotice} onRefresh={onRefresh} />
        <ExperimentEditor missionId={mission.id} experiment={experiment} onError={onError} onNotice={onNotice} onRefresh={onRefresh} />
      </div>
    </div>
  );
}

function TimelineTab({ detail, prominent }: { detail: MissionDetail; prominent?: boolean }) {
  const groups = groupFlow(detail.rounds, detail.events);
  const eventCount = detail.events.length;
  const roundCount = detail.rounds.length;
  return (
    <section className={prominent ? "panel flow-panel prominent" : "panel flow-panel"}>
      <div className="section-title">
        <Pulse />
        <div>
          <h2>执行时间线</h2>
          <p>按 round 聚合模型决策、命令输出和系统事件。{roundCount} 条模型记录，{eventCount} 条事件。</p>
        </div>
      </div>
      {groups.length ? (
        <div className="flow-list">
          {groups.map((group) => (
            <article className="flow-round" key={group.roundNo}>
              <div className="round-marker">R{String(group.roundNo).padStart(2, "0")}</div>
              <div className="round-body">
                {group.rounds.map((round, index) => (
                  <details className="trace-card model-card" key={`${round.worker_role}-${index}`}>
                    <summary>
                      <span className="trace-type">{round.worker_role}</span>
                      <strong>{compact(round.prompt_excerpt || round.raw_response, 140)}</strong>
                      <small>{formatTime(round.created_at)}</small>
                    </summary>
                    <pre>{round.raw_response || safeJson(round.decision)}</pre>
                  </details>
                ))}
                {group.events.map((event) => (
                  <EventCard event={event} key={event.id} />
                ))}
              </div>
            </article>
          ))}
        </div>
      ) : (
        <EmptyState title="暂无时间线" body="任务开始执行后，round 和事件会出现在这里。" large />
      )}
    </section>
  );
}

function ObserverTab({ detail }: { detail: MissionDetail }) {
  const observer = detail.observer;
  const latest = observer.latest_decision || {};
  const messages = observer.messages || [];
  return (
    <div className="tab-grid">
      <section className="panel span-2">
        <div className="section-title">
          <Circuitry />
          <div>
            <h2>被动 Observer</h2>
            <p>Observer 不再是可调用工具，而是在每轮结束后被动审核主模型轨迹。</p>
          </div>
        </div>
        <div className="observer-stats">
          <MetricTile label="状态" value={observer.status || "idle"} />
          <MetricTile label="最新结论" value={toText(latest.verdict || "OK")} />
          <MetricTile label="审核次数" value={String(observer.stats?.decisions || 0)} />
          <MetricTile label="WATCH" value={String(observer.stats?.watch || 0)} />
          <MetricTile label="L/ENV" value={String(observer.stats?.interrupts || 0)} />
          <MetricTile label="记忆补丁" value={String(observer.stats?.memory_patches || 0)} />
          <MetricTile label="Skill 信号" value={String(observer.stats?.skill_signals || 0)} />
        </div>
        <div className="decision-board">
          <BriefItem label="Verdict" value={toText(latest.verdict || "OK")} />
          <BriefItem label="Rationale" value={toText(latest.rationale || "暂无最新判断")} />
          <BriefItem label="支撑依据" value={toText(latest.evidence || "暂无依据")} />
          <BriefItem label="Guidance" value={toText(latest.guidance || "无纠偏")} />
          <BriefItem label="Next" value={toText(latest.next_verification || "无需额外验证")} />
          <BriefItem label="需补充验证" value={toText(latest.required_evidence || "无")} />
        </div>
      </section>
      <section className="panel span-2">
        <div className="section-title">
          <Brain />
          <div>
            <h2>Observer 消息</h2>
            <p>{messages.length ? `${messages.length} 条最近消息` : "尚无消息"}</p>
          </div>
        </div>
        {messages.length ? (
          <div className="message-stack">
            {messages.slice().reverse().map((message) => (
              <ObserverMessageCard message={message} key={message.id} />
            ))}
          </div>
        ) : (
          <EmptyState title="Observer 尚未介入" body="任务完成首轮后，这里会出现被动审核结果。" />
        )}
      </section>
    </div>
  );
}

function MemoryTab({ detail }: { detail: MissionDetail }) {
  const memory = detail.memory;
  const groups = [
    ["Findings", memory.findings],
    ["Leads", memory.leads],
    ["Credentials", memory.credentials],
    ["Dead Ends", memory.dead_ends],
    ["Topology", memory.topology]
  ] as const;
  return (
    <div className="tab-grid">
      <section className="panel span-2">
        <div className="section-title">
          <Brain />
          <div>
            <h2>任务记忆</h2>
            <p>默认每 32 次主模型调用后，由 Memory Agent 压缩工具输出；可在设置页调整。</p>
          </div>
        </div>
        <div className="memory-headline">
          <p>{memory.summary || "暂无记忆摘要。"}</p>
        </div>
      </section>
      {groups.map(([label, value]) => (
        <section className="panel memory-list-card" key={label}>
          <h3>{label}</h3>
          <ListBlock items={listify(value)} empty="暂无记录" />
        </section>
      ))}
    </div>
  );
}

function KnowledgeTab({
  mission,
  onError,
  onNotice
}: {
  mission: Mission;
  onError: (message: string) => void;
  onNotice: (message: string) => void;
}) {
  const [query, setQuery] = useState(mission.target || "");
  const [items, setItems] = useState<KnowledgeItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [crafts, setCrafts] = useState<ExperienceCraft[]>([]);
  const [selectedCraftId, setSelectedCraftId] = useState("");
  const [selectedCraft, setSelectedCraft] = useState<ExperienceCraftDetail | null>(null);
  const [craftLoading, setCraftLoading] = useState(false);
  const [reviewNotes, setReviewNotes] = useState("");

  useEffect(() => {
    let disposed = false;
    async function loadCrafts() {
      try {
        const response = await api.experienceCrafts();
        if (disposed) return;
        const nextCrafts = response.crafts || [];
        setCrafts(nextCrafts);
        setSelectedCraftId((current) => current || nextCrafts.find((craft) => craft.status === "pending_review")?.id || nextCrafts[0]?.id || "");
      } catch (err) {
        if (!disposed) onError(readError(err));
      }
    }
    loadCrafts();
    return () => {
      disposed = true;
    };
  }, [onError]);

  useEffect(() => {
    if (!selectedCraftId) {
      setSelectedCraft(null);
      return;
    }
    let disposed = false;
    async function loadCraft() {
      setCraftLoading(true);
      try {
        const response = await api.experienceCraft(selectedCraftId);
        if (!disposed) setSelectedCraft(response.craft);
      } catch (err) {
        if (!disposed) onError(readError(err));
      } finally {
        if (!disposed) setCraftLoading(false);
      }
    }
    loadCraft();
    return () => {
      disposed = true;
    };
  }, [selectedCraftId, onError]);

  async function refreshCrafts(nextSelectedId = selectedCraftId) {
    const response = await api.experienceCrafts();
    const nextCrafts = response.crafts || [];
    setCrafts(nextCrafts);
    setSelectedCraftId(nextSelectedId || nextCrafts[0]?.id || "");
    if (nextSelectedId) {
      const detail = await api.experienceCraft(nextSelectedId);
      setSelectedCraft(detail.craft);
    } else {
      setSelectedCraft(null);
    }
  }

  async function search(event?: React.FormEvent) {
    event?.preventDefault();
    if (!query.trim()) return;
    setLoading(true);
    onError("");
    try {
      const response = await api.knowledgeSearch(query, 10);
      setItems(response.items || []);
      if (!(response.items || []).length) onNotice("知识库没有找到相关条目。");
    } catch (err) {
      onError(readError(err));
    } finally {
      setLoading(false);
    }
  }

  async function reindex() {
    setLoading(true);
    try {
      await api.reindexKnowledge();
      onNotice("知识库重建完成。");
    } catch (err) {
      onError(readError(err));
    } finally {
      setLoading(false);
    }
  }

  async function reviewCraft(action: "approve" | "reject") {
    if (!selectedCraftId) return;
    setCraftLoading(true);
    try {
      if (action === "approve") {
        const response = await api.approveExperienceCraft(selectedCraftId, {
          reviewer: "human",
          notes: reviewNotes
        });
        onNotice(`Experience Craft 已批准入库：${response.distilled_path}`);
      } else {
        await api.rejectExperienceCraft(selectedCraftId, {
          reviewer: "human",
          notes: reviewNotes
        });
        onNotice("Experience Craft 已驳回，不会进入主 Agent 经验提示。");
      }
      setReviewNotes("");
      await refreshCrafts(selectedCraftId);
    } catch (err) {
      onError(readError(err));
    } finally {
      setCraftLoading(false);
    }
  }

  return (
    <div className="knowledge-workspace">
      <section className="panel">
        <div className="section-title">
          <MagnifyingGlass />
          <div>
            <h2>知识库检索</h2>
            <p>查询离线 RAG/FTS 索引，辅助判断漏洞路径。</p>
          </div>
        </div>
        <form className="search-bar" onSubmit={search}>
          <input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="thinkphp rce, file upload, redis unauth" />
          <button className="primary-button slim" type="submit" disabled={loading}>
            搜索
          </button>
          <button className="ghost-button" type="button" onClick={reindex} disabled={loading}>
            重建索引
          </button>
        </form>
        <div className="knowledge-results">
          {items.length ? (
            items.map((item) => (
              <article className="knowledge-card" key={`${item.source}-${item.id}`}>
                <span className="trace-type">{item.domain || item.source}</span>
                <strong>{item.title || item.path}</strong>
                <p>{stripSnippet(item.snippet || item.body || "")}</p>
                <small>{item.path}</small>
              </article>
            ))
          ) : (
            <EmptyState title="等待检索" body="输入关键词后，会显示知识库命中的路径和摘要。" />
          )}
        </div>
      </section>

      <section className="panel craft-review-panel">
        <div className="section-title">
          <ShieldCheck />
          <div>
            <h2>Experience Craft 复验</h2>
            <p>Agent 成功后只生成草稿；人工批准后才会进入可检索经验库。</p>
          </div>
        </div>
        <div className="craft-review-grid">
          <div className="craft-list">
            {crafts.length ? (
              crafts.map((craft) => (
                <button
                  type="button"
                  className={selectedCraftId === craft.id ? "craft-card active" : "craft-card"}
                  key={craft.id}
                  onClick={() => setSelectedCraftId(craft.id)}
                >
                  <span className={`status-badge ${craft.status === "approved" ? "ok" : craft.status === "rejected" ? "bad" : "warn"}`}>
                    {craft.status}
                  </span>
                  <strong>{craft.mission_name || craft.id}</strong>
                  <small>{craft.target || craft.path}</small>
                  <p>{stripSnippet(craft.snippet || "")}</p>
                </button>
              ))
            ) : (
              <EmptyState compact title="暂无草稿" body="任务拿到 Flag 后会自动生成待复验 craft。" />
            )}
          </div>
          <div className="craft-detail">
            {selectedCraft ? (
              <>
                <div className="craft-meta">
                  <RuntimeLine label="状态" value={selectedCraft.status} />
                  <RuntimeLine label="Mission" value={selectedCraft.source_mission_id || "unknown"} />
                  <RuntimeLine label="路径" value={selectedCraft.path} />
                  <RuntimeLine label="入库" value={selectedCraft.distilled_path || "未入库"} />
                </div>
                <pre className="craft-preview">{selectedCraft.content}</pre>
                <label className="review-notes">
                  复验备注
                  <textarea
                    value={reviewNotes}
                    onChange={(event) => setReviewNotes(event.target.value)}
                    rows={3}
                    placeholder="例如：已在干净沙箱复现 payload，确认漏洞类型与命令链。"
                  />
                </label>
                <div className="craft-actions">
                  <button
                    className="primary-button slim"
                    type="button"
                    onClick={() => void reviewCraft("approve")}
                    disabled={craftLoading || selectedCraft.status === "approved"}
                  >
                    批准入库
                  </button>
                  <button
                    className="danger-button"
                    type="button"
                    onClick={() => void reviewCraft("reject")}
                    disabled={craftLoading || selectedCraft.status === "approved"}
                  >
                    驳回
                  </button>
                </div>
              </>
            ) : (
              <EmptyState title={craftLoading ? "正在加载草稿" : "选择草稿"} body="左侧选择一个 craft 后，可以查看完整内容并复验。" />
            )}
          </div>
        </div>
      </section>
    </div>
  );
}

function SettingsPage() {
  const [config, setConfig] = useState<Config>({});
  const [bootstrap, setBootstrap] = useState<Bootstrap | null>(null);
  const [loading, setLoading] = useState(true);
  const [status, setStatus] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    let cancelled = false;
    async function load() {
      try {
        const [configResponse, bootstrapResponse] = await Promise.all([api.config(), api.bootstrap()]);
        if (!cancelled) setConfig(configResponse.config || {});
        if (!cancelled) setBootstrap(bootstrapResponse);
      } catch (err) {
        if (!cancelled) setError(readError(err));
      } finally {
        if (!cancelled) setLoading(false);
      }
    }
    load();
    return () => {
      cancelled = true;
    };
  }, []);

  function update(key: string, value: string | number | boolean) {
    setConfig((current) => ({ ...current, [key]: value }));
  }

  async function save() {
    setError("");
    setStatus("");
    try {
      const editableConfig = Object.fromEntries(
        configFields
          .map((field) => [field.key, config[field.key]] as const)
          .filter(([, value]) => value !== undefined)
      ) as Config;
      const response = await api.saveConfig(editableConfig);
      setConfig(response.config || {});
      if (response.errors && Object.keys(response.errors).length) {
        setError(Object.entries(response.errors).map(([key, value]) => `${key}: ${value}`).join("; "));
      } else {
        setStatus("配置已保存。");
      }
    } catch (err) {
      setError(readError(err));
    }
  }

  const sections = Array.from(new Set(configFields.map((field) => field.section)));
  const sectionId = (section: string) => `settings-${section.replace(/\s+/g, "-").toLowerCase()}`;
  const sectionCounts = Object.fromEntries(sections.map((section) => [section, configFields.filter((field) => field.section === section).length]));
  const settingsSummary = [
    { label: "主模型", value: String(config.effective_chat_model || config.llm_model || bootstrap?.model || "未加载") },
    { label: "LLM 模式", value: String(bootstrap?.llm_mode || "未加载") },
    { label: "Skill", value: `${String(bootstrap?.skills?.enabled ?? "-")}/${String(bootstrap?.skills?.total ?? "-")} enabled` }
  ];
  return (
    <div className="app-shell settings-shell">
      <Atmosphere />
      <Header bootstrap={bootstrap} active="settings" />
      <main className="settings-page">
        <section className="settings-hero">
          <div>
            <p className="kicker">CONFIG SURFACE</p>
            <h1>运行配置</h1>
            <p>保存后后端会热更新可变配置。API Key 返回值会被后端脱敏。</p>
          </div>
          <div className="settings-summary">
            {settingsSummary.map((item) => (
              <RuntimeLine key={item.label} label={item.label} value={item.value} />
            ))}
          </div>
        </section>
        {loading ? <SkeletonPanel title="正在加载配置" rows={6} /> : null}
        {status ? <InlineNotice tone="ok" message={status} onClose={() => setStatus("")} /> : null}
        {error ? <InlineNotice tone="bad" message={error} actionLabel="重新加载" onAction={() => window.location.reload()} onClose={() => setError("")} /> : null}
        <div className="settings-layout">
          <aside className="settings-index panel">
            <h2>配置分区</h2>
            <nav aria-label="配置分区">
              {sections.map((section) => (
                <a href={`#${sectionId(section)}`} key={section}>
                  <span>{section}</span>
                  <strong>{sectionCounts[section]}</strong>
                </a>
              ))}
            </nav>
          </aside>

          <div className="settings-grid">
            {sections.map((section) => (
              <section className="panel settings-card" id={sectionId(section)} key={section}>
                <div className="settings-card-head">
                  <h2>{section}</h2>
                  <span>{sectionCounts[section]} 项</span>
                </div>
                <div className="settings-fields">
                  {configFields
                    .filter((field) => field.section === section)
                    .map((field) => (
                      <ConfigField
                        key={field.key}
                        label={field.label}
                        type={field.type}
                        value={config[field.key]}
                        onChange={(value) => update(field.key, value)}
                      />
                    ))}
                </div>
              </section>
            ))}
          </div>
        </div>
        <div className="settings-savebar">
          <div>
            <strong>当前生效模型</strong>
            <span>{String(config.effective_chat_model || config.llm_model || "未加载")}</span>
          </div>
          <button className="primary-button" type="button" onClick={save}>
            <GearSix />
            保存配置
          </button>
        </div>
      </main>
    </div>
  );
}

function ConfigField({
  label,
  type,
  value,
  onChange
}: {
  label: string;
  type: "text" | "password" | "number" | "checkbox";
  value: unknown;
  onChange: (value: string | number | boolean) => void;
}) {
  if (type === "checkbox") {
    return (
      <label className="toggle-field">
        <span>{label}</span>
        <input type="checkbox" checked={Boolean(value)} onChange={(event) => onChange(event.target.checked)} />
      </label>
    );
  }
  return (
    <label className="config-field">
      {label}
      <input
        type={type}
        value={value === null || value === undefined ? "" : String(value)}
        onChange={(event) => onChange(type === "number" ? Number(event.target.value) : event.target.value)}
      />
    </label>
  );
}

function HumanCollaborationPanel({
  detail,
  onError,
  onNotice,
  onRefresh
}: {
  detail: MissionDetail;
  onError: (message: string) => void;
  onNotice: (message: string) => void;
  onRefresh: () => Promise<void>;
}) {
  const [content, setContent] = useState("");
  const [busy, setBusy] = useState(false);
  const enabled = detail.mission.human_collab_enabled;
  const canSend = enabled && isActiveMission(detail.mission, detail.thread_alive);

  async function toggle() {
    setBusy(true);
    try {
      await api.setCollaboration(detail.mission.id, !enabled);
      onNotice(!enabled ? "人工协作通道已开启。" : "人工协作通道已关闭。");
      await onRefresh();
    } catch (err) {
      onError(readError(err));
    } finally {
      setBusy(false);
    }
  }

  async function send(event: React.FormEvent) {
    event.preventDefault();
    if (!content.trim()) return;
    setBusy(true);
    try {
      await api.sendGuidance(detail.mission.id, content.trim());
      setContent("");
      onNotice("指导已提交，会在下一轮进入上下文。");
      await onRefresh();
    } catch (err) {
      onError(readError(err));
    } finally {
      setBusy(false);
    }
  }

  return (
    <section className="panel">
      <div className="section-title">
        <WarningCircle />
        <div>
          <h2>人工协作</h2>
          <p>{enabled ? "通道开启，可以提交下一步指导。" : "默认关闭，避免噪声干扰 agent。"}</p>
        </div>
      </div>
      <button type="button" className={enabled ? "toggle-pill on" : "toggle-pill"} onClick={toggle} disabled={busy}>
        {enabled ? "已开启" : "开启通道"}
      </button>
      <form className="guidance-form" onSubmit={send}>
        <textarea value={content} onChange={(event) => setContent(event.target.value)} placeholder="输入要注入给 agent 的短指导。" rows={4} />
        <button className="primary-button slim" type="submit" disabled={!canSend || busy || !content.trim()}>
          提交指导
        </button>
      </form>
      <ListBlock items={detail.human_guidance.map((item) => `${item.status}: ${item.content}`)} empty="暂无人工指导" />
    </section>
  );
}

function ExperimentEditor({
  missionId,
  experiment,
  onError,
  onNotice,
  onRefresh
}: {
  missionId: string;
  experiment: ExperimentRecord | null;
  onError: (message: string) => void;
  onNotice: (message: string) => void;
  onRefresh: () => Promise<void>;
}) {
  const [draft, setDraft] = useState({
    challenge_code: experiment?.challenge_code || "",
    difficulty: experiment?.difficulty || "",
    outcome: experiment?.outcome || "unknown",
    failure_reason: experiment?.failure_reason || "",
    key_parameters: experiment?.key_parameters || "",
    notes: experiment?.notes || ""
  });

  useEffect(() => {
    setDraft({
      challenge_code: experiment?.challenge_code || "",
      difficulty: experiment?.difficulty || "",
      outcome: experiment?.outcome || "unknown",
      failure_reason: experiment?.failure_reason || "",
      key_parameters: experiment?.key_parameters || "",
      notes: experiment?.notes || ""
    });
  }, [experiment?.mission_id, experiment?.updated_at]);

  async function save(event: React.FormEvent) {
    event.preventDefault();
    try {
      await api.updateExperiment(missionId, draft as Partial<ExperimentRecord>);
      onNotice("实验记录已保存。");
      await onRefresh();
    } catch (err) {
      onError(readError(err));
    }
  }

  function change(key: keyof typeof draft, value: string) {
    setDraft((current) => ({ ...current, [key]: value }));
  }

  return (
    <details className="panel experiment-collapsible archive-panel">
      <summary className="section-title">
        <Graph />
        <div>
          <h2>实验归档</h2>
          <p>记录难度、结果、失败边界和关键参数。</p>
        </div>
      </summary>
      <form className="experiment-form" onSubmit={save}>
        <div className="form-grid">
          <label>
            Challenge Code
            <input value={draft.challenge_code} onChange={(event) => change("challenge_code", event.target.value)} />
          </label>
          <label>
            Difficulty
            <input value={draft.difficulty} onChange={(event) => change("difficulty", event.target.value)} />
          </label>
          <label>
            Outcome
            <select value={draft.outcome} onChange={(event) => change("outcome", event.target.value)}>
              <option value="unknown">unknown</option>
              <option value="success">success</option>
              <option value="failed">failed</option>
              <option value="timeout">timeout</option>
              <option value="blocked">blocked</option>
            </select>
          </label>
          <label>
            Failure Reason
            <input value={draft.failure_reason} onChange={(event) => change("failure_reason", event.target.value)} />
          </label>
        </div>
        <label>
          Key Parameters
          <textarea value={draft.key_parameters} onChange={(event) => change("key_parameters", event.target.value)} rows={3} />
        </label>
        <label>
          Notes
          <textarea value={draft.notes} onChange={(event) => change("notes", event.target.value)} rows={4} />
        </label>
        <button className="ghost-button" type="submit">
          保存归档
        </button>
      </form>
    </details>
  );
}

function EventStream({ events }: { events: Event[] }) {
  if (!events.length) return <EmptyState title="暂无事件" body="运行后会自动填充。" />;
  return (
    <div className="event-stream">
      {events.map((event) => (
        <EventCard event={event} key={event.id} />
      ))}
    </div>
  );
}

function ObserverMessageCard({ message }: { message: ObserverMessage }) {
  const tone = observerMessageTone(message);
  const metadata = asRecord(message.metadata);
  const decision = observerDecisionFromMetadata(metadata, message.content);
  const observation = observerObservationFromMessage(message);
  const phase = toText(metadata.phase || observation.phase || "");
  return (
    <article className={`message-card observer-message-card ${tone}`}>
      <div className="observer-message-head">
        <span className="trace-type">{message.type}</span>
        <div>
          <strong>{message.title || "Observer message"}</strong>
          <small>
            R{message.round_no} · {phase ? `${phase} · ` : ""}{formatTime(message.created_at)}
          </small>
        </div>
      </div>
      {message.type === "observation" ? (
        <ObserverObservationPanel observation={observation} raw={message.content} />
      ) : message.type === "decision" ? (
        <ObserverDecisionPanel decision={decision} raw={message.content} metadata={metadata} />
      ) : (
        <ObserverToolPanel message={message} />
      )}
    </article>
  );
}

function ObserverEventBody({ event }: { event: Event }) {
  const metadata = asRecord(event.metadata);
  const decision = observerDecisionFromMetadata(metadata, event.content);
  const patch = asRecord(metadata.observer_memory_patch);
  if (Object.keys(decision).length) {
    return (
      <div className="observer-event-body">
        <ObserverDecisionPanel decision={decision} raw={event.content} metadata={metadata} compactView />
      </div>
    );
  }
  if (Object.keys(patch).length) {
    return (
      <div className="observer-event-body">
        <ObserverMemoryPatch patch={patch} />
        <ObserverRawDetails raw={event.content || safeJson(metadata)} />
      </div>
    );
  }
  return (
    <div className="observer-event-body">
      <p className="observer-fallback-text">{event.content || compact(metadata, 360)}</p>
    </div>
  );
}

function ObserverObservationPanel({ observation, raw }: { observation: ObserverObservationView; raw: string }) {
  const mission = asRecord(observation.mission);
  const ruleDecision = asRecord(observation.rule_observation);
  const memoryBefore = observation.memory_before;
  const memoryAfter = observation.memory_after;
  const recentCalls = observerToolCallItems(observation.recent_tool_calls);
  const roundCalls = observerToolCallItems(observation.round_tool_calls);
  const calls = roundCalls.length ? roundCalls : recentCalls;
  const target = toText(mission.target || "");
  const goal = toText(mission.goal || "");
  return (
    <div className="observer-observation">
      <div className="observer-focus-strip">
        <ObserverMiniStat label="阶段" value={toText(observation.phase || "round_review")} />
        <ObserverMiniStat label="LLM 调用" value={toText(observation.llm_call_count ?? "0")} />
        <ObserverMiniStat label="停滞轮次" value={toText(observation.stall_rounds ?? "0")} />
        <ObserverMiniStat label="规则判定" value={observerVerdictLabel(ruleDecision.verdict)} tone={observerVerdictClass(ruleDecision.verdict)} />
      </div>
      <div className="observer-summary-grid">
        <ObserverInfoBlock label="目标" value={target || "未记录"} />
        <ObserverInfoBlock label="任务" value={goal || "未记录"} />
        <ObserverInfoBlock label="审核前记忆" value={observerMemorySummary(memoryBefore)} />
        <ObserverInfoBlock label="审核后记忆" value={observerMemorySummary(memoryAfter)} />
      </div>
      {calls.length ? <ObserverToolCallList calls={calls} /> : null}
      {asStringList(ruleDecision.evidence).length ? (
        <ObserverList title="规则证据" items={asStringList(ruleDecision.evidence)} />
      ) : null}
      <ObserverRawDetails raw={raw} />
    </div>
  );
}

function ObserverDecisionPanel({
  decision,
  raw,
  metadata,
  compactView
}: {
  decision: ObserverDecisionView;
  raw: string;
  metadata: Record<string, unknown>;
  compactView?: boolean;
}) {
  const verdict = decision.verdict || "OK";
  const evidence = asStringList(decision.evidence);
  const memoryPatch = observerMemoryPatchItems(decision.memory_patch);
  const experienceRefs = asStringList(decision.experience_refs || metadata.experience_refs);
  const skillRefs = asStringList(metadata.skill_refs);
  const detailItems = observerDecisionItems(decision);
  return (
    <div className={compactView ? "observer-decision compact" : "observer-decision"}>
      <div className="observer-verdict-row">
        <span className={`observer-verdict ${observerVerdictClass(verdict)}`}>{observerVerdictLabel(verdict)}</span>
        <p>{observerPrimaryText(decision)}</p>
      </div>
      {detailItems.length ? (
        <div className="observer-detail-grid">
          {detailItems.map(([label, value]) => (
            <ObserverInfoBlock label={label} value={toText(value)} key={label} />
          ))}
        </div>
      ) : null}
      {evidence.length ? <ObserverList title="关键证据" items={evidence} /> : null}
      {memoryPatch.length ? <ObserverMemoryPatch patch={decision.memory_patch} /> : null}
      {experienceRefs.length || skillRefs.length ? (
        <div className="observer-ref-row">
          {experienceRefs.slice(0, 6).map((item) => (
            <code key={`exp-${item}`}>{item}</code>
          ))}
          {skillRefs.slice(0, 4).map((item) => (
            <code key={`skill-${item}`}>{item}</code>
          ))}
        </div>
      ) : null}
      <ObserverRawDetails raw={raw || safeJson(metadata)} />
    </div>
  );
}

function ObserverToolPanel({ message }: { message: ObserverMessage }) {
  const metadata = asRecord(message.metadata);
  const args = asRecord(metadata.args);
  const result = metadata.result;
  const tool = toText(metadata.tool || message.type);
  return (
    <div className="observer-tool-panel">
      <div className="observer-focus-strip">
        <ObserverMiniStat label="内部动作" value={tool || "observer_think"} />
        <ObserverMiniStat label="Step" value={toText(metadata.step ?? "-")} />
      </div>
      {Object.keys(args).length ? <ObserverInfoBlock label="参数" value={safeJson(args)} mono /> : null}
      {result ? <ObserverInfoBlock label="结果" value={compact(result, 900)} /> : <p className="observer-fallback-text">{message.content}</p>}
      <ObserverRawDetails raw={message.content || safeJson(metadata)} />
    </div>
  );
}

function ObserverToolCallList({ calls }: { calls: Record<string, unknown>[] }) {
  return (
    <div className="observer-call-list">
      <span>本轮工具轨迹</span>
      {calls.slice(0, 8).map((call, index) => {
        const tool = toText(call.tool || "tool");
        const args = toText(call.args_summary || call.args_full || "");
        const result = toText(call.result_summary || call.result_observer || "");
        const exitCode = call.exit_code === undefined || call.exit_code === null ? "" : `exit ${call.exit_code}`;
        return (
          <article className="observer-call" key={`${tool}-${index}`}>
            <div>
              <strong>{tool}</strong>
              {exitCode ? <em>{exitCode}</em> : null}
            </div>
            {args ? <code>{compact(args, 180)}</code> : null}
            {result ? <p>{compact(result, 260)}</p> : null}
          </article>
        );
      })}
    </div>
  );
}

function ObserverMemoryPatch({ patch }: { patch: unknown }) {
  const groups = observerMemoryPatchItems(patch);
  if (!groups.length) return null;
  return (
    <div className="observer-memory-patch">
      <span>记忆补丁</span>
      {groups.map((group) => (
        <section key={group.key}>
          <strong>{group.key}</strong>
          <ul>
            {group.items.slice(0, 6).map((item, index) => (
              <li key={`${group.key}-${index}`}>{item}</li>
            ))}
          </ul>
        </section>
      ))}
    </div>
  );
}

function ObserverInfoBlock({ label, value, mono }: { label: string; value: string; mono?: boolean }) {
  return (
    <article className={mono ? "observer-info mono" : "observer-info"}>
      <span>{label}</span>
      <p>{value}</p>
    </article>
  );
}

function ObserverMiniStat({ label, value, tone }: { label: string; value: string; tone?: string }) {
  return (
    <article className={tone ? `observer-mini-stat ${tone}` : "observer-mini-stat"}>
      <span>{label}</span>
      <strong>{value}</strong>
    </article>
  );
}

function ObserverList({ title, items }: { title: string; items: string[] }) {
  return (
    <div className="observer-list-block">
      <span>{title}</span>
      <ul>
        {items.slice(0, 8).map((item, index) => (
          <li key={`${title}-${index}`}>{item}</li>
        ))}
      </ul>
    </div>
  );
}

function ObserverRawDetails({ raw }: { raw: string }) {
  if (!raw.trim()) return null;
  return (
    <details className="observer-raw">
      <summary>原始数据</summary>
      <pre>{raw}</pre>
    </details>
  );
}

function EventCard({ event }: { event: Event }) {
  const isObserver = event.type === "observer_agent";
  return (
    <details className={`trace-card ${eventTone(event.type)}`} open={event.type === "flag" || event.type === "error"}>
      <summary>
        <span className="trace-type">{eventLabel(event.type)}</span>
        <strong>{event.title || compact(event.command || event.content, 120)}</strong>
        <small>
          R{event.round_no} · {formatTime(event.ended_at || event.started_at)}
        </small>
      </summary>
      {event.command ? <code className="command-line">{event.command}</code> : null}
      {isObserver ? <ObserverEventBody event={event} /> : <pre>{event.content || safeJson(event.metadata)}</pre>}
      {event.exit_code ? <span className="exit-code">exit {event.exit_code}</span> : null}
    </details>
  );
}

function BriefItem({ label, value, mono }: { label: string; value: string; mono?: boolean }) {
  return (
    <article className={mono ? "brief-item mono" : "brief-item"}>
      <span>{label}</span>
      <p>{value}</p>
    </article>
  );
}

function MetricTile({ label, value }: { label: string; value: string }) {
  return (
    <article className="metric-tile">
      <span>{label}</span>
      <strong>{value}</strong>
    </article>
  );
}

function ListBlock({ items, empty }: { items: string[]; empty: string }) {
  if (!items.length) return <p className="muted">{empty}</p>;
  return (
    <ul className="smart-list">
      {items.slice(0, 12).map((item, index) => (
        <li key={`${item}-${index}`}>{item}</li>
      ))}
    </ul>
  );
}

function RuntimeLine({ label, value }: { label: string; value: string }) {
  return (
    <div className="runtime-line">
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}

function EmptyState({
  title,
  body,
  large,
  compact,
  action
}: {
  title: string;
  body: string;
  large?: boolean;
  compact?: boolean;
  action?: { label: string; onClick: () => void };
}) {
  return (
    <div className={large ? "empty-state large" : compact ? "empty-state compact" : "empty-state"}>
      <TerminalWindow />
      <strong>{title}</strong>
      <p>{body}</p>
      {action ? (
        <button type="button" className="ghost-button" onClick={action.onClick}>
          {action.label}
        </button>
      ) : null}
    </div>
  );
}

function InlineNotice({
  tone,
  message,
  actionLabel,
  onAction,
  onClose
}: {
  tone: "ok" | "bad";
  message: string;
  actionLabel?: string;
  onAction?: () => void | Promise<void>;
  onClose: () => void;
}) {
  return (
    <div className={`inline-notice ${tone}`} role={tone === "bad" ? "alert" : "status"} aria-live={tone === "bad" ? "assertive" : "polite"}>
      <span>{tone === "ok" ? <CheckCircle /> : <WarningCircle />}</span>
      <p>{message}</p>
      {actionLabel && onAction ? (
        <button type="button" onClick={() => void onAction()}>
          {actionLabel}
        </button>
      ) : null}
      <button type="button" onClick={onClose}>
        关闭
      </button>
    </div>
  );
}

function SkeletonPanel({ title = "正在加载", rows = 3 }: { title?: string; rows?: number }) {
  return (
    <section className="panel skeleton-panel">
      <strong>{title}</strong>
      {Array.from({ length: rows }).map((_, index) => (
        <span key={index} />
      ))}
    </section>
  );
}

function readError(err: unknown): string {
  if (err instanceof ApiError) return `${err.message} (HTTP ${err.status})`;
  if (err instanceof Error) return err.message;
  return String(err);
}

function stripSnippet(value: string): string {
  return value.replaceAll("[", "").replaceAll("]", "").replace(/\s+/g, " ").trim();
}

createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
