import type { Event, Mission, Round } from "./types";

const timeFormatter = new Intl.DateTimeFormat("zh-CN", {
  timeZone: "Asia/Shanghai",
  month: "2-digit",
  day: "2-digit",
  hour: "2-digit",
  minute: "2-digit",
  second: "2-digit",
  hour12: false
});

export function formatTime(value?: string | null): string {
  if (!value) return "未记录";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;
  return timeFormatter.format(date);
}

export function relativeTime(value?: string | null): string {
  if (!value) return "无时间戳";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;
  const diff = Date.now() - date.getTime();
  const abs = Math.abs(diff);
  const mins = Math.round(abs / 60000);
  if (mins < 1) return diff >= 0 ? "刚刚" : "即将";
  if (mins < 60) return `${mins} 分钟${diff >= 0 ? "前" : "后"}`;
  const hours = Math.round(mins / 60);
  if (hours < 24) return `${hours} 小时${diff >= 0 ? "前" : "后"}`;
  const days = Math.round(hours / 24);
  return `${days} 天${diff >= 0 ? "前" : "后"}`;
}

export function compact(value: unknown, limit = 180): string {
  const text = toText(value).replace(/\s+/g, " ").trim();
  return text.length > limit ? `${text.slice(0, limit - 1)}…` : text;
}

export function toText(value: unknown): string {
  if (value === null || value === undefined) return "";
  if (typeof value === "string") return value;
  if (typeof value === "number" || typeof value === "boolean") return String(value);
  try {
    return JSON.stringify(value, null, 2);
  } catch {
    return String(value);
  }
}

export function listify(value: unknown): string[] {
  if (!value) return [];
  if (Array.isArray(value)) return value.map((item) => compact(item, 240)).filter(Boolean);
  if (typeof value === "object") {
    return Object.entries(value as Record<string, unknown>).map(([key, item]) => `${key}: ${compact(item, 180)}`);
  }
  return [String(value)];
}

export function isActiveMission(mission?: Mission | null, threadAlive = false): boolean {
  if (!mission) return false;
  return mission.status === "queued" || mission.status === "running" || threadAlive;
}

export function statusTone(status: string): "idle" | "live" | "ok" | "warn" | "bad" {
  if (status === "running" || status === "queued") return "live";
  if (status === "done") return "ok";
  if (status === "stopped" || status === "timeout") return "warn";
  if (status === "error") return "bad";
  return "idle";
}

export function eventTone(type: string): string {
  if (type === "flag") return "flag";
  if (type === "error") return "bad";
  if (type === "command" || type === "command_running") return "command";
  if (type === "observer_agent") return "observer";
  if (type === "human_guidance") return "human";
  if (type === "knowledge") return "knowledge";
  return "system";
}

export function eventLabel(type: string): string {
  const labels: Record<string, string> = {
    system: "系统",
    command: "命令",
    command_running: "运行中",
    knowledge: "知识库",
    sandbox: "沙箱",
    main_agent: "主 Agent",
    memory_agent: "记忆",
    observer_agent: "Observer",
    human_guidance: "人工介入",
    error: "错误",
    flag: "Flag"
  };
  return labels[type] || type;
}

export function groupFlow(rounds: Round[], events: Event[]) {
  const keys = new Set<number>();
  rounds.forEach((round) => keys.add(round.round_no));
  events.forEach((event) => keys.add(event.round_no));
  return Array.from(keys)
    .sort((a, b) => a - b)
    .map((roundNo) => ({
      roundNo,
      rounds: rounds.filter((round) => round.round_no === roundNo),
      events: events.filter((event) => event.round_no === roundNo)
    }));
}

export function percentage(value: number, total: number): number {
  if (!total) return 0;
  return Math.max(0, Math.min(100, Math.round((value / total) * 100)));
}

export function safeJson(value: unknown): string {
  try {
    return JSON.stringify(value, null, 2);
  } catch {
    return String(value);
  }
}
