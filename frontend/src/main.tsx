import React, { useEffect, useMemo, useState, useTransition } from "react";
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
  Skull,
  TerminalWindow,
  Trash,
  WarningCircle
} from "@phosphor-icons/react";
import { api, ApiError } from "./api";
import type {
  AppTab,
  Bootstrap,
  Config,
  Event,
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
  const flagCount = missions.reduce((sum, mission) => sum + (mission.captured_flag_count || 0), 0);

  async function refreshAll() {
    const [missionData, experimentData] = await Promise.all([api.missions(), api.experiments()]);
    setMissions(missionData.missions || []);
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

  return (
    <div className="app-shell">
      <Atmosphere />
      <Header bootstrap={bootstrap} active="missions" />
      <main className="control-grid">
        <aside className="left-rail">
          <MissionLaunch defaults={bootstrap?.defaults} skills={skills} onCreated={handleCreated} onError={setError} />
          <MissionList missions={missions} selectedId={selectedId} onSelect={setSelectedId} />
        </aside>

        <section className="workbench">
          <DashboardStrip
            loading={loading || isPending}
            model={bootstrap?.model}
            runningCount={runningCount}
            flagCount={flagCount}
            missionCount={missions.length}
            knowledgeDocs={bootstrap?.knowledge?.total_docs || bootstrap?.knowledge?.total_chunks || 0}
          />

          {notice ? <InlineNotice tone="ok" message={notice} onClose={() => setNotice("")} /> : null}
          {error ? <InlineNotice tone="bad" message={error} onClose={() => setError("")} /> : null}

          <MissionDetailHeader
            mission={selectedMission}
            detail={detail}
            detailLoading={detailLoading}
            onStop={() => missionAction("stop")}
            onResume={() => missionAction("resume")}
            onDelete={() => missionAction("delete")}
          />

          <div className="tabs" role="tablist" aria-label="任务视图">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                type="button"
                className={activeTab === tab.id ? "tab active" : "tab"}
                onClick={() => setActiveTab(tab.id)}
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
        </section>

        <aside className="right-rail">
          <RuntimeCard bootstrap={bootstrap} skills={skills} />
          <ExperimentPulse experiments={experiments} />
          <SkillDeck skills={skills} />
        </aside>
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
  onCreated,
  onError
}: {
  defaults?: Bootstrap["defaults"];
  skills: Skill[];
  onCreated: (id: string) => Promise<void>;
  onError: (message: string) => void;
}) {
  const [submitting, setSubmitting] = useState(false);
  const [selectedSkills, setSelectedSkills] = useState<string[]>([]);

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
    <section className="panel launch-panel">
      <div className="panel-heading">
        <span className="panel-icon">
          <Plus />
        </span>
        <div>
          <h2>发起任务</h2>
          <p>定义目标、范围和终止条件。</p>
        </div>
      </div>
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
          <textarea name="goal" rows={4} placeholder="例如：找到并提交所有 flag，记录可复现路径。" required />
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
    </section>
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
          <EmptyState title="暂无任务" body="左上角创建一个目标后，这里会显示运行状态和最近更新。" />
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
        <div className="progress-ring" style={{ "--progress": `${progress}%` } as React.CSSProperties}>
          <span>{progress}%</span>
        </div>
        <div className="command-copy">
          <span className={`status-badge ${statusTone(mission.status)}`}>{mission.status}</span>
          <strong>
            R{String(mainRounds).padStart(2, "0")} / {mission.max_rounds}
          </strong>
          <small>{detail?.thread_alive ? "worker alive" : detailLoading ? "同步中" : "worker idle"}</small>
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
  if (!detail) return <EmptyState title="等待任务数据" body="创建或选择任务后，这里会出现运行态详情。" large />;
  if (tab === "overview") return <OverviewTab detail={detail} experiments={experiments} onError={onError} onNotice={onNotice} onRefresh={onRefresh} />;
  if (tab === "timeline") return <TimelineTab detail={detail} />;
  if (tab === "observer") return <ObserverTab detail={detail} />;
  if (tab === "memory") return <MemoryTab detail={detail} />;
  if (tab === "evidence") return <EvidenceTab detail={detail} />;
  return <KnowledgeTab mission={detail.mission} onError={onError} onNotice={onNotice} />;
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
      <section className="panel span-2">
        <div className="section-title">
          <ShieldCheck />
          <div>
            <h2>当前判断</h2>
            <p>把 agent 的目标、阻塞点和下一步压缩成可读指挥面板。</p>
          </div>
        </div>
        <div className="brief-grid">
          <BriefItem label="摘要" value={memory.summary || "暂未形成稳定摘要。"} />
          <BriefItem label="最高价值线索" value={memory.highest_value_lead || "暂无"} />
          <BriefItem label="下一条命令" value={memory.next_one_command || "等待下一轮规划"} mono />
          <BriefItem label="阻塞原因" value={memory.blocked_reason || mission.error_message || "未阻塞"} />
        </div>
      </section>
      <section className="panel">
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
      <section className="panel span-2">
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
          <MetricTile label="审核次数" value={String(observer.stats?.decisions || 0)} />
          <MetricTile label="纠偏" value={String(observer.stats?.steers || 0)} />
          <MetricTile label="记忆补丁" value={String(observer.stats?.memory_patches || 0)} />
          <MetricTile label="Skill 信号" value={String(observer.stats?.skill_signals || 0)} />
        </div>
        <div className="decision-board">
          <BriefItem label="Action" value={toText(latest.action || latest.intervention || "none")} />
          <BriefItem label="Severity" value={toText(latest.severity || "normal")} />
          <BriefItem label="Reason" value={toText(latest.reason || latest.rationale || latest.summary || "暂无最新判断")} />
          <BriefItem label="Steer" value={toText(latest.steer || latest.message || latest.follow_up || "无纠偏")} />
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
                  <span className="trace-type">{message.type}</span>
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
    <section className="panel">
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

  return (
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
  );
}

function RuntimeCard({ bootstrap, skills }: { bootstrap: Bootstrap | null; skills: Skill[] }) {
  const knowledgeStatus = bootstrap?.knowledge?.rag?.available
    ? `RAG ready · ${bootstrap.knowledge.rag.total_chunks || 0} chunks`
    : bootstrap?.knowledge?.status || bootstrap?.knowledge?.search_backend || "未加载";
  const loadedEnabledSkills = skills.filter((skill) => skill.enabled).length;
  const enabledSkills = Math.max(Number(bootstrap?.skills?.enabled || 0), loadedEnabledSkills);
  const totalSkills = Math.max(Number(bootstrap?.skills?.total || 0), skills.length);
  return (
    <section className="panel runtime-card">
      <div className="panel-heading compact">
        <span className="panel-icon">
          <Skull />
        </span>
        <div>
          <h2>运行态</h2>
          <p>{bootstrap?.sandbox_container || "sandbox pending"}</p>
        </div>
      </div>
      <div className="runtime-lines">
        <RuntimeLine label="工作目录" value={bootstrap?.sandbox_workdir || "未加载"} />
        <RuntimeLine label="LLM 模式" value={bootstrap?.llm_mode || "未加载"} />
        <RuntimeLine label="知识库" value={knowledgeStatus} />
        <RuntimeLine label="Skills" value={`${enabledSkills}/${totalSkills} enabled`} />
      </div>
    </section>
  );
}

function ExperimentPulse({ experiments }: { experiments: ExperimentRecord[] }) {
  const success = experiments.filter((item) => item.outcome === "success").length;
  const failed = experiments.filter((item) => item.outcome === "failed" || item.outcome === "blocked").length;
  return (
    <section className="panel">
      <div className="panel-heading compact">
        <span className="panel-icon">
          <CheckCircle />
        </span>
        <div>
          <h2>实验记录</h2>
          <p>{experiments.length} 条 mission 归档</p>
        </div>
      </div>
      <div className="experiment-bars">
        <MetricTile label="成功" value={String(success)} />
        <MetricTile label="失败或阻塞" value={String(failed)} />
      </div>
    </section>
  );
}

function SkillDeck({ skills }: { skills: Skill[] }) {
  return (
    <section className="panel">
      <div className="panel-heading compact">
        <span className="panel-icon">
          <Circuitry />
        </span>
        <div>
          <h2>Skills</h2>
          <p>{skills.length ? `${skills.length} 个可用` : "未加载"}</p>
        </div>
      </div>
      <div className="skill-deck">
        {skills.slice(0, 10).map((skill) => (
          <article className="skill-card" key={skill.id}>
            <strong>{skill.name || skill.id}</strong>
            <p>{compact(skill.description, 90)}</p>
          </article>
        ))}
      </div>
    </section>
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
  return (
    <div className="app-shell settings-shell">
      <Atmosphere />
      <Header bootstrap={bootstrap} active="settings" />
      <main className="settings-page">
        <section className="settings-hero">
          <p className="kicker">CONFIG SURFACE</p>
          <h1>把模型、Observer、知识库和运行参数放在一个清晰面板里。</h1>
          <p>保存后后端会热更新可变配置。API Key 返回值会被后端脱敏。</p>
        </section>
        {loading ? <SkeletonPanel /> : null}
        {status ? <InlineNotice tone="ok" message={status} onClose={() => setStatus("")} /> : null}
        {error ? <InlineNotice tone="bad" message={error} onClose={() => setError("")} /> : null}
        <div className="settings-grid">
          {sections.map((section) => (
            <section className="panel settings-card" key={section}>
              <h2>{section}</h2>
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
    <section className="panel">
      <div className="section-title">
        <Graph />
        <div>
          <h2>实验归档</h2>
          <p>记录难度、结果、失败边界和关键参数。</p>
        </div>
      </div>
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
    </section>
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

function EmptyState({ title, body, large }: { title: string; body: string; large?: boolean }) {
  return (
    <div className={large ? "empty-state large" : "empty-state"}>
      <TerminalWindow />
      <strong>{title}</strong>
      <p>{body}</p>
    </div>
  );
}

function InlineNotice({
  tone,
  message,
  onClose
}: {
  tone: "ok" | "bad";
  message: string;
  onClose: () => void;
}) {
  return (
    <div className={`inline-notice ${tone}`}>
      <span>{tone === "ok" ? <CheckCircle /> : <WarningCircle />}</span>
      <p>{message}</p>
      <button type="button" onClick={onClose}>
        关闭
      </button>
    </div>
  );
}

function SkeletonPanel() {
  return (
    <section className="panel skeleton-panel">
      <span />
      <span />
      <span />
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
