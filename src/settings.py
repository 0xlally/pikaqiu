from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ENV_PATH = PROJECT_ROOT / ".env"


def _read_env_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[7:].strip()
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip().lstrip("\ufeff")
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
            value = value[1:-1]
        values[key] = value
    return values


def _pick(raw: dict[str, str], key: str, default: str = "") -> str:
    value = raw.get(key)
    if value is None:
        value = os.environ.get(key, default)
    return value.strip()


@dataclass(slots=True)
class AppSettings:
    env_path: Path
    runtime_workspace_root: Path
    model: str
    base_url: str
    anthropic_api_key: str | None
    anthropic_auth_token: str | None


def load_settings(env_path: str | Path | None = None) -> AppSettings:
    path = Path(env_path) if env_path else DEFAULT_ENV_PATH
    raw = _read_env_file(path)

    workspace_root_raw = _pick(raw, "PIKAQIU_RUNTIME_WORKSPACE_ROOT")
    workspace_root = Path(workspace_root_raw) if workspace_root_raw else PROJECT_ROOT / ".runtime_workspaces"
    if not workspace_root.is_absolute():
        workspace_root = (PROJECT_ROOT / workspace_root).resolve()

    model = (
        _pick(raw, "ANTHROPIC_MODEL")
        or _pick(raw, "CLAUDE_AGENT_MODEL")
        or _pick(raw, "DEEPSEEK_MODEL", "deepseek-chat")
    )
    base_url = _pick(raw, "ANTHROPIC_BASE_URL") or _pick(raw, "DEEPSEEK_BASE_URL") or "https://api.anthropic.com"
    api_key = _pick(raw, "ANTHROPIC_API_KEY") or None
    auth_token = _pick(raw, "ANTHROPIC_AUTH_TOKEN") or _pick(raw, "DEEPSEEK_API_KEY") or None

    settings = AppSettings(
        env_path=path,
        runtime_workspace_root=workspace_root,
        model=model,
        base_url=base_url,
        anthropic_api_key=api_key,
        anthropic_auth_token=auth_token,
    )
    _validate_settings(settings)
    return settings


def _validate_settings(settings: AppSettings) -> None:
    if settings.base_url.rstrip("/").endswith("/chat/completions"):
        raise ValueError(
            "base_url 不能是原生 /chat/completions。"
            "请填写 Anthropic 兼容网关根地址（例如 https://api.deepseek.com/anthropic）。"
        )

    if not settings.model.strip():
        raise ValueError("缺少模型名，请在 .env 中设置 ANTHROPIC_MODEL 或 CLAUDE_AGENT_MODEL。")
    if settings.anthropic_api_key or settings.anthropic_auth_token:
        return
    raise ValueError("缺少认证信息，请在 .env 中设置 ANTHROPIC_AUTH_TOKEN 或 ANTHROPIC_API_KEY。")
