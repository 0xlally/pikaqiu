import type {
  Bootstrap,
  AgentSlot,
  Config,
  ConfigResponse,
  ConfigSaveResponse,
  ExperimentRecord,
  KnowledgeItem,
  Mission,
  MissionDetail,
  Skill,
  SkillStats
} from "./types";

export class ApiError extends Error {
  status: number;
  body: unknown;

  constructor(message: string, status: number, body: unknown) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.body = body;
  }
}

async function requestJson<T>(url: string, init: RequestInit = {}): Promise<T> {
  const response = await fetch(url, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(init.headers || {})
    }
  });
  const text = await response.text();
  let body: unknown = {};
  try {
    body = text ? JSON.parse(text) : {};
  } catch {
    body = text;
  }
  if (!response.ok) {
    const message =
      typeof body === "object" && body && "error" in body
        ? String((body as { error?: unknown }).error)
        : `HTTP ${response.status}`;
    throw new ApiError(message, response.status, body);
  }
  return body as T;
}

export const api = {
  bootstrap: () => requestJson<Bootstrap>("/api/bootstrap"),
  config: () => requestJson<ConfigResponse>("/api/config"),
  saveConfig: (config: Config) =>
    requestJson<ConfigSaveResponse>("/api/config", {
      method: "POST",
      body: JSON.stringify({ config })
    }),
  skills: () => requestJson<{ skills: Skill[]; stats: SkillStats }>("/api/skills"),
  experiments: () =>
    requestJson<{ records: ExperimentRecord[]; summary: Record<string, unknown> }>("/api/experiments"),
  missions: () => requestJson<{ missions: Mission[]; agent_slots?: AgentSlot[] }>("/api/missions"),
  createMission: (payload: Record<string, unknown>) =>
    requestJson<{ mission_id: string }>("/api/missions", {
      method: "POST",
      body: JSON.stringify(payload)
    }),
  missionDetail: (missionId: string) => requestJson<MissionDetail>(`/api/missions/${missionId}`),
  updateExperiment: (missionId: string, payload: Partial<ExperimentRecord>) =>
    requestJson<{ ok: boolean; experiment: ExperimentRecord }>(`/api/missions/${missionId}/experiment`, {
      method: "PUT",
      body: JSON.stringify(payload)
    }),
  setCollaboration: (missionId: string, enabled: boolean) =>
    requestJson<{ ok: boolean; enabled: boolean }>(`/api/missions/${missionId}/collaboration`, {
      method: "POST",
      body: JSON.stringify({ enabled })
    }),
  sendGuidance: (missionId: string, content: string) =>
    requestJson<{ ok: boolean }>(`/api/missions/${missionId}/guidance`, {
      method: "POST",
      body: JSON.stringify({ content })
    }),
  stopMission: (missionId: string) =>
    requestJson<{ ok: boolean }>(`/api/missions/${missionId}/stop`, { method: "POST" }),
  resumeMission: (missionId: string, extraRounds?: number) =>
    requestJson<{ ok: boolean }>(`/api/missions/${missionId}/resume`, {
      method: "POST",
      body: JSON.stringify(extraRounds ? { extra_rounds: extraRounds } : {})
    }),
  deleteMission: (missionId: string) =>
    requestJson<{ ok: boolean; deleted_id: string }>(`/api/missions/${missionId}`, { method: "DELETE" }),
  knowledgeSearch: (query: string, limit = 8) => {
    const params = new URLSearchParams({ q: query, limit: String(limit) });
    return requestJson<{ items: KnowledgeItem[] }>(`/api/knowledge/search?${params.toString()}`);
  },
  cveSearch: (query: { product?: string; version?: string; cve_id?: string; vuln_type?: string; keyword?: string }) => {
    const params = new URLSearchParams();
    Object.entries(query).forEach(([key, value]) => {
      if (value) params.set(key, value);
    });
    return requestJson<{ items: unknown[]; stats: Record<string, unknown> }>(
      `/api/knowledge/cve-search?${params.toString()}`
    );
  },
  reindexKnowledge: () =>
    requestJson<{ ok: boolean; knowledge: Record<string, unknown> }>("/api/knowledge/reindex", {
      method: "POST"
    })
};
