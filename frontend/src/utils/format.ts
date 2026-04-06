import type { JsonValue } from "../types/debug";

export function classNames(...values: Array<string | false | null | undefined>): string {
  return values.filter(Boolean).join(" ");
}

export function formatDateTime(value: string | null): string {
  if (!value) {
    return "-";
  }

  return new Intl.DateTimeFormat("zh-CN", {
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
  }).format(new Date(value));
}

export function formatDuration(value: number | null): string {
  if (value === null) {
    return "-";
  }

  if (value < 1000) {
    return `${value} ms`;
  }

  return `${(value / 1000).toFixed(2)} s`;
}

export function stringifyValue(value: unknown): string {
  if (typeof value === "string") {
    return value;
  }

  return JSON.stringify(value, null, 2);
}

export async function copyText(value: unknown): Promise<void> {
  const text = stringifyValue(value);
  await navigator.clipboard.writeText(text);
}

export function searchText(value: unknown): string {
  if (typeof value === "string") {
    return value.toLowerCase();
  }

  return JSON.stringify(value).toLowerCase();
}

export function truncateText(value: string, maxLength = 140): string {
  if (value.length <= maxLength) {
    return value;
  }

  return `${value.slice(0, maxLength - 1)}…`;
}

export function asJsonValue(value: JsonValue | string | null): JsonValue {
  if (value === null || typeof value !== "string") {
    return value as JsonValue;
  }

  return value;
}
