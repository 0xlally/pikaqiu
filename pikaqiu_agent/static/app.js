/* ========== PikaQiu Pentest Agent – Main App (Simplified) ========== */

const state = {
  missions: [],
  pollTimer: null,
  selectedMissionId: null,
  bootstrapDefaults: null,
  openDetailKeys: new Set(),
  expandedContentKeys: new Set(),
  detailStateHydrated: false,
  flowGroupCount: 0,
  lastDetailHash: "",
  lastMissionsHash: "",
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
  advisor_agent: "策略纠偏",
  error: "异常",
  flag: "🚩 Flag",
};

const ROLE_LABELS = { main: "主决策", memory: "记忆压缩", advisor: "策略纠偏" };
const ROLE_ORDER = { main: 1, memory: 2, advisor: 3 };

const BJ_TIME_FORMATTER = new Intl.DateTimeFormat("zh-CN", {
  timeZone: "Asia/Shanghai",
  year: "numeric", month: "2-digit", day: "2-digit",
  hour: "2-digit", minute: "2-digit", second: "2-digit",
  timeZoneName: "shortOffset", hour12: false,
});

const missionFormEl = document.getElementById("mission-form");
const formErrorEl = document.getElementById("form-error");
const missionsListEl = document.getElementById("missions-list");
const missionDetailEl = document.getElementById("mission-detail");
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
  if (!text) return { display: "尚未沉淀全局摘要", full: "", truncated: false };
  if (looksLikeTransportEnvelope(text)) return { display: "memory agent 本轮返回了运行回执而不是摘要，已判定为输出格式异常。", full: "", truncated: false };
  const limit = 220;
  if (text.length <= limit) return { display: text, full: text, truncated: false };
  return { display: text.slice(0, limit) + "…", full: text, truncated: true };
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

// ─── Chips / Pills ───

function statusPill(status) {
  return `<span class="status-pill status-${escapeHtml(status)}">${escapeHtml(STATUS_LABELS[status] || status)}</span>`;
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

// ─── Detail open/close state ───

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
  return compactText(d.advice || "advisor 已返回建议", 140);
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
      await refreshMissionDetail();
    });
  });
}

// ─── Render: Decision Brief ───

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
  const advisorRound = group.rounds.find((r) => r.worker_role === "advisor");
  const mainD = mainRound?.decision || {};
  const title = group.roundNo === 0
    ? "任务启动 / 知识库索引 / Sandbox 自检"
    : mainD.round_goal || summarizeRound(mainRound || memoryRound || advisorRound || {});
  const digest = group.roundNo === 0
    ? compactText(group.events.map((e) => e.title).join(" / "), 180)
    : compactText(mainD.thought_summary || memoryRound?.decision?.summary || advisorRound?.decision?.advice || "", 220);
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
          ${advisorRound ? renderDecisionBrief(advisorRound, "advisor", group.roundNo) : ""}
        </div>
      `}
      <div class="event-stack">
        ${group.events.length ? group.events.map((e) => renderEventCard(e)).join("") : `<div class="empty-state">这一轮暂无事件。</div>`}
      </div>
    </details>
  `;
}

// ─── Render: Mission Detail ───

function renderMissionDetail(data) {
  const mission = data.mission;
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
  const flowGroups = groupMissionFlow(rounds, events);
  state.flowGroupCount = flowGroups.length;
  const latestMain = rounds.filter((r) => r.worker_role === "main").at(-1);
  const memorySummary = displayMemorySummary(memory.summary);
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

    <section class="memory-dossier">
      <div class="memory-summary-row">
        <div class="memory-summary-content">
          <p class="section-kicker">全局记忆</p>
          <h4>${escapeHtml(memorySummary.display)}</h4>
          ${memorySummary.truncated ? `<button class="expand-btn memory-expand-btn" onclick="this.previousElementSibling.textContent=this.dataset.full;this.remove()" data-full="${escapeHtml(memorySummary.full)}">展开全部 (${(memory.summary || "").length} chars)</button>` : ""}
        </div>
        <div class="memory-update">${escapeHtml(formatMissionTime(memory.updated_at || mission.updated_at))}</div>
      </div>
      <div class="memory-grid">
        <div class="memory-column">
          <div class="kv-title">已确认发现</div>
          ${renderChipRail(memory.findings, "暂无确认发现")}
        </div>
        <div class="memory-column">
          <div class="kv-title">待验证线索</div>
          ${renderChipRail(memory.leads, "暂无待验证线索")}
        </div>
        <div class="memory-column">
          <div class="kv-title">凭据</div>
          ${renderChipRail(memory.credentials, "暂无凭据")}
        </div>
      </div>
      <div class="memory-column full-width">
        <div class="kv-title">死胡同 / 下步方向</div>
        ${renderChipRail([...(memory.dead_ends || []), ...(memory.next_focus || [])], "暂无阻塞项")}
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
  });
  if (hash === state.lastDetailHash) return;
  state.lastDetailHash = hash;
  renderMissionDetail(data);
}

async function refreshAll() {
  try {
    await Promise.all([refreshMissions(), refreshMissionDetail()]);
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
