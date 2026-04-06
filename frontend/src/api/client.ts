import type { RunSummary } from "../types/debug";

export interface RunListItem {
  runId: string;
  goal: string;
  status: "running" | "completed" | "failed";
  updatedAt: string;
  currentStage: string;
}

interface CreateRunRequest {
  featureDescription: string;
  mappingPath?: string;
}

async function requestJson<T>(url: string, init?: RequestInit): Promise<T> {
  const response = await fetch(url, {
    ...init,
    headers: {
      "content-type": "application/json",
      ...(init?.headers ?? {}),
    },
  });

  if (!response.ok) {
    const body = await response.text();
    throw new Error(body || `请求失败: ${response.status}`);
  }

  return response.json() as Promise<T>;
}

export async function createRun(featureDescription: string, mappingPath?: string): Promise<RunSummary> {
  const payload: CreateRunRequest = { featureDescription };
  if (mappingPath) {
    payload.mappingPath = mappingPath;
  }

  return requestJson<RunSummary>("/api/runs", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function getLatestRun(): Promise<RunSummary | null> {
  const response = await fetch("/api/runs/latest");
  if (response.status === 404) {
    return null;
  }
  if (!response.ok) {
    const body = await response.text();
    throw new Error(body || `请求失败: ${response.status}`);
  }
  return response.json() as Promise<RunSummary>;
}

export async function listRuns(): Promise<RunListItem[]> {
  return requestJson<RunListItem[]>("/api/runs", { method: "GET" });
}

export async function getRunById(runId: string): Promise<RunSummary> {
  return requestJson<RunSummary>(`/api/runs/${encodeURIComponent(runId)}`, { method: "GET" });
}
