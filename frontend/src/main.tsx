import React, { useEffect, useMemo, useRef, useState, useTransition } from "react";
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
  { id: "evidence", label: "证据" },
  { id: "knowledge", label: "知识库" }
];

const tabButtonId = (tab: AppTab) => `mission-tab-${tab}`;
const tabPanelId = (tab: AppTab) => `mission-panel-${tab}`;

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
  { key: "observer_review_interval", label: "Observer 审核间隔", type: "number", section: "Observer" },
  { key: "observer_reasoning_effort", label: "Observer 推理强度", type: "text", section: "Observer" },
  { key: "initial_rounds", label: "默认轮数", type: "number", section: "Agent 参数" },
  { key: "initial_commands", label: "每轮命令数", type: "number", section: "Agent 参数" },
  { key: "command_timeout_sec", label: "命令超时秒数", type: "number", section: "Agent 参数" },
  { key: "stdout_limit", label: "输出截断长度", type: "number", section: "Agent 参数" },
  { key: "knowledge_top_k", label: "知识库检索数", type: "number", section: "Agent 参数" },
  { key: "skills_dir", label: "Skills 目录", type: "text", section: "Agent 参数" },
  { key: "skills_auto_use", label: "自动启用 Skill", type: "checkbox", section: "Agent 参数" }
] as const;

function App() {
  const isSettings = window.location.pathname.endsWith("/settings.html");
  return isSettings ? <SettingsPage /> : <MissionControl />;
}

function MissionControl() {
  const [bootstrap, setBootstrap] = useState<Bootstrap | null>(null);
  const [agentSlots, setAgentSlots] = useState<AgentSlot[]>([]);
  const [missions, setMissions] = useState<Mission[]>([]);
  const [experiments, setExperiments] = useState<ExperimentRecord[]>([]);
  const [skills, setSkills] = useState<Skill[]>([]);
  const [selectedId, setSelectedId] = useState<string>("");
  const [detail, setDetail] = useState<MissionDetail | null>(null);
  const [activeTab, setActiveTab] = useState<AppTab>("overview");
  const [loading, setLoading] = useState(true);
  const [detailLoading, setDetailLoading] = useState(false);
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
        setSelectedId((current) => current || missionData.missions?.[0]?.id || "");
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
          setSelectedId((current) => current || missionData.missions?.[0]?.id || "");
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

  useEffect(() => {
    if (!selectedId) {
      setDetail(null);
      return;
    }
    let disposed = false;
    async function loadDetail(showLoading: boolean) {
      if (showLoading) setDetailLoading(true);
      try {
        const data = await api.missionDetail(selectedId);
        if (!disposed) setDetail(data);
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
  }, [selectedId]);

  const selectedMission = useMemo(
    () => missions.find((mission) => mission.id === selectedId) || detail?.mission || null,
    [missions, selectedId, detail]
  );
  const runningCount = missions.filter((mission) => isActiveMission(mission)).length;
  const activeAgentCount = agentSlots.filter((slot) => slot.status === "running").length;
  const flagCount = missions.reduce((sum, mission) => sum + (mission.captured_flag_count || 0), 0);

  async function refreshAll() {
    const [missionData, experimentData] = await Promise.all([api.missions(), api.experiments()]);
    setMissions(missionData.missions || []);
    setAgentSlots(missionData.agent_slots || []);
    setExperiments(experimentData.records || []);
    if (selectedId) setDetail(await api.missionDetail(selectedId));
  }

  async function handleCreated(id: string) {
    setSelectedId(id);
    setNotice("任务已创建，正在进入队列。");
    await refreshAll();
  }

  async function missionAction(action: "stop" | "resume" | "delete") {
    if (!selectedMission) return;
    setError("");
    try {
      if (action === "stop") await api.stopMission(selectedMission.id);
      if (action === "resume") await api.resumeMission(selectedMission.id);
      if (action === "delete") {
        const ok = window.confirm(`删除任务 ${selectedMission.name}？该操作不会停止运行中的任务。`);
        if (!ok) return;
        await api.deleteMission(selectedMission.id);
        setSelectedId("");
        setDetail(null);
      }
      setNotice(action === "stop" ? "停止请求已发送。" : action === "resume" ? "任务已请求继续。" : "任务记录已删除。");
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

        <section className="control-grid">
          <aside className={missions.length ? "left-rail" : "left-rail empty-queue"}>
            <MissionLaunch
              defaults={bootstrap?.defaults}
              skills={skills}
              hasMissions={missions.length > 0}
              onCreated={handleCreated}
              onError={setError}
            />
            <MissionList missions={missions} selectedId={selectedId} onSelect={setSelectedId} />
          </aside>

          <section className="workbench">
            <SystemBar bootstrap={bootstrap} skills={skills} experiments={experiments} agentSlots={agentSlots} />

            <MissionDetailHeader
              mission={selectedMission}
              detail={detail}
              detailLoading={detailLoading}
              onStop={() => missionAction("stop")}
              onResume={() => missionAction("resume")}
              onDelete={() => missionAction("delete")}
            />

            <FunctionMap detail={detail} onOpenTab={setActiveTab} />

            <div className="pane-region">
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

              <MissionPane
                tab={activeTab}
                detail={detail}
                experiments={experiments}
                onError={setError}
                onNotice={setNotice}
                onRefresh={refreshAll}
              />
            </div>
          </section>
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
    const form = new FormData(event.currentTarget);
    const payload = {
      name: String(form.get("name") || "Pentest"),
      target: String(form.get("target") || "").trim(),
      goal: String(form.get("goal") || "").trim(),
      max_rounds: Number(form.get("max_rounds") || defaults?.max_rounds || 8),
      max_commands: Number(form.get("max_commands") || defaults?.max_commands || 32),
      command_timeout_sec: Number(form.get("command_timeout_sec") || defaults?.command_timeout_sec || 60),
      expected_flags: Number(form.get("expected_flags") || 1),
      skills: selectedSkills
    };
    try {
      const response = await api.createMission(payload);
      event.currentTarget.reset();
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
            <input name="max_rounds" type="number" min={1} max={200} defaultValue={defaults?.max_rounds || 8} />
          </label>
          <label>
            每轮命令
            <input name="max_commands" type="number" min={1} max={500} defaultValue={defaults?.max_commands || 32} />
          </label>
          <label>
            超时秒数
            <input
              name="command_timeout_sec"
              type="number"
              min={5}
              max={600}
              defaultValue={defaults?.command_timeout_sec || 60}
            />
          </label>
          <label>
            Flag 数量
            <input name="expected_flags" type="number" min={1} max={50} defaultValue={1} />
          </label>
        </div>
        {skills.length ? (
          <div className="skill-picker" aria-label="选择技能">
            {skills.slice(0, 8).map((skill) => (
              <button
                key={skill.id}
                type="button"
                className={selectedSkills.includes(skill.id) ? "chip selected" : "chip"}
                onClick={() => toggleSkill(skill.id)}
                title={skill.description}
              >
                {skill.name || skill.id}
              </button>
            ))}
          </div>
        ) : null}
        <button className="primary-button" type="submit" disabled={submitting}>
          <Lightning weight="fill" />
          {submitting ? "创建中" : "启动任务"}
        </button>
      </form>
    </details>
  );
}

function MissionList({
  missions,
  selectedId,
  onSelect
}: {
  missions: Mission[];
  selectedId: string;
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
              className={mission.id === selectedId ? "mission-card active" : "mission-card"}
              aria-pressed={mission.id === selectedId}
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
          <p>页面会自动轮询后端，将命令、Observer 审核、记忆和证据整理到同一条时间线。</p>
        </div>
      </section>
    );
  }
  const mainRounds = detail?.rounds.filter((round) => round.worker_role === "main").length || 0;
  const progress = mission.status === "done" ? 100 : percentage(mainRounds, mission.max_rounds);
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
            R{String(mainRounds).padStart(2, "0")} / {mission.max_rounds}
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

function FunctionMap({
  detail,
  onOpenTab
}: {
  detail: MissionDetail | null;
  onOpenTab: (tab: AppTab) => void;
}) {
  if (!detail) {
    return (
      <section className="function-map empty">
        <div className="function-map-head">
          <div>
            <h2>一屏功能总览</h2>
            <p>创建或选择任务后，这里会集中显示审核、记忆、证据、知识库和协作入口。</p>
          </div>
        </div>
        <div className="function-grid placeholder-grid">
          {tabs.slice(2).map((tab) => (
            <button key={tab.id} type="button" className="function-card muted-card" disabled>
              <span className="function-label">{tab.label}</span>
              <strong>等待任务数据</strong>
            </button>
          ))}
        </div>
      </section>
    );
  }

  const evidenceCount = detail.events.filter((event) =>
    ["flag", "command", "knowledge", "error", "sandbox"].includes(event.type)
  ).length;
  const observer = detail.observer;
  const latest = observer.latest_decision || {};
  const modules: {
    label: string;
    title: string;
    body: string;
    meta: string;
    icon: React.ReactNode;
    tab: AppTab;
    tone?: string;
  }[] = [
    {
      label: "Observer",
      title: observer.status || "idle",
      body: compact(toText(latest.rationale || latest.guidance || "等待被动审核"), 92),
      meta: `${observer.stats?.decisions || 0} 次审核`,
      icon: <Circuitry />,
      tab: "observer",
      tone: observer.stats?.interrupts ? "warn" : "blue"
    },
    {
      label: "Memory",
      title: detail.memory.highest_value_lead || detail.memory.primary_hypothesis || "暂无主线",
      body: compact(detail.memory.next_one_command || detail.memory.next_verification || detail.memory.summary || "等待下一轮压缩", 92),
      meta: formatTime(detail.memory.updated_at),
      icon: <Brain />,
      tab: "memory",
      tone: "blue"
    },
    {
      label: "Evidence",
      title: `${evidenceCount} 条证据`,
      body: detail.captured_flags.length ? compact(detail.captured_flags[0], 92) : "命令输出、知识命中、错误和 Flag 会进入证据仓。",
      meta: `${detail.captured_flag_count} / ${detail.mission.expected_flags || 1} flag`,
      icon: <Database />,
      tab: "evidence",
      tone: detail.captured_flag_count ? "ok" : "blue"
    },
    {
      label: "Knowledge",
      title: "RAG / FTS 检索",
      body: `默认用目标 ${compact(detail.mission.target || "关键词", 64)} 发起离线知识库查询。`,
      meta: "可搜索并重建索引",
      icon: <MagnifyingGlass />,
      tab: "knowledge",
      tone: "blue"
    }
  ];

  return (
    <section className="function-map" aria-label="一屏功能总览">
      <div className="function-map-head">
        <div>
          <h2>一屏功能总览</h2>
          <p>核心能力全部收在当前任务下，深看再切换下方详情。</p>
        </div>
        <span>{detail.thread_alive ? "worker online" : "worker idle"}</span>
      </div>
      <div className="function-grid">
        {modules.map((item) => (
          <button
            key={item.label}
            type="button"
            className={`function-card ${item.tone || "blue"}`}
            aria-label={`打开${item.label}视图，${item.title}，${item.meta}`}
            onClick={() => onOpenTab(item.tab)}
          >
            <span className="function-icon">{item.icon}</span>
            <span className="function-label">{item.label}</span>
            <strong>{item.title}</strong>
            <p>{item.body}</p>
            <small>{item.meta}</small>
          </button>
        ))}
      </div>
    </section>
  );
}

function SystemBar({
  bootstrap,
  skills,
  experiments,
  agentSlots
}: {
  bootstrap: Bootstrap | null;
  skills: Skill[];
  experiments: ExperimentRecord[];
  agentSlots: AgentSlot[];
}) {
  const knowledgeStatus = bootstrap?.knowledge?.rag?.available
    ? `${bootstrap.knowledge.rag.total_chunks || 0} chunks`
    : bootstrap?.knowledge?.status || bootstrap?.knowledge?.search_backend || "未加载";
  const loadedEnabledSkills = skills.filter((skill) => skill.enabled).length;
  const enabledSkills = Math.max(Number(bootstrap?.skills?.enabled || 0), loadedEnabledSkills);
  const totalSkills = Math.max(Number(bootstrap?.skills?.total || 0), skills.length);
  const success = experiments.filter((item) => item.outcome === "success").length;
  const slots = agentSlots.length ? agentSlots : bootstrap?.agent_slots || [];
  return (
    <section className="system-bar" aria-label="运行环境摘要">
      <div className="agent-fleet">
        {slots.map((slot) => (
          <AgentSlotCard key={slot.agent_id || slot.slot} slot={slot} />
        ))}
      </div>
      <RuntimeLine label="工作目录" value={bootstrap?.sandbox_workdir || "未加载"} />
      <RuntimeLine label="知识库" value={knowledgeStatus} />
      <RuntimeLine label="Skills" value={`${enabledSkills}/${totalSkills} enabled`} />
      <RuntimeLine label="归档成功" value={`${success}/${experiments.length}`} />
    </section>
  );
}

function AgentSlotCard({ slot }: { slot: AgentSlot }) {
  const running = slot.status === "running";
  const reason =
    slot.status_reason === "flag_captured"
      ? `空闲 · ${slot.captured_flag_count} flag`
      : slot.status_reason === "not_started"
        ? "空闲 · 未启动"
        : running
          ? "运行中"
          : "空闲";
  const title = slot.mission_name || slot.container;
  const meta = slot.target || slot.container;
  return (
    <article className={running ? "agent-slot running" : "agent-slot idle"}>
      <span className="agent-index">A{slot.slot}</span>
      <div>
        <strong>{reason}</strong>
        <small title={title}>{title}</small>
        <em title={meta}>{meta}</em>
      </div>
    </article>
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
        body="选择左侧任务，或展开发起任务表单创建新目标。这里会显示总览、时间线、Observer、记忆、证据和知识库。"
        large
      />
    );
  } else if (tab === "overview") {
    content = <OverviewTab detail={detail} experiments={experiments} onError={onError} onNotice={onNotice} onRefresh={onRefresh} />;
  } else if (tab === "timeline") {
    content = <TimelineTab detail={detail} />;
  } else if (tab === "observer") {
    content = <ObserverTab detail={detail} />;
  } else if (tab === "memory") {
    content = <MemoryTab detail={detail} />;
  } else if (tab === "evidence") {
    content = <EvidenceTab detail={detail} />;
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
            <BriefItem label="最高价值线索" value={memory.highest_value_lead || "暂无"} />
            <BriefItem label="下一条命令" value={memory.next_one_command || "等待下一轮规划"} mono />
            <BriefItem label="阻塞原因" value={memory.blocked_reason || mission.error_message || "未阻塞"} />
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

function TimelineTab({ detail }: { detail: MissionDetail }) {
  const groups = groupFlow(detail.rounds, detail.events);
  return (
    <section className="panel flow-panel">
      <div className="section-title">
        <Pulse />
        <div>
          <h2>执行时间线</h2>
          <p>按 round 聚合模型决策、命令输出和系统事件。</p>
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
            <p>Observer 不再是可调用工具，而是按配置间隔被动审核主模型轨迹。</p>
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
          <BriefItem label="Evidence" value={toText(latest.evidence || "暂无证据")} />
          <BriefItem label="Guidance" value={toText(latest.guidance || "无纠偏")} />
          <BriefItem label="Next" value={toText(latest.next_verification || "无需额外验证")} />
          <BriefItem label="Required Evidence" value={toText(latest.required_evidence || "无")} />
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
              <article className="message-card" key={message.id}>
                <div>
                  <span className="trace-type">
                    {message.type}
                    {typeof message.metadata?.decision === "object" && message.metadata.decision
                      ? ` · ${toText((message.metadata.decision as Record<string, unknown>).verdict || "")}`
                      : ""}
                  </span>
                  <strong>{message.title || "observer message"}</strong>
                </div>
                <p>{message.content || compact(message.metadata, 260)}</p>
                <small>
                  R{message.round_no} · {formatTime(message.created_at)}
                </small>
              </article>
            ))}
          </div>
        ) : (
          <EmptyState title="Observer 尚未介入" body="达到审核间隔或出现关键风险时，这里会出现被动审核结果。" />
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
    ["Next Focus", memory.next_focus],
    ["Topology", memory.topology]
  ] as const;
  return (
    <div className="tab-grid">
      <section className="panel span-2">
        <div className="section-title">
          <Brain />
          <div>
            <h2>任务记忆</h2>
            <p>更新时间：{formatTime(memory.updated_at)}</p>
          </div>
        </div>
        <div className="memory-headline">
          <p>{memory.summary || "暂无记忆摘要。"}</p>
        </div>
        <div className="brief-grid">
          <BriefItem label="当前假设" value={memory.primary_hypothesis || "暂无"} />
          <BriefItem label="下一步验证" value={memory.next_verification || "暂无"} />
          <BriefItem label="失败边界" value={memory.failure_boundary || "暂无"} />
          <BriefItem label="需要证据" value={memory.required_next_evidence || "暂无"} />
        </div>
      </section>
      {groups.map(([label, value]) => (
        <section className="panel memory-list-card" key={label}>
          <h3>{label}</h3>
          <ListBlock items={listify(value)} empty="暂无记录" />
        </section>
      ))}
      <section className="panel span-2">
        <h3>Nodes</h3>
        <pre className="json-block">{safeJson(memory.nodes)}</pre>
      </section>
    </div>
  );
}

function EvidenceTab({ detail }: { detail: MissionDetail }) {
  const evidence = detail.events.filter((event) =>
    ["flag", "command", "knowledge", "error", "sandbox"].includes(event.type)
  );
  return (
    <section className="panel collaboration-panel">
      <div className="section-title">
        <Database />
        <div>
          <h2>证据仓</h2>
          <p>聚合命令输出、知识库命中、错误和 Flag。</p>
        </div>
      </div>
      {evidence.length ? <EventStream events={evidence.slice().reverse()} /> : <EmptyState title="暂无证据" body="关键输出会在任务运行后自动进入这里。" large />}
    </section>
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
      const response = await api.saveConfig(config);
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
    { label: "Observer 间隔", value: `${String(config.observer_review_interval || "未加载")} 轮` },
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

function EventCard({ event }: { event: Event }) {
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
      <pre>{event.content || safeJson(event.metadata)}</pre>
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
