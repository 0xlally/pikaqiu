/* ========== PikaQiu Pentest Agent – Main App (Simplified) ========== */

const state = {
  missions: [],
  experiments: [],
  experimentSummary: null,
  pollTimer: null,
  selectedMissionId: null,
  bootstrapDefaults: null,
  openDetailKeys: new Set(),
  expandedContentKeys: new Set(),
  detailStateHydrated: false,
  flowGroupCount: 0,
  lastDetailHash: "",
  lastMissionsHash: "",
  lastExperimentsHash: "",
};

const STATUS_LABELS = {
  queued: "排队中",
  running: "运行中",
  done: "已完成",
  stopped: "已停止",
  error: "异常",
};

const EVENT_TITLES = {
  system: "系统",
  command: "命令执行",
  command_running: "执行中",
  knowledge: "知识库",
  sandbox: "沙箱",
  main_agent: "主决策",
  memory_agent: "记忆压缩",
  observer_agent: "观察纠偏",
  human_guidance: "人类协同",
  error: "异常",
  flag: "🚩 Flag",
};

const ROLE_LABELS = { main: "主决策", memory: "记忆压缩" };
const ROLE_ORDER = { main: 1, memory: 2 };
const OUTCOME_LABELS = {
  unknown: "unknown",
  success: "success",
  failed: "failed",
  timeout: "timeout",
  blocked: "blocked",
};
const FAILURE_REASON_LABELS = [
  ["", "none"],
  ["network_or_proxy", "network/proxy"],
  ["sandbox_missing_tool", "sandbox/tooling"],
  ["target_unreachable", "target unreachable"],
  ["auth_or_token", "auth/token"],
  ["exploit_not_confirmed", "exploit not confirmed"],
  ["time_or_round_limit", "time/round limit"],
  ["model_loop_or_bad_plan", "model loop/bad plan"],
  ["other", "other"],
];

const BJ_TIME_FORMATTER = new Intl.DateTimeFormat("zh-CN", {
  timeZone: "Asia/Shanghai",
  year: "numeric", month: "2-digit", day: "2-digit",
  hour: "2-digit", minute: "2-digit", second: "2-digit",
  timeZoneName: "shortOffset", hour12: false,
});

const missionFormEl = document.getElementById("mission-form");
const formErrorEl = document.getElementById("form-error");
const missionsListEl = document.getElementById("missions-list");
const experimentSummaryEl = document.getElementById("experiment-summary");
const experimentTableEl = document.getElementById("experiment-table");
const missionDetailEl = document.getElementById("mission-detail");
const resumeBtnEl = document.getElementById("resume-btn");
const deleteBtnEl = document.getElementById("delete-btn");
const stopBtnEl = document.getElementById("stop-btn");

// ─── Utilities ───

async function fetchJson(url, options = {}) {
  const response = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  const raw = await response.text();
  let data = {};
  try {
    data = raw ? JSON.parse(raw) : {};
  } catch {
    data = {};
  }
  if (!response.ok) throw new Error(data.error || `HTTP ${response.status}`);
  return data;
}

function applyFormDefaults(defaults) {
  if (!defaults || !missionFormEl) return;
  missionFormEl.max_rounds.value = defaults.max_rounds;
  missionFormEl.max_commands.value = defaults.max_commands;
  missionFormEl.command_timeout_sec.value = defaults.command_timeout_sec;
}

function resetDetailViewState() {
  state.openDetailKeys.clear();
  state.expandedContentKeys.clear();
  state.detailStateHydrated = false;
  state.lastDetailHash = "";
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function compactText(value, limit = 500) {
  const text = String(value ?? "").replace(/\s+/g, " ").trim();
  return text.length <= limit ? text : text.slice(0, limit - 1) + "…";
}

function looksLikeTransportEnvelope(value) {
  const text = String(value ?? "").trim();
  if (!text.startsWith("{") || !text.includes('"type"')) return false;
  const markers = ['"session_id"', '"duration_ms"', '"modelUsage"', '"usage"'];
  return markers.filter((m) => text.includes(m)).length >= 2;
}

function displayMemorySummary(value) {
  const text = String(value ?? "").trim();
  if (!text) return { display: "No summary yet", full: "", truncated: false };
  if (looksLikeTransportEnvelope(text)) return { display: "memory agent returned a transport envelope instead of a summary.", full: "", truncated: false };
  return { display: text, full: text, truncated: false };
}

// ─── Time helpers ───

function parseMissionTime(value) {
  const normalized = String(value || "").trim().replace(/([+-]\d{2})(\d{2})$/, "$1:$2");
  if (!normalized) return null;
  const ms = Date.parse(normalized);
  return Number.isFinite(ms) ? new Date(ms) : null;
}

function formatMissionTime(value) {
  const date = parseMissionTime(value);
  if (!date) return String(value || "时间未知");
  const parts = Object.fromEntries(
    BJ_TIME_FORMATTER.formatToParts(date).map((p) => [p.type, p.value]),
  );
  return `${parts.year}-${parts.month}-${parts.day} ${parts.hour}:${parts.minute}:${parts.second}`;
}

function formatRelativeTime(value) {
  const date = parseMissionTime(value);
  if (!date) return "";
  const delta = Math.round((Date.now() - date.getTime()) / 1000);
  const abs = Math.abs(delta);
  const suffix = delta >= 0 ? "前" : "后";
  if (abs < 60) return `${abs}s ${suffix}`;
  const m = Math.round(abs / 60);
  if (m < 60) return `${m}m ${suffix}`;
  const h = Math.round(m / 60);
  if (h < 48) return `${h}h ${suffix}`;
  return `${Math.round(h / 24)}d ${suffix}`;
}

function formatTimeRange(startValue, endValue) {
  const start = formatMissionTime(startValue);
  const end = formatMissionTime(endValue || startValue);
  if (!startValue && !endValue) return "时间未知";
  if (!endValue || start === end) return start;
  const sd = parseMissionTime(startValue);
  const ed = parseMissionTime(endValue);
  if (sd && ed && sd.toDateString() === ed.toDateString()) {
    const ep = Object.fromEntries(BJ_TIME_FORMATTER.formatToParts(ed).map((p) => [p.type, p.value]));
    return `${start} → ${ep.hour}:${ep.minute}:${ep.second}`;
  }
  return `${start} → ${end}`;
}

function formatDuration(startValue, endValue) {
  const sd = parseMissionTime(startValue);
  const ed = parseMissionTime(endValue || startValue);
  if (!sd || !ed) return "";
  const s = Math.max(0, Math.round((ed - sd) / 1000));
  return s < 60 ? `${s}s` : `${Math.floor(s / 60)}m ${String(s % 60).padStart(2, "0")}s`;
}

function formatDurationSeconds(value) {
  if (value === null || value === undefined || value === "") return "";
  const s = Math.max(0, Number(value) || 0);
  if (s < 60) return `${s}s`;
  const m = Math.floor(s / 60);
  if (m < 60) return `${m}m ${String(s % 60).padStart(2, "0")}s`;
  const h = Math.floor(m / 60);
  return `${h}h ${String(m % 60).padStart(2, "0")}m`;
}

// ─── Chips / Pills ───

function statusPill(status) {
  return `<span class="status-pill status-${escapeHtml(status)}">${escapeHtml(STATUS_LABELS[status] || status)}</span>`;
}

function outcomePill(outcome) {
  const safe = String(outcome || "unknown").trim() || "unknown";
  return `<span class="outcome-pill outcome-${escapeHtml(safe)}">${escapeHtml(OUTCOME_LABELS[safe] || safe)}</span>`;
}

function monoChip(value) {
  return `<span class="mono-chip" title="${escapeHtml(value)}">${escapeHtml(compactText(value, 72))}</span>`;
}

function softChip(value) {
  return `<span class="soft-chip" title="${escapeHtml(value)}">${escapeHtml(compactText(value, 88))}</span>`;
}

function renderChipRail(items, emptyText) {
  const list = (items || []).map((i) => String(i || "").trim()).filter(Boolean);
  if (!list.length) return `<div class="chip-rail"><span class="soft-chip">${escapeHtml(emptyText)}</span></div>`;
  return `<div class="chip-rail">${list.slice(0, 20).map((i) => softChip(i)).join("")}</div>`;
}

function asMemoryList(value) {
  if (Array.isArray(value)) return value.map((i) => String(i || "").trim()).filter(Boolean);
  const text = String(value || "").trim();
  return text ? [text] : [];
}

function memoryNextFocus(memory) {
  const canonical = asMemoryList(memory?.next_focus);
  return canonical.length ? canonical : asMemoryList(memory?.nex_focus);
}

function renderMemoryColumn(label, items, emptyText, extraClass = "") {
  return `
    <div class="memory-column ${escapeHtml(extraClass)}">
      <div class="kv-title">${escapeHtml(label)}</div>
      ${renderMemoryList(asMemoryList(items), emptyText)}
    </div>
  `;
}

function renderMemoryList(items, emptyText) {
  const list = asMemoryList(items);
  if (!list.length) return `<div class="memory-empty">${escapeHtml(emptyText)}</div>`;
  return `
    <ul class="memory-list">
      ${list.map((item) => `<li class="memory-item">${escapeHtml(item)}</li>`).join("")}
    </ul>
  `;
}

function renderGuidanceHistory(items) {
  const list = Array.isArray(items) ? items.slice(-8) : [];
  if (!list.length) return `<div class="guidance-empty">暂无人工引导</div>`;
  return `
    <div class="guidance-history">
      ${list.map((item) => `
        <article class="guidance-entry">
          <div class="guidance-entry-head">
            <span class="guidance-status status-${escapeHtml(item.status || "pending")}">${escapeHtml(item.status || "pending")}</span>
            <span>${escapeHtml(formatMissionTime(item.created_at))}</span>
          </div>
          <p>${escapeHtml(item.content || "")}</p>
        </article>
      `).join("")}
    </div>
  `;
}

function renderHumanCollabPanel(mission, guidanceItems, threadAlive, draft) {
  const enabled = Boolean(mission?.human_collab_enabled);
  const canSend = enabled && Boolean(threadAlive || ["queued", "running"].includes(mission?.status));
  return `
    <section class="human-collab-panel">
      <div class="human-collab-head">
        <div>
          <p class="section-kicker">human collaboration</p>
          <h4>人类协同引导</h4>
        </div>
        <label class="collab-toggle">
          <input id="human-collab-toggle" type="checkbox" ${enabled ? "checked" : ""} />
          <span>${enabled ? "已开启" : "已关闭"}</span>
        </label>
      </div>
      <form id="human-guidance-form" class="collab-form">
        <textarea id="human-guidance-input" rows="3" maxlength="4000" ${canSend ? "" : "disabled"} placeholder="${enabled ? "输入下一步渗透方向、假设或需要优先验证的路径" : "开启人类协同后可发送引导词"}">${escapeHtml(draft || "")}</textarea>
        <button id="human-guidance-submit" type="submit" class="secondary" ${canSend ? "" : "disabled"}>发送给 agent</button>
      </form>
      <p id="human-guidance-status" class="collab-status"></p>
      ${renderGuidanceHistory(guidanceItems)}
    </section>
  `;
}

function bindHumanCollabControls(missionId) {
  const toggle = document.getElementById("human-collab-toggle");
  const form = document.getElementById("human-guidance-form");
  const input = document.getElementById("human-guidance-input");
  const status = document.getElementById("human-guidance-status");

  toggle?.addEventListener("change", async () => {
    toggle.disabled = true;
    if (status) status.textContent = "正在更新协同开关...";
    try {
      await fetchJson(`/api/missions/${missionId}/collaboration`, {
        method: "POST",
        body: JSON.stringify({ enabled: toggle.checked }),
      });
      state.lastDetailHash = "";
      await refreshAll();
    } catch (err) {
      if (status) status.textContent = `更新失败: ${err.message || err}`;
      toggle.checked = !toggle.checked;
      toggle.disabled = false;
    }
  });

  form?.addEventListener("submit", async (event) => {
    event.preventDefault();
    const content = String(input?.value || "").trim();
    if (!content) {
      if (status) status.textContent = "请输入引导词。";
      return;
    }
    const submit = document.getElementById("human-guidance-submit");
    if (submit) submit.disabled = true;
    if (status) status.textContent = "正在发送给 agent...";
    try {
      await fetchJson(`/api/missions/${missionId}/guidance`, {
        method: "POST",
        body: JSON.stringify({ content }),
      });
      if (input) input.value = "";
      state.lastDetailHash = "";
      await refreshAll();
    } catch (err) {
      if (status) status.textContent = `发送失败: ${err.message || err}`;
      if (submit) submit.disabled = false;
    }
  });
}

// --- Observer monitor helpers ---

function observerEvents(events) {
  return (events || []).filter((event) => event.type === "observer_agent");
}

function observerDecision(event) {
  const decision = event?.metadata?.observer;
  return decision && typeof decision === "object" ? decision : null;
}

function observerMemoryPatch(event) {
  const fromEvent = event?.metadata?.observer_memory_patch;
  if (fromEvent && typeof fromEvent === "object") return fromEvent;
  const fromDecision = observerDecision(event)?.memory_patch;
  return fromDecision && typeof fromDecision === "object" ? fromDecision : {};
}

function observerPatchCount(patch) {
  if (!patch || typeof patch !== "object") return 0;
  return Object.values(patch).reduce((total, value) => {
    if (Array.isArray(value)) return total + value.length;
    return total + (String(value || "").trim() ? 1 : 0);
  }, 0);
}

function observerPatchSummary(patch) {
  if (!patch || typeof patch !== "object") return "";
  return Object.entries(patch)
    .map(([key, value]) => {
      const count = Array.isArray(value) ? value.length : (String(value || "").trim() ? 1 : 0);
      return count ? `${key}:${count}` : "";
    })
    .filter(Boolean)
    .join(" · ");
}

function observerSeverityClass(severity) {
  const safe = String(severity || "none").toLowerCase();
  return ["none", "info", "warn", "critical"].includes(safe) ? safe : "info";
}

function observerActionable(decision, patch) {
  if (!decision) return observerPatchCount(patch) > 0;
  return Boolean(
    (decision.action && decision.action !== "no_action")
    || (decision.intervention && decision.intervention !== "none")
    || decision.steer_message
    || decision.skill_signal
    || (decision.skill_card && decision.skill_card !== "none")
    || observerPatchCount(patch) > 0
  );
}

function renderObserverStat(label, value, hint = "") {
  return `
    <div class="observer-stat">
      <span>${escapeHtml(label)}</span>
      <strong>${escapeHtml(value)}</strong>
      ${hint ? `<em>${escapeHtml(hint)}</em>` : ""}
    </div>
  `;
}

function renderObserverEntry(event) {
  const decision = observerDecision(event) || {};
  const patch = observerMemoryPatch(event);
  const patchSummary = observerPatchSummary(patch);
  const severity = observerSeverityClass(decision.severity || (patchSummary ? "info" : "none"));
  const stateLabel = decision.state || (patchSummary ? "memory_sync" : "notice");
  const intervention = decision.intervention || (patchSummary ? "memory_sync" : "none");
  const action = decision.action || (intervention === "none" ? "no_action" : intervention);
  const problems = Array.isArray(decision.problems) ? decision.problems.filter(Boolean) : [];
  const skillCard = decision.skill_signal || (decision.skill_card && decision.skill_card !== "none" ? decision.skill_card : "");
  const steer = decision.steer_message || "";
  const instruction = decision.skill_instruction || "";
  const route = decision.route_assessment || "";
  const refs = Array.isArray(decision.experience_refs) ? decision.experience_refs.filter(Boolean) : [];
  const phase = event?.metadata?.phase || "event";
  const fallback = !steer && !instruction ? compactText(event.content || event.title || "", 260) : "";

  return `
    <article class="observer-entry observer-severity-${escapeHtml(severity)}">
      <div class="observer-entry-head">
        <span class="observer-phase">${escapeHtml(phase)}</span>
        <span>${escapeHtml(formatMissionTime(event.started_at))}</span>
      </div>
      <div class="observer-entry-title">${escapeHtml(event.title || "Observer decision")}</div>
      <div class="observer-meta-row">
        ${monoChip(`state: ${stateLabel}`)}
        ${monoChip(`action: ${action}`)}
        ${monoChip(`intervention: ${intervention}`)}
        ${monoChip(`severity: ${severity}`)}
        ${skillCard ? monoChip(`skill: ${skillCard}`) : ""}
      </div>
      ${route ? `<p class="observer-route">Route: ${escapeHtml(route)}</p>` : ""}
      ${problems.length ? `
        <ul class="observer-problems">
          ${problems.slice(0, 5).map((problem) => `<li>${escapeHtml(problem)}</li>`).join("")}
        </ul>
      ` : ""}
      ${steer ? `<p class="observer-steer">Steer: ${escapeHtml(steer)}</p>` : ""}
      ${instruction ? `<p class="observer-instruction">${escapeHtml(instruction)}</p>` : ""}
      ${skillCard ? `<p class="observer-skill">Skill signal: ${escapeHtml(skillCard)}</p>` : ""}
      ${refs.length ? `<p class="observer-refs">Experience: ${refs.slice(0, 5).map(escapeHtml).join(" · ")}</p>` : ""}
      ${patchSummary ? `<p class="observer-patch">Memory sync: ${escapeHtml(patchSummary)}</p>` : ""}
      ${fallback ? `<p class="observer-fallback">${escapeHtml(fallback)}</p>` : ""}
    </article>
  `;
}

function renderObserverMonitorLegacy(events) {
  const list = observerEvents(events);
  const items = list.map((event) => {
    const decision = observerDecision(event);
    const patch = observerMemoryPatch(event);
    return { event, decision, patch };
  });
  const latest = items.at(-1);
  const latestDecision = latest?.decision || {};
  const latestPatch = latest?.patch || {};
  const latestPatchCount = observerPatchCount(latestPatch);
  const latestSeverity = observerSeverityClass(latestDecision.severity || (latest ? "info" : "none"));
  const latestState = latestDecision.state || (latestPatchCount ? "memory_sync" : (latest ? "watching" : "armed"));
  const latestIntervention = latestDecision.intervention || (latestPatchCount ? "memory_sync" : "none");
  const latestSkill = latestDecision.skill_card && latestDecision.skill_card !== "none" ? latestDecision.skill_card : "none";
  const actionableCount = items.filter(({ decision, patch }) => observerActionable(decision, patch)).length;
  const criticalWarnCount = items.filter(({ decision }) => ["critical", "warn"].includes(decision?.severity)).length;
  const steerCount = items.filter(({ decision }) => ["steer", "follow_up", "rollback_steer"].includes(decision?.intervention)).length;
  const skillCount = items.filter(({ decision }) => decision?.skill_card && decision.skill_card !== "none").length;
  const memorySyncCount = items.filter(({ event, patch }) => event.title === "Observer memory sync applied" || observerPatchCount(patch) > 0).length;
  const latestSteer = latestDecision.steer_message || "";
  const recent = list.slice(-6).reverse();

  return `
    <section class="observer-monitor observer-severity-${escapeHtml(latestSeverity)}">
      <div class="observer-monitor-head">
        <div>
          <p class="section-kicker">observer agent</p>
          <h4>Observer 监控台</h4>
          <p>持续展示纠偏、回退 steer、memory sync 和 skill 使用信号，让 Observer 的介入变得可见。</p>
        </div>
        <div class="observer-live-badge">
          <span class="observer-dot"></span>
          <strong>${escapeHtml(latestState)}</strong>
          <small>${escapeHtml(latestIntervention)}</small>
        </div>
      </div>

      <div class="observer-status-grid">
        ${renderObserverStat("Decisions", String(list.length), `${actionableCount} actionable`)}
        ${renderObserverStat("Warn/Critical", String(criticalWarnCount), latestSeverity)}
        ${renderObserverStat("Steers", String(steerCount), "steer/follow-up")}
        ${renderObserverStat("Memory Sync", String(memorySyncCount), "patches applied")}
        ${renderObserverStat("Skill Signals", String(skillCount), latestSkill)}
      </div>

      ${latestSteer ? `
        <div class="observer-current-steer">
          <span>Current steer</span>
          <p>${escapeHtml(latestSteer)}</p>
        </div>
      ` : ""}

      <div class="observer-feed">
        <div class="observer-feed-head">
          <span>Recent Observer Activity</span>
          <span>${escapeHtml(list.length ? `${recent.length}/${list.length} shown` : "waiting for signal")}</span>
        </div>
        ${recent.length ? recent.map(renderObserverEntry).join("") : `
          <div class="observer-empty">
            Observer 已启用但尚未介入。出现重复扫描、连续失败、flag 未提交、版本未查 CVE、RCE 后未找 flag 等信号时，这里会显示它的判断和纠偏动作。
          </div>
        `}
      </div>
    </section>
  `;
}

// ─── Detail open/close state ───

function observerMessageDecision(message) {
  const decision = message?.metadata?.decision;
  return decision && typeof decision === "object" ? decision : null;
}

function renderObserverMessage(message) {
  const decision = observerMessageDecision(message) || {};
  const patch = decision.memory_patch && typeof decision.memory_patch === "object" ? decision.memory_patch : {};
  const patchSummary = observerPatchSummary(patch);
  const severity = observerSeverityClass(decision.severity || (message.type === "decision" ? "info" : "none"));
  const stateLabel = decision.state || message.type || "activity";
  const action = decision.action || (message.type === "decision" ? "no_action" : message.direction || "internal");
  const phase = message?.metadata?.phase || message.type || "observer";
  const problems = Array.isArray(decision.problems) ? decision.problems.filter(Boolean) : [];
  const steer = decision.steer_message || "";
  const route = decision.route_assessment || "";
  const visible = decision.visible_summary || "";
  const skillSignal = decision.skill_signal || (decision.skill_card && decision.skill_card !== "none" ? decision.skill_card : "");
  const refs = Array.isArray(decision.experience_refs) ? decision.experience_refs.filter(Boolean) : [];
  const fallback = !steer && !route && !visible ? compactText(message.content || message.title || "", 360) : "";

  return `
    <article class="observer-entry observer-severity-${escapeHtml(severity)}">
      <div class="observer-entry-head">
        <span class="observer-phase">${escapeHtml(phase)}</span>
        <span>${escapeHtml(formatMissionTime(message.created_at))}</span>
      </div>
      <div class="observer-entry-title">${escapeHtml(message.title || "Observer activity")}</div>
      <div class="observer-meta-row">
        ${monoChip(`type: ${message.type || "message"}`)}
        ${monoChip(`state: ${stateLabel}`)}
        ${monoChip(`action: ${action}`)}
        ${monoChip(`severity: ${severity}`)}
      </div>
      ${visible ? `<p class="observer-fallback">${escapeHtml(visible)}</p>` : ""}
      ${route ? `<p class="observer-route">Route: ${escapeHtml(route)}</p>` : ""}
      ${problems.length ? `
        <ul class="observer-problems">
          ${problems.slice(0, 5).map((problem) => `<li>${escapeHtml(problem)}</li>`).join("")}
        </ul>
      ` : ""}
      ${steer ? `<p class="observer-steer">Steer: ${escapeHtml(steer)}</p>` : ""}
      ${skillSignal ? `<p class="observer-skill">Skill signal: ${escapeHtml(skillSignal)}</p>` : ""}
      ${refs.length ? `<p class="observer-refs">Experience: ${refs.slice(0, 6).map(escapeHtml).join(" · ")}</p>` : ""}
      ${patchSummary ? `<p class="observer-patch">Memory sync: ${escapeHtml(patchSummary)}</p>` : ""}
      ${fallback ? `<p class="observer-fallback">${escapeHtml(fallback)}</p>` : ""}
    </article>
  `;
}

function renderObserverMonitor(observer, events) {
  const messages = Array.isArray(observer?.messages) ? observer.messages : [];
  if (!messages.length) {
    return renderObserverMonitorLegacy(events);
  }

  const decisions = messages
    .map((message) => ({ message, decision: observerMessageDecision(message) }))
    .filter(({ decision }) => decision);
  const latestDecision = observer?.latest_decision || decisions.at(-1)?.decision || {};
  const latestPatch = latestDecision.memory_patch && typeof latestDecision.memory_patch === "object" ? latestDecision.memory_patch : {};
  const latestPatchCount = observerPatchCount(latestPatch);
  const latestSeverity = observerSeverityClass(latestDecision.severity || "info");
  const latestState = latestDecision.state || observer?.status || "observing";
  const latestAction = latestDecision.action || "no_action";
  const latestSteer = latestDecision.steer_message || "";
  const latestRoute = latestDecision.route_assessment || "";
  const latestSkill = latestDecision.skill_signal || (latestDecision.skill_card && latestDecision.skill_card !== "none" ? latestDecision.skill_card : "none");
  const latestRefs = Array.isArray(latestDecision.experience_refs) ? latestDecision.experience_refs.filter(Boolean) : [];
  const stats = observer?.stats || {};
  const actionableCount = decisions.filter(({ decision }) => observerActionable(decision, decision.memory_patch)).length;
  const recent = messages.slice(-8).reverse();

  return `
    <section class="observer-monitor observer-severity-${escapeHtml(latestSeverity)}">
      <div class="observer-monitor-head">
        <div>
          <p class="section-kicker">observer agent</p>
          <h4>Observer Timeline</h4>
          <p>独立监督会话，记录 observation、内部思考、experience/skill 只读引用和最终纠偏结论。</p>
        </div>
        <div class="observer-live-badge">
          <span class="observer-dot"></span>
          <strong>${escapeHtml(observer?.status || latestState)}</strong>
          <small>${escapeHtml(latestAction)}</small>
        </div>
      </div>

      <div class="observer-status-grid">
        ${renderObserverStat("Messages", String(stats.messages ?? messages.length), `${decisions.length} decisions`)}
        ${renderObserverStat("Warn/Critical", String(stats.warn_critical ?? 0), latestSeverity)}
        ${renderObserverStat("Actionable", String(actionableCount), latestAction)}
        ${renderObserverStat("Memory Patch", String(stats.memory_patches ?? (latestPatchCount ? 1 : 0)), "allowed keys only")}
        ${renderObserverStat("Skill Signals", String(stats.skill_signals ?? 0), latestSkill)}
      </div>

      ${latestRoute ? `
        <div class="observer-current-steer">
          <span>Route assessment</span>
          <p>${escapeHtml(latestRoute)}</p>
        </div>
      ` : ""}

      ${latestSteer ? `
        <div class="observer-current-steer">
          <span>Current steer</span>
          <p>${escapeHtml(latestSteer)}</p>
        </div>
      ` : ""}

      ${latestSkill && latestSkill !== "none" ? `<p class="observer-skill">Skill signal: ${escapeHtml(latestSkill)}</p>` : ""}
      ${latestRefs.length ? `<p class="observer-refs">Experience refs: ${latestRefs.slice(0, 8).map(escapeHtml).join(" · ")}</p>` : ""}
      ${latestPatchCount ? `<p class="observer-patch">Memory sync: ${escapeHtml(observerPatchSummary(latestPatch))}</p>` : ""}

      <div class="observer-feed">
        <div class="observer-feed-head">
          <span>Observer Timeline</span>
          <span>${escapeHtml(`${recent.length}/${messages.length} shown`)}</span>
        </div>
        ${recent.map(renderObserverMessage).join("")}
      </div>
    </section>
  `;
}

function captureDetailOpenState() {
  state.openDetailKeys = new Set(
    Array.from(missionDetailEl.querySelectorAll("details[data-detail-key][open]")).map(
      (d) => d.dataset.detailKey,
    ),
  );
}

function restoreDetailOpenState() {
  missionDetailEl.querySelectorAll("details[data-detail-key]").forEach((detail) => {
    const key = detail.dataset.detailKey;
    if (key && state.openDetailKeys.has(key)) detail.open = true;
    detail.addEventListener("toggle", () => {
      if (!key) return;
      detail.open ? state.openDetailKeys.add(key) : state.openDetailKeys.delete(key);
    });
  });
}

// ─── Expand content handler ───

function expandContent(btn) {
  const pre = btn.previousElementSibling;
  if (!pre) return;
  const full = pre.dataset.fullContent;
  if (full) {
    pre.textContent = full;
    pre.classList.remove("is-truncated");
    // Track this expansion so re-renders don't collapse it
    const key = pre.dataset.expandKey;
    if (key) state.expandedContentKeys.add(key);
  }
  btn.remove();
}

function renderTruncatedContent(fullContent, limit, expandKey) {
  const isExpanded = expandKey && state.expandedContentKeys.has(expandKey);
  const isTruncated = !isExpanded && fullContent.length > limit;
  const display = isTruncated ? fullContent.slice(0, limit) + "\n…" : fullContent;
  const dataAttr = isTruncated ? ` data-full-content="${escapeHtml(fullContent)}"` : "";
  const keyAttr = expandKey ? ` data-expand-key="${escapeHtml(expandKey)}"` : "";
  return `<div class="event-content-wrap"><pre class="event-pre ${isTruncated ? "is-truncated" : ""}"${dataAttr}${keyAttr}>${escapeHtml(display)}</pre>${isTruncated ? `<button class="expand-btn" onclick="expandContent(this)">展开全部 (${fullContent.length} chars)</button>` : ""}</div>`;
}

// ─── Round helpers ───

function extractRoundKnowledge(round) {
  const lines = String(round?.prompt_excerpt || "").split(/\r?\n/);
  const titles = [];
  for (const line of lines) {
    const m = line.match(/^\[\d+\]\s+domain=([^\s]+)\s+source=([^\s]+)\s+title=(.+)$/);
    if (m?.[3]) titles.push(`${m[1]} · ${m[3].trim()}`);
  }
  return titles.slice(0, 6);
}

function summarizeRound(round) {
  const d = round.decision || {};
  if (round.worker_role === "main") return compactText(d.round_goal || d.thought_summary || "等待下一步动作", 140);
  if (round.worker_role === "memory") return compactText(d.summary || "记忆压缩完成", 140);
  return compactText(d.visible_summary || d.route_assessment || "未识别的历史记录", 140);
}

function roundStats(round) {
  const d = round.decision || {};
  if (round.worker_role === "main") return `cmd ${(d.commands || []).length} · finding ${(d.findings || []).length} · ${d.status || "continue"}`;
  if (round.worker_role === "memory") return `facts ${(d.findings || []).length} · leads ${(d.leads || []).length}`;
  return `queries ${(d.next_queries || []).length} · cmds ${(d.next_commands || []).length}`;
}

function groupMissionFlow(rounds, events) {
  const groups = new Map();
  const ensure = (rn) => {
    if (!groups.has(rn)) groups.set(rn, { roundNo: rn, rounds: [], events: [], startedAt: "", endedAt: "" });
    return groups.get(rn);
  };
  (rounds || []).forEach((r) => ensure(r.round_no || 0).rounds.push(r));
  (events || []).forEach((e) => ensure(e.round_no || 0).events.push(e));
  const list = Array.from(groups.values());
  list.forEach((g) => {
    g.rounds.sort((a, b) => (ROLE_ORDER[a.worker_role] || 99) - (ROLE_ORDER[b.worker_role] || 99));
    g.events.sort((a, b) => Number(a.id || 0) - Number(b.id || 0));
    g.startedAt = g.events[0]?.started_at || g.rounds[0]?.created_at || "";
    g.endedAt = g.events.at(-1)?.ended_at || g.rounds.at(-1)?.created_at || g.startedAt;
  });
  return list.sort((a, b) => a.roundNo - b.roundNo);
}

// ─── Event helpers ───

function eventTone(event) {
  if (event.type === "observer_agent") {
    const decision = observerDecision(event);
    if (decision?.severity === "critical") return "danger";
    if (decision?.severity === "warn") return "running";
    if (observerPatchCount(observerMemoryPatch(event)) > 0) return "success";
    return "command";
  }
  if (event.type === "command_running") return "running";
  if (event.type === "flag") return "success";
  if (event.exit_code !== 0 || event.type === "error") return "danger";
  if (event.type === "command") return "command";
  if (event.type === "system" && /完成/.test(event.title + event.content)) return "success";
  return "neutral";
}

function summarizeEvent(event) {
  if (event.command) {
    const m = String(event.content || "").match(/^purpose:\s*(.+)$/m);
    if (m?.[1]) return compactText(m[1], 150);
    // Don't repeat command here — it's shown in command-inline
    return "";
  }
  return compactText(event.content, 130) || event.title;
}

function commandPreview(event) {
  const lines = String(event.content || "").split(/\r?\n/).map((l) => l.trim()).filter(Boolean);
  const idx = lines.findIndex((l) => l === "STDOUT:" || l === "STDERR:");
  if (idx < 0 || idx + 1 >= lines.length) return "";
  const out = lines.slice(idx + 1).find((l) => !/^\[exit=/.test(l));
  return out ? compactText(out, 160) : "";
}

// ─── Render: Mission List ───

function renderMissions() {
  if (!state.missions.length) {
    const emptyHash = "__empty__";
    if (state.lastMissionsHash === emptyHash) return;
    state.lastMissionsHash = emptyHash;
    missionsListEl.innerHTML = `<div class="empty-state">暂无任务，从上方创建一个新任务。</div>`;
    return;
  }

  // Skip re-render if mission list hasn't changed
  const hash = JSON.stringify(state.missions.map(m => [m.id, m.status, m.updated_at, m.name])) + "|" + (state.selectedMissionId || "");
  if (hash === state.lastMissionsHash) return;
  state.lastMissionsHash = hash;

  missionsListEl.innerHTML = state.missions
    .map((m) => {
      const active = m.id === state.selectedMissionId ? "active" : "";
      return `
        <article class="mission-card ${active}" data-id="${escapeHtml(m.id)}">
          <div class="mission-title-row">
            <strong>${escapeHtml(compactText(m.name, 30))}</strong>
            ${statusPill(m.status)}
          </div>
          <div class="mission-target" title="${escapeHtml(m.target)}">${escapeHtml(compactText(m.target, 40))}</div>
          <div class="mission-time">${escapeHtml(formatRelativeTime(m.updated_at))}</div>
        </article>
      `;
    })
    .join("");

  missionsListEl.querySelectorAll(".mission-card").forEach((card) => {
    card.addEventListener("click", async () => {
      if (state.selectedMissionId !== card.dataset.id) {
        resetDetailViewState();
      }
      state.selectedMissionId = card.dataset.id;
      renderMissions();
      renderExperiments();
      await refreshMissionDetail();
    });
  });
}

// ─── Render: Decision Brief ───

function renderExperiments() {
  if (!experimentSummaryEl || !experimentTableEl) return;
  const records = state.experiments || [];
  const summary = state.experimentSummary || {};
  const hash = JSON.stringify({
    selected: state.selectedMissionId || "",
    summary,
    records: records.map((r) => [
      r.mission_id, r.updated_at, r.outcome, r.failure_reason,
      r.command_count, r.error_count, r.duration_sec,
    ]),
  });
  if (hash === state.lastExperimentsHash) return;
  state.lastExperimentsHash = hash;

  const rate = Math.round(Number(summary.success_rate || 0) * 100);
  experimentSummaryEl.innerHTML = `
    <div class="experiment-summary-grid">
      <div><span>Total</span><strong>${escapeHtml(summary.total ?? 0)}</strong></div>
      <div><span>Success</span><strong>${escapeHtml(`${rate}%`)}</strong></div>
      <div><span>Solved</span><strong>${escapeHtml(summary.success_count ?? 0)}</strong></div>
      <div><span>Avg time</span><strong>${escapeHtml(formatDurationSeconds(summary.avg_duration_sec) || "-")}</strong></div>
    </div>
  `;

  if (!records.length) {
    experimentTableEl.innerHTML = `<div class="empty-state">No experiment records yet.</div>`;
    return;
  }

  experimentTableEl.innerHTML = `
    <table class="experiment-table">
      <thead>
        <tr>
          <th>Time</th>
          <th>Challenge</th>
          <th>Target</th>
          <th>Diff</th>
          <th>Outcome</th>
          <th>Duration</th>
          <th>Skills</th>
          <th>Cmd/Err</th>
          <th>Failure</th>
          <th>Notes</th>
        </tr>
      </thead>
      <tbody>
        ${records.slice(0, 80).map((r) => {
          const active = r.mission_id === state.selectedMissionId ? "active" : "";
          const skillList = (r.activated_skills || []).length ? r.activated_skills : (r.selected_skills || []);
          const skills = skillList.join(", ");
          return `
            <tr class="${active}" data-id="${escapeHtml(r.mission_id)}">
              <td>${escapeHtml(formatMissionTime(r.started_at || r.updated_at))}</td>
              <td title="${escapeHtml(r.mission_id)}">${escapeHtml(compactText(r.challenge_code || r.mission_name || r.mission_id, 34))}</td>
              <td title="${escapeHtml(r.target)}">${escapeHtml(compactText(r.target, 34))}</td>
              <td>${escapeHtml(r.difficulty || "-")}</td>
              <td>${outcomePill(r.outcome)}</td>
              <td>${escapeHtml(formatDurationSeconds(r.duration_sec) || "-")}</td>
              <td title="${escapeHtml(skills)}">${escapeHtml(compactText(skills || "-", 28))}</td>
              <td>${escapeHtml(`${r.command_count || 0}/${r.error_count || 0}`)}</td>
              <td title="${escapeHtml(r.failure_reason)}">${escapeHtml(compactText(r.failure_reason || "-", 28))}</td>
              <td title="${escapeHtml(r.notes || r.key_parameters)}">${escapeHtml(compactText(r.notes || r.key_parameters || "-", 42))}</td>
            </tr>
          `;
        }).join("")}
      </tbody>
    </table>
  `;

  experimentTableEl.querySelectorAll("tr[data-id]").forEach((row) => {
    row.addEventListener("click", async () => {
      if (state.selectedMissionId !== row.dataset.id) {
        resetDetailViewState();
      }
      state.selectedMissionId = row.dataset.id;
      renderMissions();
      renderExperiments();
      await refreshMissionDetail();
    });
  });
}

function renderDecisionBrief(round, role, roundNo) {
  const detailKey = `round:${roundNo}:role:${role}`;
  if (!round) {
    return `
      <div class="role-brief role-empty">
        <div class="role-brief-head">
          <span class="trace-type">${escapeHtml((ROLE_LABELS[role] || role).toUpperCase())}</span>
          <span class="trace-meta">暂无输出</span>
        </div>
        <div class="role-brief-text">这一轮还没有 ${escapeHtml(ROLE_LABELS[role] || role)} 结果。</div>
      </div>
    `;
  }
  const kbTitles = role === "main" ? extractRoundKnowledge(round) : [];
  const fullJson = JSON.stringify(round.decision || {}, null, 2);

  return `
    <details class="role-brief" data-detail-key="${escapeHtml(detailKey)}">
      <summary>
        <div class="role-brief-head">
          <span class="trace-type">${escapeHtml(ROLE_LABELS[role] || role.toUpperCase())}</span>
          <span class="trace-meta">${escapeHtml(roundStats(round))}</span>
        </div>
        <div class="role-brief-text">${escapeHtml(summarizeRound(round))}</div>
        ${kbTitles.length ? `<div class="kb-hit-row">${renderChipRail(kbTitles, "暂无知识库命中")}</div>` : ""}
      </summary>
      ${renderTruncatedContent(fullJson, 500, detailKey)}
    </details>
  `;
}

// ─── Render: Event Card ───

function renderEventCard(event) {
  const tone = eventTone(event);
  const typeLabel = EVENT_TITLES[event.type] || event.type.toUpperCase();
  const previewText = event.command ? commandPreview(event) : "";
  const detailKey = `event:${event.id}`;
  const fullContent = String(event.content || "");
  const purposeMatch = event.command ? String(event.content || "").match(/^purpose:\s*(.+)$/m) : null;
  const purposeText = purposeMatch?.[1] || "";

  return `
    <details class="trace-card event-trace tone-${escapeHtml(tone)}" data-detail-key="${escapeHtml(detailKey)}">
      <summary>
        <div class="trace-head">
          <span class="trace-type">${escapeHtml(typeLabel)}</span>
          <span class="trace-title">${escapeHtml(event.title)}</span>
          ${purposeText ? `<span class="trace-purpose">${escapeHtml(compactText(purposeText, 100))}</span>` : ""}
        </div>
        <div class="trace-meta">
          ${event.command ? `<span class="command-inline">$ ${escapeHtml(compactText(event.command, 140))}</span>` : ""}
          ${!event.command ? `<span>${escapeHtml(summarizeEvent(event))}</span>` : ""}
          ${previewText ? `<span class="output-inline">${escapeHtml(previewText)}</span>` : ""}
          <span>${escapeHtml(formatMissionTime(event.started_at))}${formatDuration(event.started_at, event.ended_at) ? ` · 耗时 ${escapeHtml(formatDuration(event.started_at, event.ended_at))}` : ""}</span>
          ${event.exit_code !== undefined && event.exit_code !== null ? statusPill(event.exit_code === 0 ? "done" : "error") : ""}
        </div>
      </summary>
      ${renderTruncatedContent(fullContent, event.type === "command" ? 2000 : 500, detailKey)}
    </details>
  `;
}

// ─── Render: Flow Round ───

function renderFlowRound(group, index) {
  const mainRound = group.rounds.find((r) => r.worker_role === "main");
  const memoryRound = group.rounds.find((r) => r.worker_role === "memory");
  const mainD = mainRound?.decision || {};
  const title = group.roundNo === 0
    ? "任务启动 / 知识库索引 / Sandbox 自检"
    : mainD.round_goal || summarizeRound(mainRound || memoryRound || {});
  const digest = group.roundNo === 0
    ? compactText(group.events.map((e) => e.title).join(" / "), 180)
    : compactText(mainD.thought_summary || memoryRound?.decision?.summary || "", 220);
  const cmdCount = group.events.filter((e) => e.type === "command").length;
  const badge = group.roundNo === 0 ? "BOOT" : `R${String(group.roundNo).padStart(2, "0")}`;
  const dur = formatDuration(group.startedAt, group.endedAt);
  const isLatest = !state.detailStateHydrated && index === state.flowGroupCount - 1;
  const detailKey = `flow-round:${group.roundNo}`;

  return `
    <details class="flow-round-card" data-detail-key="${escapeHtml(detailKey)}" ${isLatest ? "open" : ""}>
      <summary>
        <div class="flow-round-head">
          <span class="round-badge">${escapeHtml(badge)}</span>
          <div class="flow-round-copy">
            <h4>${escapeHtml(title)}</h4>
            <p>${escapeHtml(digest || "本轮暂无摘要")}</p>
          </div>
        </div>
        <div class="flow-round-meta">
          <span class="time-chip">${escapeHtml(formatTimeRange(group.startedAt, group.endedAt))}${dur ? ` · ${escapeHtml(dur)}` : ""}</span>
          <span class="mono-chip">${escapeHtml(`${cmdCount} cmd · ${group.events.length} events`)}</span>
          ${group.roundNo === 0 ? "" : statusPill(mainD.status || "continue")}
        </div>
      </summary>
      ${group.roundNo === 0 ? "" : `
        <div class="role-brief-grid">
          ${renderDecisionBrief(mainRound, "main", group.roundNo)}
          ${renderDecisionBrief(memoryRound, "memory", group.roundNo)}
        </div>
      `}
      <div class="event-stack">
        ${group.events.length ? group.events.map((e) => renderEventCard(e)).join("") : `<div class="empty-state">这一轮暂无事件。</div>`}
      </div>
    </details>
  `;
}

// ─── Render: Mission Detail ───

function getExperimentDraft(missionId) {
  const form = document.getElementById("experiment-form");
  if (!form || form.dataset.missionId !== missionId) return null;
  const fd = new FormData(form);
  return {
    challenge_code: fd.get("challenge_code"),
    difficulty: fd.get("difficulty"),
    outcome: fd.get("outcome"),
    failure_reason: fd.get("failure_reason"),
    key_parameters: fd.get("key_parameters"),
    notes: fd.get("notes"),
  };
}

function renderOptionList(items, selected) {
  return items.map(([value, label]) => (
    `<option value="${escapeHtml(value)}" ${String(value) === String(selected || "") ? "selected" : ""}>${escapeHtml(label)}</option>`
  )).join("");
}

function renderExperimentPanel(mission, experiment, events, draft) {
  const record = {
    challenge_code: "",
    difficulty: "",
    outcome: "unknown",
    failure_reason: "",
    key_parameters: "",
    notes: "",
    activated_skills: mission?.activated_skills || [],
    selected_skills: mission?.skills || [],
    command_count: (events || []).filter((e) => e.type === "command").length,
    error_count: (events || []).filter((e) => e.type === "error" || e.exit_code !== 0).length,
    flag_count: (events || []).filter((e) => e.type === "flag").length,
    started_at: mission?.created_at || "",
    ended_at: ["done", "error", "stopped", "timeout"].includes(mission?.status) ? mission?.updated_at || "" : "",
    duration_sec: null,
    ...(experiment || {}),
    ...(draft || {}),
  };
  const outcomeOptions = Object.keys(OUTCOME_LABELS).map((key) => [key, OUTCOME_LABELS[key]]);
  const skillList = (record.activated_skills || []).length ? record.activated_skills : (record.selected_skills || []);
  const skills = skillList.join(", ");
  const duration = formatDurationSeconds(record.duration_sec) || formatDuration(record.started_at, record.ended_at) || "-";

  return `
    <section class="experiment-detail-panel">
      <div class="experiment-detail-head">
        <div>
          <p class="section-kicker">experiment record</p>
          <h4>Research-style test log</h4>
        </div>
        ${outcomePill(record.outcome)}
      </div>
      <div class="experiment-metric-row">
        <div><span>Started</span><strong>${escapeHtml(formatMissionTime(record.started_at))}</strong></div>
        <div><span>Duration</span><strong>${escapeHtml(duration)}</strong></div>
        <div><span>Cmd/Err</span><strong>${escapeHtml(`${record.command_count || 0}/${record.error_count || 0}`)}</strong></div>
        <div><span>Skills</span><strong title="${escapeHtml(skills)}">${escapeHtml(compactText(skills || "-", 40))}</strong></div>
      </div>
      <form id="experiment-form" class="experiment-form" data-mission-id="${escapeHtml(mission.id)}">
        <div class="experiment-form-grid">
          <label>
            Challenge code
            <input name="challenge_code" type="text" value="${escapeHtml(record.challenge_code)}" placeholder="uuid / challenge id" />
          </label>
          <label>
            Difficulty
            <input name="difficulty" type="text" value="${escapeHtml(record.difficulty)}" placeholder="easy / medium / hard" />
          </label>
          <label>
            Outcome
            <select name="outcome">${renderOptionList(outcomeOptions, record.outcome)}</select>
          </label>
          <label>
            Failure reason
            <select name="failure_reason">${renderOptionList(FAILURE_REASON_LABELS, record.failure_reason)}</select>
          </label>
        </div>
        <label>
          Key parameters
          <textarea name="key_parameters" rows="3" placeholder="payload, credential, endpoint, flag path, important env">${escapeHtml(record.key_parameters)}</textarea>
        </label>
        <label>
          Notes / optimization
          <textarea name="notes" rows="4" placeholder="what failed, why it failed, next optimization idea">${escapeHtml(record.notes)}</textarea>
        </label>
        <div class="experiment-form-actions">
          <button id="experiment-save-btn" type="submit" class="secondary">Save experiment record</button>
          <p id="experiment-save-status" class="collab-status"></p>
        </div>
      </form>
    </section>
  `;
}

function bindExperimentForm(missionId) {
  const form = document.getElementById("experiment-form");
  const status = document.getElementById("experiment-save-status");
  const button = document.getElementById("experiment-save-btn");
  if (!form) return;
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const fd = new FormData(form);
    const payload = {
      challenge_code: fd.get("challenge_code"),
      difficulty: fd.get("difficulty"),
      outcome: fd.get("outcome"),
      failure_reason: fd.get("failure_reason"),
      key_parameters: fd.get("key_parameters"),
      notes: fd.get("notes"),
    };
    if (button) button.disabled = true;
    if (status) status.textContent = "Saving experiment record...";
    try {
      await fetchJson(`/api/missions/${missionId}/experiment`, {
        method: "PUT",
        body: JSON.stringify(payload),
      });
      state.lastDetailHash = "";
      state.lastExperimentsHash = "";
      if (status) status.textContent = "Saved.";
      await refreshAll();
    } catch (err) {
      if (status) status.textContent = `Save failed: ${err.message || err}`;
      if (button) button.disabled = false;
    }
  });
}

function renderMissionDetail(data) {
  const mission = data.mission;
  resumeBtnEl.disabled = !mission || ["running", "queued"].includes(mission.status) || Boolean(data.thread_alive);
  stopBtnEl.disabled = !mission || !["running", "queued"].includes(mission.status);
  deleteBtnEl.disabled = !mission || ["running", "queued"].includes(mission.status) || Boolean(data.thread_alive);

  if (!mission) {
    missionDetailEl.className = "mission-detail empty";
    missionDetailEl.innerHTML = `<div class="empty-state">未选择任务。点击左侧任务列表中的一条记录查看执行轨迹。</div>`;
    return;
  }

  const memory = data.memory || {};
  const rounds = data.rounds || [];
  const events = data.events || [];
  const guidanceItems = data.human_guidance || [];
  const guidanceDraft = document.getElementById("human-guidance-input")?.value || "";
  const experimentDraft = getExperimentDraft(mission.id);
  const experiment = data.experiment || null;
  const flowGroups = groupMissionFlow(rounds, events);
  state.flowGroupCount = flowGroups.length;
  const latestMain = rounds.filter((r) => r.worker_role === "main").at(-1);
  const memorySummary = displayMemorySummary(memory.summary);
  const nextFocus = memoryNextFocus(memory);
  const rawMission = JSON.stringify({ target: mission.target, goal: mission.goal, memory, error_message: mission.error_message, thread_alive: data.thread_alive }, null, 2);

  missionDetailEl.className = "mission-detail";
  missionDetailEl.innerHTML = `
    <section class="mission-hero">
      <div class="hero-left">
        <div class="hero-kicker">${escapeHtml(mission.id)}</div>
        <h3>${escapeHtml(mission.name)}</h3>
        <p class="hero-goal">${escapeHtml(mission.goal)}</p>
      </div>
      <div class="hero-right">
        <div class="stat-card">
          <div class="stat-label">状态</div>
          <div class="stat-value">${statusPill(mission.status)}</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">轮次</div>
          <div class="stat-value">R${escapeHtml(String(rounds.filter((r) => r.worker_role === "main").length).padStart(2, "0"))} / ${escapeHtml(mission.max_rounds)}</div>
          <div class="stat-foot">${data.thread_alive ? "worker alive" : "worker idle"}</div>
        </div>
        ${(mission.expected_flags || 1) > 1 ? `<div class="stat-card">
          <div class="stat-label">Flag</div>
          <div class="stat-value">🚩 ×${mission.expected_flags}</div>
        </div>` : ''}
        <div class="stat-card">
          <div class="stat-label">更新时间</div>
          <div class="stat-value stat-time">${escapeHtml(formatMissionTime(mission.updated_at))}</div>
          <div class="stat-foot">${escapeHtml(formatRelativeTime(mission.updated_at))}</div>
        </div>
      </div>
    </section>

    ${renderHumanCollabPanel(mission, guidanceItems, data.thread_alive, guidanceDraft)}

    ${renderExperimentPanel(mission, experiment, events, experimentDraft)}

    ${renderObserverMonitor(data.observer, events)}

    <section class="memory-dossier">
      <div class="memory-summary-row">
        <div class="memory-summary-content">
          <p class="section-kicker">summary</p>
          <h4>${escapeHtml(memorySummary.display)}</h4>
          ${memorySummary.truncated ? `<button class="expand-btn memory-expand-btn" onclick="this.previousElementSibling.textContent=this.dataset.full;this.remove()" data-full="${escapeHtml(memorySummary.full)}">展开全部 (${(memory.summary || "").length} chars)</button>` : ""}
        </div>
        <div class="memory-update">${escapeHtml(formatMissionTime(memory.updated_at || mission.updated_at))}</div>
      </div>
      <div class="memory-grid">
        ${renderMemoryColumn("findings", memory.findings, "No findings yet")}
        ${renderMemoryColumn("leads", memory.leads, "No leads yet")}
        ${renderMemoryColumn("credentials", memory.credentials, "No credentials yet")}
        ${renderMemoryColumn("dead_ends", memory.dead_ends, "No dead ends yet", "full-width")}
        ${renderMemoryColumn("next_focus", nextFocus, "No next focus yet", "full-width")}
      </div>

      <details class="trace-card raw-json-card" data-detail-key="mission:raw-json">
        <summary>
          <div class="trace-head">
            <span class="trace-type">RAW</span>
            <span class="trace-title">任务 JSON / 记忆快照</span>
          </div>
        </summary>
        <pre>${escapeHtml(rawMission)}</pre>
      </details>

      ${latestMain ? `<div class="latest-action">${monoChip(`latest: ${summarizeRound(latestMain)}`)}</div>` : ""}
      ${mission.error_message ? `<div class="error-banner">${escapeHtml(mission.error_message)}</div>` : ""}
    </section>

    <div class="section-band">
      <span>执行时间线</span>
      <span>${escapeHtml(flowGroups.length)} 组 · 按执行顺序从上到下</span>
    </div>
    ${flowGroups.length ? flowGroups.map((g, i) => renderFlowRound(g, i)).join("") : `<div class="empty-state">暂无轮次</div>`}
  `;
  restoreDetailOpenState();
  bindHumanCollabControls(mission.id);
  bindExperimentForm(mission.id);
  state.detailStateHydrated = true;
}

// ─── Data refresh ───

async function refreshMissions() {
  const data = await fetchJson("/api/missions");
  state.missions = data.missions || [];
  if (!state.selectedMissionId && state.missions.length) {
    state.selectedMissionId = state.missions[0].id;
  }
  renderMissions();
}

async function refreshExperiments() {
  const data = await fetchJson("/api/experiments");
  state.experiments = data.records || [];
  state.experimentSummary = data.summary || {};
  renderExperiments();
}

let _detailFetchSeq = 0;

async function refreshMissionDetail() {
  if (!state.selectedMissionId) {
    renderMissionDetail({ mission: null, rounds: [], events: [], memory: {} });
    return;
  }
  captureDetailOpenState();
  const seq = ++_detailFetchSeq;
  const targetId = state.selectedMissionId;
  const data = await fetchJson(`/api/missions/${targetId}`);
  // Discard stale response if user switched missions during fetch
  if (seq !== _detailFetchSeq || targetId !== state.selectedMissionId) return;
  // Skip re-render if data hasn't changed (preserves expanded content)
  const hash = JSON.stringify({
    s: data.mission?.status, u: data.mission?.updated_at,
    rc: data.rounds?.length, ec: data.events?.length,
    ta: data.thread_alive, ms: data.memory?.updated_at,
    hc: data.mission?.human_collab_enabled,
    hg: (data.human_guidance || []).map((g) => [g.id, g.status, g.consumed_at]).join("|"),
    ex: [
      data.experiment?.updated_at,
      data.experiment?.outcome,
      data.experiment?.failure_reason,
      data.experiment?.key_parameters,
      data.experiment?.notes,
    ].join("|"),
  });
  if (hash === state.lastDetailHash) return;
  state.lastDetailHash = hash;
  renderMissionDetail(data);
}

async function refreshAll() {
  try {
    await refreshMissions();
    await Promise.all([refreshExperiments(), refreshMissionDetail()]);
  } catch (err) {
    console.error(err);
  }
}

// ─── Bootstrap ───

async function bootstrap() {
  try {
    const data = await fetchJson("/api/bootstrap");
    state.bootstrapDefaults = data.defaults || null;
    applyFormDefaults(state.bootstrapDefaults);
  } catch (err) {
    console.error("bootstrap error:", err);
  }
  await refreshAll();
  if (state.pollTimer) clearInterval(state.pollTimer);
  state.pollTimer = setInterval(refreshAll, 3000);
}

// Cleanup polling on page unload
window.addEventListener("beforeunload", () => {
  if (state.pollTimer) clearInterval(state.pollTimer);
});

// ─── Form submit ───

missionFormEl.addEventListener("submit", async (event) => {
  event.preventDefault();
  formErrorEl.textContent = "";
  const fd = new FormData(missionFormEl);
  const payload = {
    name: fd.get("name"),
    target: fd.get("target"),
    goal: fd.get("goal"),
    max_rounds: Number(fd.get("max_rounds")),
    max_commands: Number(fd.get("max_commands")),
    command_timeout_sec: Number(fd.get("command_timeout_sec")),
    expected_flags: Number(fd.get("expected_flags") || 1),
  };
  try {
    const data = await fetchJson("/api/missions", {
      method: "POST",
      body: JSON.stringify(payload),
    });
    state.selectedMissionId = data.mission_id;
    missionFormEl.reset();
    applyFormDefaults(state.bootstrapDefaults);
    await refreshAll();
  } catch (err) {
    formErrorEl.textContent = String(err.message || err);
  }
});

// ─── Stop / Delete ───

resumeBtnEl.addEventListener("click", async () => {
  if (!state.selectedMissionId) return;
  resumeBtnEl.disabled = true;
  resumeBtnEl.textContent = "继续中...";
  formErrorEl.textContent = "";
  try {
    await fetchJson(`/api/missions/${state.selectedMissionId}/resume`, {
      method: "POST",
      body: JSON.stringify({}),
    });
  } catch (err) {
    formErrorEl.textContent = "继续任务失败: " + (err.message || err);
  } finally {
    state.lastDetailHash = "";
    await refreshAll();
    resumeBtnEl.textContent = "继续任务";
  }
});

stopBtnEl.addEventListener("click", async () => {
  if (!state.selectedMissionId) return;
  stopBtnEl.disabled = true;
  stopBtnEl.textContent = "停止中...";
  try {
    await fetchJson(`/api/missions/${state.selectedMissionId}/stop`, { method: "POST" });
  } catch (err) {
    formErrorEl.textContent = "停止任务失败: " + (err.message || err);
  }
  state.lastDetailHash = "";
  await refreshAll();
  stopBtnEl.textContent = "停止任务";
});

deleteBtnEl.addEventListener("click", async () => {
  if (!state.selectedMissionId) return;
  const mission = state.missions.find((m) => m.id === state.selectedMissionId);
  const label = mission?.name || state.selectedMissionId;
  if (!window.confirm(`确认删除任务记录：${label}？`)) return;
  try {
    await fetchJson(`/api/missions/${state.selectedMissionId}`, { method: "DELETE" });
  } catch (err) {
    formErrorEl.textContent = "删除失败: " + (err.message || err);
    return;
  }
  state.selectedMissionId = null;
  resetDetailViewState();
  await refreshAll();
});

// ─── Go ───
bootstrap();
