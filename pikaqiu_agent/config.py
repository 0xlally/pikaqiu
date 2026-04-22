from __future__ import annotations

import logging
import os
import threading
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# Load .env file if present (backward compatibility)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    _env_file = Path.cwd() / ".env"
    if _env_file.is_file():
        for _line in _env_file.read_text(encoding="utf-8").splitlines():
            _line = _line.strip()
            if not _line or _line.startswith("#"):
                continue
            if "=" in _line:
                _k, _, _v = _line.partition("=")
                _k, _v = _k.strip(), _v.strip()
                if _k and _k not in os.environ:
                    os.environ[_k] = _v

logger = logging.getLogger(__name__)

DEFAULT_LLM_BASE_URL = "http://10.50.1.215:8080/v1"
DEFAULT_LLM_API_KEY = ""
DEFAULT_LLM_MODEL = "minimax-m2.7"


# ── Model Pool Entry ──────────────────────────────────────────────

@dataclass
class ModelPoolEntry:
    """One LLM configuration in the model pool."""
    id: str
    base_url: str
    api_key: str
    model: str
    thinking: bool = False
    priority: int = 1
    max_concurrent: int = 3
    _active_count: int = field(default=0, init=False, repr=False)
    _pool_lock: threading.Lock = field(default_factory=threading.Lock, init=False, repr=False)

    @property
    def available(self) -> bool:
        return self._active_count < self.max_concurrent

    def acquire(self) -> bool:
        with self._pool_lock:
            if self._active_count < self.max_concurrent:
                self._active_count += 1
                return True
            return False

    def release(self) -> None:
        with self._pool_lock:
            self._active_count = max(0, self._active_count - 1)


# ── Difficulty Params─────────────────────────────────────────────

@dataclass
class DifficultyParams:
    """Per-difficulty initial and ceiling params."""
    initial_rounds: int = 4
    initial_commands: int = 64
    max_rounds: int = 16
    max_commands: int = 400


@dataclass
class MultiFlagScaling:
    """Extra resources per additional flag beyond the first."""
    extra_rounds_per_flag: int = 3
    extra_commands_per_flag: int = 12


# Fields that the WebUI may read/write at runtime
_RUNTIME_MUTABLE_FIELDS = {
    # LLM
    "llm_base_url", "llm_api_key", "llm_model", "llm_chat_model", "llm_thinking", "llm_timeout_sec",
    # Advisor
    "advisor_base_url", "advisor_api_key", "advisor_model", "advisor_thinking",
    # Agent params
    "initial_rounds", "initial_commands", "max_rounds", "max_commands",
    "command_timeout_sec", "stdout_limit", "knowledge_top_k",
    "context_compress_threshold",
    "extra_rounds_per_flag", "extra_commands_per_flag",
    # Mock
    "mock",
}

# Sensitive fields: shown as masked in API responses
_SENSITIVE_FIELDS = {"llm_api_key", "advisor_api_key"}


@dataclass
class AgentSettings:
    workspace_root: Path
    db_path: Path
    sandbox_container: str
    sandbox_workdir: str
    sandbox_containers: list[str] | None = None  # multi-sandbox pool; if set, overrides sandbox_container
    sandbox_public_ip: str = ""  # Public IP for reverse shell listeners
    # Main LLM (used by main agent + memory agent)
    llm_base_url: str = DEFAULT_LLM_BASE_URL
    llm_api_key: str = ""
    llm_model: str = DEFAULT_LLM_MODEL
    llm_chat_model: str = ""   # override tool-calling model; if empty, uses llm_model
    llm_thinking: bool = False  # deepseek-chat with thinking enabled via extra_body
    llm_timeout_sec: int = 240
    llm_max_retries: int = 10  # LLM timeout/error auto-retry count
    # Compression LLM (cheap model for context compression; falls back to main LLM if empty)
    compression_base_url: str = ""
    compression_api_key: str = ""
    compression_model: str = ""
    compression_timeout_sec: int = 60
    # Advisor LLM (falls back to main LLM if empty)
    advisor_base_url: str = ""
    advisor_api_key: str = ""
    advisor_model: str = ""
    advisor_thinking: bool = False   # Qwen3 supports enable_thinking=false; disable for speed
    # Agent params — "initial" for first attempt, "max" as ceiling for retries
    initial_rounds: int = 4
    initial_commands: int = 64
    command_timeout_sec: int = 60      # default sandbox command timeout
    stdout_limit: int = 8000
    context_compress_threshold: int = 80000  # chars; mid-round context compression trigger
    round_timeout_sec: int = 300
    knowledge_top_k: int = 6
    knowledge_dir: str = "./knowledge"  # directory for knowledge zips/folders
    max_rounds: int = 16
    max_commands: int = 400
    max_retries: int = 2  # number of retry attempts for failed missions
    mission_timeout_sec: int = 0  # total mission timeout in seconds (0 = no limit)
    # Per-difficulty params (overrides initial/max above)
    difficulty_params: dict[str, DifficultyParams] = field(default_factory=dict)
    # Web
    host: str = "127.0.0.1"
    port: int = 8765
    # Mock mode
    mock: bool = False
    # Model pool (populated from config.yml)
    model_pool: list[ModelPoolEntry] = field(default_factory=list)
    multi_flag_scaling: MultiFlagScaling = field(default_factory=MultiFlagScaling)
    disable_memory_cleaning: bool = False  # skip memory cleaning on stall (keep all confirmed findings)

    # Thread-safe lock for runtime updates
    _lock: threading.Lock = field(default_factory=threading.Lock, init=False, repr=False)

    @property
    def use_mock_llm(self) -> bool:
        if self.mock:
            return True
        return not self.llm_api_key

    def get_difficulty_params(self, difficulty: str) -> DifficultyParams:
        """Get params for a specific difficulty, falling back to global defaults."""
        dp = self.difficulty_params.get(difficulty.lower())
        if dp:
            return dp
        return DifficultyParams(
            initial_rounds=self.initial_rounds,
            initial_commands=self.initial_commands,
            max_rounds=self.max_rounds,
            max_commands=self.max_commands,
        )

    def get_advisor_base_url(self) -> str:
        return self.advisor_base_url or self.llm_base_url

    def get_chat_model(self) -> str:
        """Non-thinking model name for tool calling. Returns llm_chat_model if set, else llm_model.
        deepseek-reasoner now supports tool calling (as of 2025 API update), so no forced fallback."""
        return self.llm_chat_model or self.llm_model

    def get_advisor_api_key(self) -> str:
        return self.advisor_api_key or self.llm_api_key

    def get_advisor_model(self) -> str:
        return self.advisor_model or self.llm_model

    def get_model_by_id(self, model_id: str) -> ModelPoolEntry | None:
        """Get a model pool entry by ID."""
        for m in self.model_pool:
            if m.id == model_id:
                return m
        return None

    def get_model_by_model_name(self, model_name: str) -> ModelPoolEntry | None:
        """Get a model pool entry by its model name (e.g. 'deepseek-reasoner')."""
        for m in self.model_pool:
            if m.model == model_name:
                return m
        return None

    def get_available_models(self, count: int = 1) -> list[ModelPoolEntry]:
        """Get available models sorted by priority. Returns up to `count` models."""
        available = [m for m in sorted(self.model_pool, key=lambda m: m.priority) if m.available]
        return available[:count]

    # ── Runtime update (thread-safe) ──────────────────────────────────

    def update(self, changes: dict[str, Any]) -> dict[str, str]:
        """Apply runtime config changes. Returns dict of field→error for bad values."""
        errors: dict[str, str] = {}
        with self._lock:
            for key, value in changes.items():
                if key not in _RUNTIME_MUTABLE_FIELDS:
                    errors[key] = f"field '{key}' is not runtime-mutable"
                    continue
                if not hasattr(self, key):
                    errors[key] = f"unknown field '{key}'"
                    continue
                current = getattr(self, key)
                try:
                    if isinstance(current, bool):
                        coerced = value if isinstance(value, bool) else str(value).lower() not in {"0", "false", "no", "off", ""}
                    elif isinstance(current, int):
                        coerced = int(value)
                    elif isinstance(current, str):
                        coerced = str(value)
                    else:
                        coerced = value
                    setattr(self, key, coerced)
                except (ValueError, TypeError) as e:
                    errors[key] = f"invalid value for '{key}': {e}"
        if changes and not errors:
            logger.info("Config updated: %s", {k: ("***" if k in _SENSITIVE_FIELDS else v) for k, v in changes.items()})
        return errors

    # ── Serialization ─────────────────────────────────────────────────

    def to_dict(self, mask_secrets: bool = True) -> dict[str, Any]:
        """Export settings as a JSON-safe dict."""
        d: dict[str, Any] = {}
        for key in _RUNTIME_MUTABLE_FIELDS:
            val = getattr(self, key, None)
            if mask_secrets and key in _SENSITIVE_FIELDS and val:
                d[key] = val[:8] + "***" if len(val) > 8 else "***"
            else:
                d[key] = val
        # Add read-only computed fields
        d["use_mock_llm"] = self.use_mock_llm
        d["effective_advisor_model"] = self.get_advisor_model()
        d["effective_chat_model"] = self.get_chat_model()
        return d

    def get_mission_params(self, overrides: dict[str, Any] | None = None) -> dict[str, int]:
        """Get mission execution parameters, optionally overridden per-mission."""
        params = {
            "max_rounds": self.initial_rounds,
            "max_commands": self.initial_commands,
            "command_timeout_sec": self.command_timeout_sec,
        }
        if overrides:
            for key in params:
                if key in overrides:
                    try:
                        params[key] = int(overrides[key])
                    except (ValueError, TypeError):
                        pass
        return params


def _env_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if not value:
        return default
    try:
        return int(value)
    except ValueError:
        return default


def _env_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() not in {"0", "false", "no", "off", ""}


def _env_str(name: str, *fallback_names: str, default: str = "") -> str:
    """Read env var, with fallback names for backward compatibility."""
    for n in (name, *fallback_names):
        v = os.getenv(n)
        if v and v.strip():
            return v.strip()
    return default


def load_settings(workspace_root: Path | None = None) -> AgentSettings:
    root = workspace_root or Path.cwd()

    # Try loading config.yml first, fall back to .env
    yml_path = root / "config.yml"
    if yml_path.is_file():
        return _load_from_yaml(root, yml_path)

    return _load_from_env(root)


def _load_from_env(root: Path) -> AgentSettings:
    """Legacy .env-based loading."""
    base_url = _env_str("PIKAQIU_LLM_BASE_URL", "PIKAQIU_ANTHROPIC_BASE_URL", default=DEFAULT_LLM_BASE_URL)
    if base_url.endswith("/anthropic"):
        base_url = base_url[:-len("/anthropic")]

    return AgentSettings(
        workspace_root=root.resolve(),
        db_path=(root / ".pikaqiu_agent" / "state.sqlite3").resolve(),
        sandbox_container=_env_str("PIKAQIU_SANDBOX_CONTAINER", default="pikaqiu-sandbox-1"),
        sandbox_workdir=_env_str("PIKAQIU_SANDBOX_WORKDIR", default="/tmp/pikaqiu-agent-workspace"),
        llm_base_url=base_url,
        llm_api_key=_env_str("PIKAQIU_LLM_API_KEY", "PIKAQIU_ANTHROPIC_AUTH_TOKEN", default=DEFAULT_LLM_API_KEY),
        llm_model=_env_str("PIKAQIU_LLM_MODEL", "PIKAQIU_ANTHROPIC_MODEL", default=DEFAULT_LLM_MODEL),
        llm_chat_model=_env_str("PIKAQIU_LLM_CHAT_MODEL", default=""),
        llm_thinking=_env_bool("PIKAQIU_LLM_THINKING", default=False),
        llm_timeout_sec=_env_int("PIKAQIU_LLM_TIMEOUT_SEC", _env_int("PIKAQIU_CLAUDE_TIMEOUT_SEC", 60)),
        llm_max_retries=_env_int("PIKAQIU_LLM_MAX_RETRIES", 10),
        advisor_base_url=_env_str("PIKAQIU_ADVISOR_BASE_URL", default=""),
        advisor_api_key=_env_str("PIKAQIU_ADVISOR_API_KEY", default=""),
        advisor_model=_env_str("PIKAQIU_ADVISOR_MODEL", default=""),
        advisor_thinking=_env_bool("PIKAQIU_ADVISOR_THINKING", default=False),
        initial_rounds=_env_int("PIKAQIU_MAX_ROUNDS", 8),
        initial_commands=_env_int("PIKAQIU_MAX_COMMANDS_PER_ROUND", 32),
        command_timeout_sec=_env_int("PIKAQIU_COMMAND_TIMEOUT_SEC", 60),
        stdout_limit=_env_int("PIKAQIU_STDOUT_LIMIT", 16000),
        knowledge_top_k=_env_int("PIKAQIU_KNOWLEDGE_TOP_K", 6),
        knowledge_dir=_env_str("PIKAQIU_KNOWLEDGE_DIR", default="./knowledge"),
        host=_env_str("PIKAQIU_WEB_HOST", default="127.0.0.1"),
        port=_env_int("PIKAQIU_WEB_PORT", 8765),
        mock=_env_bool("PIKAQIU_MOCK", False),
    )


def _parse_difficulty_params(raw: dict) -> dict[str, DifficultyParams]:
    """Parse difficulty_params section from config.yml."""
    result: dict[str, DifficultyParams] = {}
    for diff_name, vals in raw.items():
        if isinstance(vals, dict):
            result[diff_name.lower()] = DifficultyParams(
                initial_rounds=vals.get("initial_rounds", 4),
                initial_commands=vals.get("initial_commands", 64),
                max_rounds=vals.get("max_rounds", 16),
                max_commands=vals.get("max_commands", 400),
            )
    return result


def _load_from_yaml(root: Path, yml_path: Path) -> AgentSettings:
    """Load settings from config.yml (preferred)."""
    try:
        import yaml
    except ImportError:
        logger.warning("PyYAML not installed, falling back to .env")
        return _load_from_env(root)

    with open(yml_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f) or {}

    # Parse model pool
    model_pool: list[ModelPoolEntry] = []
    for entry in cfg.get("model_pool", []):
        model_pool.append(ModelPoolEntry(
            id=entry.get("id", f"model-{len(model_pool)}"),
            base_url=entry.get("base_url", DEFAULT_LLM_BASE_URL),
            api_key=entry.get("api_key", ""),
            model=entry.get("model", DEFAULT_LLM_MODEL),
            thinking=entry.get("thinking", False),
            priority=entry.get("priority", len(model_pool) + 1),
            max_concurrent=entry.get("max_concurrent", 3),
        ))

    # Primary model = first in pool (highest priority) or env fallback.
    # Environment values intentionally override config.yml so secrets can stay in .env.
    primary = model_pool[0] if model_pool else None
    base_default = primary.base_url if primary else DEFAULT_LLM_BASE_URL
    key_default = primary.api_key if primary else DEFAULT_LLM_API_KEY
    model_default = primary.model if primary else DEFAULT_LLM_MODEL
    thinking_default = primary.thinking if primary else False
    llm_base_url = _env_str("PIKAQIU_LLM_BASE_URL", default=base_default)
    llm_api_key = _env_str("PIKAQIU_LLM_API_KEY", default=key_default)
    llm_model = _env_str("PIKAQIU_LLM_MODEL", default=model_default)
    llm_thinking = _env_bool("PIKAQIU_LLM_THINKING", default=thinking_default)
    if primary:
        primary.base_url = llm_base_url
        primary.api_key = llm_api_key
        primary.model = llm_model
        primary.thinking = llm_thinking

    # Advisor
    adv = cfg.get("advisor", {})
    # Agent defaults
    ag = cfg.get("agent_defaults", {})
    # Sandbox
    sb = cfg.get("sandbox", {})
    # Web
    web = cfg.get("web", {})

    # Multi-sandbox pool: prefer "containers" list, fallback to single "container"
    _sb_containers_raw = sb.get("containers", [])
    _sb_default = sb.get("container", "pikaqiu-sandbox-1")
    _sb_containers = _sb_containers_raw if _sb_containers_raw else None

    settings = AgentSettings(
        workspace_root=root.resolve(),
        db_path=(root / ".pikaqiu_agent" / "state.sqlite3").resolve(),
        sandbox_container=_sb_containers[0] if _sb_containers else _sb_default,
        sandbox_workdir=sb.get("workdir", "/tmp/pikaqiu-agent-workspace"),
        sandbox_containers=_sb_containers,
        sandbox_public_ip=sb.get("public_ip", ""),
        llm_base_url=llm_base_url,
        llm_api_key=llm_api_key,
        llm_model=llm_model,
        llm_chat_model="",
        llm_thinking=llm_thinking,
        llm_timeout_sec=ag.get("llm_timeout_sec", 240),
        llm_max_retries=ag.get("llm_max_retries", 10),
        compression_base_url=cfg.get("compression", {}).get("base_url", ""),
        compression_api_key=cfg.get("compression", {}).get("api_key", ""),
        compression_model=cfg.get("compression", {}).get("model", ""),
        compression_timeout_sec=cfg.get("compression", {}).get("timeout_sec", 60),
        advisor_base_url=adv.get("base_url", ""),
        advisor_api_key=adv.get("api_key", ""),
        advisor_model=adv.get("model", ""),
        advisor_thinking=adv.get("thinking", False),
        initial_rounds=ag.get("initial_rounds", ag.get("max_rounds", 8)),
        initial_commands=ag.get("initial_commands", ag.get("max_commands_per_round", 32)),
        command_timeout_sec=ag.get("command_timeout_sec", 60),
        stdout_limit=ag.get("stdout_limit", 8000),
        context_compress_threshold=ag.get("context_compress_threshold", 80000),
        round_timeout_sec=ag.get("round_timeout_sec", 300),
        knowledge_top_k=ag.get("knowledge_top_k", 6),
        knowledge_dir=ag.get("knowledge_dir", "./knowledge"),
        max_rounds=ag.get("max_rounds_ceiling", ag.get("retry_max_rounds", 16)),
        max_commands=ag.get("max_commands_ceiling", ag.get("retry_max_commands_per_round", 128)),
        max_retries=ag.get("max_retries", 2),
        mission_timeout_sec=ag.get("mission_timeout_sec", 0),
        difficulty_params=_parse_difficulty_params(ag.get("difficulty_params", {})),
        multi_flag_scaling=MultiFlagScaling(
            extra_rounds_per_flag=ag.get("multi_flag_scaling", {}).get("extra_rounds_per_flag", 3),
            extra_commands_per_flag=ag.get("multi_flag_scaling", {}).get("extra_commands_per_flag", 12),
        ),
        host=web.get("host", "127.0.0.1"),
        port=web.get("port", 8765),
        mock=False,
        model_pool=model_pool,
        disable_memory_cleaning=ag.get("disable_memory_cleaning", False),
    )

    logger.info("Loaded config from %s: %d models in pool",
                yml_path, len(model_pool))
    return settings
