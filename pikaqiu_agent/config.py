from __future__ import annotations

import logging
import os
import threading
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# Load .env file if present (backward compatibility)
_ENV_FILE = Path(__file__).resolve().parent.parent / ".env"
try:
    from dotenv import load_dotenv
    load_dotenv(_ENV_FILE if _ENV_FILE.is_file() else None)
except ImportError:
    for _env_file in (_ENV_FILE, Path.cwd() / ".env"):
        if not _env_file.is_file():
            continue
        for _line in _env_file.read_text(encoding="utf-8").splitlines():
            _line = _line.strip()
            if not _line or _line.startswith("#"):
                continue
            if "=" in _line:
                _k, _, _v = _line.partition("=")
                _k, _v = _k.strip(), _v.strip()
                if _k and _k not in os.environ:
                    os.environ[_k] = _v
        break

logger = logging.getLogger(__name__)

DEFAULT_LLM_BASE_URL = "https://www.inroi.shop"
DEFAULT_LLM_API_KEY = ""
DEFAULT_LLM_MODEL = "gpt-5.5"
DEFAULT_LLM_REASONING_EFFORT = "xhigh"
DEFAULT_COMPRESSION_MODEL = DEFAULT_LLM_MODEL
DEFAULT_COMPRESSION_REASONING_EFFORT = "low"
DEFAULT_COMPRESSION_TIMEOUT_SEC = 180
_ALLOWED_COMPRESSION_REASONING_EFFORTS = {"minimal", "low", "medium"}
DEFAULT_MEMORY_COMPRESS_INTERVAL = 8
COMMAND_TIMEOUT_MAX_SEC = 300
MAX_AGENT_SLOTS = 5
DEFAULT_SANDBOX_CONTAINERS = tuple(f"pikaqiu-sandbox-{idx}" for idx in range(1, MAX_AGENT_SLOTS + 1))


def _clamp_command_timeout(value: Any, default: int = COMMAND_TIMEOUT_MAX_SEC) -> int:
    try:
        timeout = int(value)
    except (ValueError, TypeError):
        timeout = int(default)
    return max(1, min(timeout, COMMAND_TIMEOUT_MAX_SEC))


# ── Model Pool Entry ──────────────────────────────────────────────

@dataclass
class ModelPoolEntry:
    """One LLM configuration in the model pool."""
    id: str
    base_url: str
    api_key: str
    model: str
    thinking: bool = False
    reasoning_effort: str = DEFAULT_LLM_REASONING_EFFORT
    use_responses_api: bool = True
    disable_response_storage: bool = True
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
    "llm_reasoning_effort", "llm_use_responses_api", "llm_disable_response_storage",
    # Passive Observer
    "observer_base_url", "observer_api_key", "observer_model", "observer_thinking",
    "observer_reasoning_effort", "observer_use_responses_api", "observer_disable_response_storage",
    # Mid-round context compression
    "compression_base_url", "compression_api_key", "compression_model",
    "compression_reasoning_effort", "compression_use_responses_api",
    "compression_disable_response_storage", "compression_timeout_sec",
    # Agent params
    "initial_rounds", "initial_commands", "max_rounds", "max_commands",
    "command_timeout_sec", "stdout_limit", "knowledge_top_k", "skills_dir",
    "skills_auto_use", "skill_catalog_limit", "skill_prompt_max_chars", "skill_reference_max_chars",
    "context_compress_threshold", "memory_compress_interval",
    "disable_memory_rebase",
    "extra_rounds_per_flag", "extra_commands_per_flag",
    # Mock
    "mock",
}

# Sensitive fields: shown as masked in API responses
_SENSITIVE_FIELDS = {"llm_api_key", "observer_api_key", "compression_api_key"}


@dataclass
class AgentSettings:
    workspace_root: Path
    db_path: Path
    sandbox_container: str
    sandbox_workdir: str
    sandbox_containers: list[str] = field(default_factory=lambda: list(DEFAULT_SANDBOX_CONTAINERS))
    sandbox_public_ip: str = ""  # Public IP for reverse shell listeners
    # Main LLM (used by main agent + memory agent)
    llm_base_url: str = DEFAULT_LLM_BASE_URL
    llm_api_key: str = ""
    llm_model: str = DEFAULT_LLM_MODEL
    llm_chat_model: str = ""   # override tool-calling model; if empty, uses llm_model
    llm_thinking: bool = False  # deepseek-chat with thinking enabled via extra_body
    llm_reasoning_effort: str = DEFAULT_LLM_REASONING_EFFORT
    llm_use_responses_api: bool = True
    llm_disable_response_storage: bool = True
    llm_timeout_sec: int = 240
    llm_max_retries: int = 10  # LLM timeout/error auto-retry count
    # Compression LLM (semantic mid-round context compression)
    compression_base_url: str = ""
    compression_api_key: str = ""
    compression_model: str = DEFAULT_COMPRESSION_MODEL
    compression_reasoning_effort: str = DEFAULT_COMPRESSION_REASONING_EFFORT
    compression_use_responses_api: bool = True
    compression_disable_response_storage: bool = True
    compression_timeout_sec: int = DEFAULT_COMPRESSION_TIMEOUT_SEC
    # Passive Observer LLM (falls back to main LLM if empty)
    observer_base_url: str = ""
    observer_api_key: str = ""
    observer_model: str = ""
    observer_thinking: bool = False   # Qwen3 supports enable_thinking=false; disable for speed
    observer_reasoning_effort: str = DEFAULT_LLM_REASONING_EFFORT
    observer_use_responses_api: bool = True
    observer_disable_response_storage: bool = True
    # Agent params — "initial" for first attempt, "max" as ceiling for retries
    initial_rounds: int = 4
    initial_commands: int = 64
    command_timeout_sec: int = 300     # default sandbox command timeout
    stdout_limit: int = 8000
    context_compress_threshold: int = 80000  # chars; mid-round context compression trigger
    memory_compress_interval: int = DEFAULT_MEMORY_COMPRESS_INTERVAL  # main LLM calls between structured memory compression runs
    knowledge_top_k: int = 6
    knowledge_dir: str = "./knowledge"  # directory for knowledge zips/folders
    skills_dir: str = "./skills"  # directory containing */SKILL.md skill folders
    skills_auto_use: bool = True
    skill_catalog_limit: int = 50
    skill_prompt_max_chars: int = 12000
    skill_reference_max_chars: int = 20000
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
    disable_memory_rebase: bool = False  # skip MemoryAgent rebase on stall

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

    def get_observer_base_url(self) -> str:
        return self.observer_base_url or self.llm_base_url

    def get_chat_model(self) -> str:
        """Non-thinking model name for tool calling. Returns llm_chat_model if set, else llm_model.
        deepseek-reasoner now supports tool calling (as of 2025 API update), so no forced fallback."""
        return self.llm_chat_model or self.llm_model

    def get_observer_api_key(self) -> str:
        return self.observer_api_key or self.llm_api_key

    def get_observer_model(self) -> str:
        return self.observer_model or self.llm_model

    def get_compression_base_url(self) -> str:
        return self.compression_base_url or self.llm_base_url

    def get_compression_api_key(self) -> str:
        return self.compression_api_key or self.llm_api_key

    def get_compression_model(self) -> str:
        return self.compression_model or DEFAULT_COMPRESSION_MODEL

    def get_compression_reasoning_effort(self) -> str:
        return _normalize_compression_reasoning_effort(self.compression_reasoning_effort)

    def get_compression_timeout_sec(self) -> int:
        try:
            timeout = int(self.compression_timeout_sec)
        except (TypeError, ValueError):
            timeout = DEFAULT_COMPRESSION_TIMEOUT_SEC
        return max(1, timeout)

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
        applied: dict[str, Any] = {}
        with self._lock:
            for key, value in changes.items():
                if key == "disable_memory_cleaning":
                    if "disable_memory_rebase" in changes:
                        continue
                    key = "disable_memory_rebase"
                if key not in _RUNTIME_MUTABLE_FIELDS:
                    errors[key] = f"field '{key}' is not runtime-mutable"
                    continue
                if not hasattr(self, key):
                    errors[key] = f"unknown field '{key}'"
                    continue
                current = getattr(self, key)
                try:
                    if key in _SENSITIVE_FIELDS and isinstance(value, str) and value.endswith("***"):
                        continue
                    if isinstance(current, bool):
                        value = value if isinstance(value, bool) else str(value).lower() not in {"0", "false", "no", "off", ""}
                    elif isinstance(current, int):
                        value = int(value)
                    elif isinstance(current, str):
                        value = str(value)
                    if key == "compression_reasoning_effort":
                        value = _normalize_compression_reasoning_effort(value)
                    if key == "command_timeout_sec":
                        value = _clamp_command_timeout(value)
                    setattr(self, key, value)
                except (ValueError, TypeError) as e:
                    errors[key] = f"invalid value for '{key}': {e}"
                    continue
                applied[key] = value
        if applied and not errors:
            logger.info("Config updated: %s", {k: ("***" if k in _SENSITIVE_FIELDS else v) for k, v in applied.items()})
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
        d["effective_observer_model"] = self.get_observer_model()
        d["effective_chat_model"] = self.get_chat_model()
        d["effective_compression_model"] = self.get_compression_model()
        d["effective_compression_reasoning_effort"] = self.get_compression_reasoning_effort()
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
                        value = int(overrides[key])
                        params[key] = _clamp_command_timeout(value) if key == "command_timeout_sec" else value
                    except (ValueError, TypeError):
                        pass
        return params


def _env(name: str, *fallback_names: str, default: Any = "", cast: Any = str) -> Any:
    """Read env var, with fallback names for backward compatibility."""
    for n in (name, *fallback_names):
        raw = os.getenv(n)
        if raw is None:
            continue
        value = raw.strip()
        if cast is bool:
            return value.lower() not in {"0", "false", "no", "off", ""}
        if not value:
            continue
        if cast is str:
            return value
        try:
            return cast(value)
        except (ValueError, TypeError):
            continue
    return default


def _default_if_blank(value: Any, default: Any) -> Any:
    if value is None:
        return default
    if isinstance(value, str) and not value.strip():
        return default
    return value


def _normalize_compression_reasoning_effort(value: Any) -> str:
    effort = str(_default_if_blank(value, DEFAULT_COMPRESSION_REASONING_EFFORT)).strip().lower()
    if effort in _ALLOWED_COMPRESSION_REASONING_EFFORTS:
        return effort
    logger.warning(
        "Ignoring unsupported compression reasoning_effort=%r; using %s",
        value,
        DEFAULT_COMPRESSION_REASONING_EFFORT,
    )
    return DEFAULT_COMPRESSION_REASONING_EFFORT


def _string_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        raw_items = value.replace("\n", ",").replace(";", ",").split(",")
    elif isinstance(value, (list, tuple, set)):
        raw_items = list(value)
    else:
        return []
    items: list[str] = []
    seen: set[str] = set()
    for item in raw_items:
        text = str(item or "").strip()
        if not text or text in seen:
            continue
        seen.add(text)
        items.append(text)
    return items


def _sandbox_container_list(*, primary: Any = "", containers: Any = None) -> list[str]:
    configured = _string_list(containers)
    primary_text = str(primary or "").strip()
    if not configured:
        configured = list(DEFAULT_SANDBOX_CONTAINERS)
    if primary_text and primary_text not in configured:
        configured.insert(0, primary_text)
    return configured[:MAX_AGENT_SLOTS]


def load_settings(workspace_root: Path | None = None) -> AgentSettings:
    root = workspace_root or Path.cwd()

    # Try loading config.yml first, fall back to .env
    yml_path = root / "config.yml"
    if yml_path.is_file():
        return _load_from_yaml(root, yml_path)

    return _load_from_env(root)


def _load_from_env(root: Path) -> AgentSettings:
    """Legacy .env-based loading."""
    base_url = _env("PIKAQIU_LLM_BASE_URL", "PIKAQIU_ANTHROPIC_BASE_URL", default=DEFAULT_LLM_BASE_URL)
    if base_url.endswith("/anthropic"):
        base_url = base_url[:-len("/anthropic")]
    sandbox_containers = _sandbox_container_list(
        primary=_env("PIKAQIU_SANDBOX_CONTAINER", default=""),
        containers=_env("PIKAQIU_SANDBOX_CONTAINERS", default=""),
    )

    return AgentSettings(
        workspace_root=root.resolve(),
        db_path=(root / ".pikaqiu_agent" / "state.sqlite3").resolve(),
        sandbox_container=sandbox_containers[0],
        sandbox_workdir=_env("PIKAQIU_SANDBOX_WORKDIR", default="/tmp/pikaqiu-agent-workspace"),
        sandbox_containers=sandbox_containers,
        llm_base_url=base_url,
        llm_api_key=_env("PIKAQIU_LLM_API_KEY", "OPENAI_API_KEY", "PIKAQIU_ANTHROPIC_AUTH_TOKEN", default=DEFAULT_LLM_API_KEY),
        llm_model=_env("PIKAQIU_LLM_MODEL", "PIKAQIU_ANTHROPIC_MODEL", default=DEFAULT_LLM_MODEL),
        llm_chat_model=_env("PIKAQIU_LLM_CHAT_MODEL", default=""),
        llm_thinking=_env("PIKAQIU_LLM_THINKING", default=False, cast=bool),
        llm_reasoning_effort=_env("PIKAQIU_LLM_REASONING_EFFORT", default=DEFAULT_LLM_REASONING_EFFORT),
        llm_use_responses_api=_env("PIKAQIU_LLM_USE_RESPONSES_API", default=True, cast=bool),
        llm_disable_response_storage=_env("PIKAQIU_LLM_DISABLE_RESPONSE_STORAGE", default=True, cast=bool),
        llm_timeout_sec=_env("PIKAQIU_LLM_TIMEOUT_SEC", "PIKAQIU_CLAUDE_TIMEOUT_SEC", default=60, cast=int),
        llm_max_retries=_env("PIKAQIU_LLM_MAX_RETRIES", default=10, cast=int),
        observer_base_url=_env("PIKAQIU_OBSERVER_BASE_URL", default=""),
        observer_api_key=_env("PIKAQIU_OBSERVER_API_KEY", default=""),
        observer_model=_env("PIKAQIU_OBSERVER_MODEL", default=""),
        observer_thinking=_env("PIKAQIU_OBSERVER_THINKING", default=False, cast=bool),
        observer_reasoning_effort=_env("PIKAQIU_OBSERVER_REASONING_EFFORT", default=DEFAULT_LLM_REASONING_EFFORT),
        observer_use_responses_api=_env("PIKAQIU_OBSERVER_USE_RESPONSES_API", default=True, cast=bool),
        observer_disable_response_storage=_env("PIKAQIU_OBSERVER_DISABLE_RESPONSE_STORAGE", default=True, cast=bool),
        compression_base_url=_env("PIKAQIU_COMPRESSION_BASE_URL", default=""),
        compression_api_key=_env("PIKAQIU_COMPRESSION_API_KEY", "OPENAI_API_KEY", default=""),
        compression_model=_env("PIKAQIU_COMPRESSION_MODEL", default=DEFAULT_COMPRESSION_MODEL),
        compression_reasoning_effort=_normalize_compression_reasoning_effort(
            _env(
                "PIKAQIU_COMPRESSION_REASONING_EFFORT",
                default=DEFAULT_COMPRESSION_REASONING_EFFORT,
            )
        ),
        compression_use_responses_api=_env("PIKAQIU_COMPRESSION_USE_RESPONSES_API", default=True, cast=bool),
        compression_disable_response_storage=_env("PIKAQIU_COMPRESSION_DISABLE_RESPONSE_STORAGE", default=True, cast=bool),
        compression_timeout_sec=_env(
            "PIKAQIU_COMPRESSION_TIMEOUT_SEC",
            default=DEFAULT_COMPRESSION_TIMEOUT_SEC,
            cast=int,
        ),
        initial_rounds=_env("PIKAQIU_MAX_ROUNDS", default=4, cast=int),
        initial_commands=_env("PIKAQIU_MAX_COMMANDS_PER_ROUND", default=64, cast=int),
        command_timeout_sec=_clamp_command_timeout(_env("PIKAQIU_COMMAND_TIMEOUT_SEC", default=300, cast=int)),
        stdout_limit=_env("PIKAQIU_STDOUT_LIMIT", default=16000, cast=int),
        memory_compress_interval=_env(
            "PIKAQIU_MEMORY_COMPRESS_INTERVAL",
            default=DEFAULT_MEMORY_COMPRESS_INTERVAL,
            cast=int,
        ),
        knowledge_top_k=_env("PIKAQIU_KNOWLEDGE_TOP_K", default=6, cast=int),
        knowledge_dir=_env("PIKAQIU_KNOWLEDGE_DIR", default="./knowledge"),
        skills_dir=_env("PIKAQIU_SKILLS_DIR", default="./skills"),
        skills_auto_use=_env("PIKAQIU_SKILLS_AUTO_USE", default=True, cast=bool),
        skill_catalog_limit=_env("PIKAQIU_SKILL_CATALOG_LIMIT", default=50, cast=int),
        skill_prompt_max_chars=_env("PIKAQIU_SKILL_PROMPT_MAX_CHARS", default=12000, cast=int),
        skill_reference_max_chars=_env("PIKAQIU_SKILL_REFERENCE_MAX_CHARS", default=20000, cast=int),
        disable_memory_rebase=_env(
            "PIKAQIU_DISABLE_MEMORY_REBASE",
            "PIKAQIU_DISABLE_MEMORY_CLEANING",
            default=False,
            cast=bool,
        ),
        host=_env("PIKAQIU_WEB_HOST", default="127.0.0.1"),
        port=_env("PIKAQIU_WEB_PORT", default=8765, cast=int),
        mock=_env("PIKAQIU_MOCK", default=False, cast=bool),
    )


def _load_from_yaml(root: Path, yml_path: Path) -> AgentSettings:
    """Load settings from config.yml (preferred)."""
    try:
        import yaml
    except ImportError:
        logger.warning("PyYAML not installed, falling back to .env")
        return _load_from_env(root)

    with open(yml_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f) or {}

    model_pool: list[ModelPoolEntry] = []
    for idx, entry in enumerate(cfg.get("model_pool", [])):
        if not isinstance(entry, dict):
            continue
        model_pool.append(ModelPoolEntry(
            id=entry.get("id", f"model-{idx}"),
            base_url=entry.get("base_url", DEFAULT_LLM_BASE_URL),
            api_key=entry.get("api_key", ""),
            model=entry.get("model", DEFAULT_LLM_MODEL),
            thinking=bool(entry.get("thinking", False)),
            reasoning_effort=entry.get("reasoning_effort", DEFAULT_LLM_REASONING_EFFORT),
            use_responses_api=bool(entry.get("use_responses_api", True)),
            disable_response_storage=bool(entry.get("disable_response_storage", True)),
            priority=entry.get("priority", idx + 1),
            max_concurrent=entry.get("max_concurrent", 3),
        ))

    # Primary model = first in pool (highest priority) or env fallback.
    # Environment values intentionally override config.yml so secrets can stay in .env.
    primary = model_pool[0] if model_pool else None
    base_default = primary.base_url if primary else DEFAULT_LLM_BASE_URL
    key_default = primary.api_key if primary else DEFAULT_LLM_API_KEY
    model_default = primary.model if primary else DEFAULT_LLM_MODEL
    thinking_default = primary.thinking if primary else False
    reasoning_effort_default = primary.reasoning_effort if primary else DEFAULT_LLM_REASONING_EFFORT
    use_responses_default = primary.use_responses_api if primary else True
    disable_storage_default = primary.disable_response_storage if primary else True
    llm_base_url = _env("PIKAQIU_LLM_BASE_URL", default=base_default)
    llm_api_key = _env("PIKAQIU_LLM_API_KEY", "OPENAI_API_KEY", default=key_default)
    llm_model = _env("PIKAQIU_LLM_MODEL", default=model_default)
    llm_thinking = _env("PIKAQIU_LLM_THINKING", default=thinking_default, cast=bool)
    llm_reasoning_effort = _env("PIKAQIU_LLM_REASONING_EFFORT", default=reasoning_effort_default)
    llm_use_responses_api = _env("PIKAQIU_LLM_USE_RESPONSES_API", default=use_responses_default, cast=bool)
    llm_disable_response_storage = _env(
        "PIKAQIU_LLM_DISABLE_RESPONSE_STORAGE",
        default=disable_storage_default,
        cast=bool,
    )
    if primary:
        primary.base_url = llm_base_url
        primary.api_key = llm_api_key
        primary.model = llm_model
        primary.thinking = llm_thinking
        primary.reasoning_effort = llm_reasoning_effort
        primary.use_responses_api = llm_use_responses_api
        primary.disable_response_storage = llm_disable_response_storage

    sections: dict[str, dict[str, Any]] = {}
    for key in ("observer", "agent_defaults", "sandbox", "web", "compression"):
        section = cfg.get(key, {})
        sections[key] = section if isinstance(section, dict) else {}
    observer_cfg, ag, sb, web, compression = (
        sections["observer"],
        sections["agent_defaults"],
        sections["sandbox"],
        sections["web"],
        sections["compression"],
    )

    observer_base_url = _env("PIKAQIU_OBSERVER_BASE_URL", default=observer_cfg.get("base_url", ""))
    observer_api_key = _env("PIKAQIU_OBSERVER_API_KEY", default=observer_cfg.get("api_key", ""))
    observer_model = _env("PIKAQIU_OBSERVER_MODEL", default=observer_cfg.get("model", ""))
    observer_thinking = _env("PIKAQIU_OBSERVER_THINKING", default=observer_cfg.get("thinking", False), cast=bool)
    observer_reasoning_effort = _env(
        "PIKAQIU_OBSERVER_REASONING_EFFORT",
        default=observer_cfg.get("reasoning_effort", DEFAULT_LLM_REASONING_EFFORT),
    )
    observer_use_responses_api = _env(
        "PIKAQIU_OBSERVER_USE_RESPONSES_API",
        default=observer_cfg.get("use_responses_api", True),
        cast=bool,
    )
    observer_disable_response_storage = _env(
        "PIKAQIU_OBSERVER_DISABLE_RESPONSE_STORAGE",
        default=observer_cfg.get("disable_response_storage", True),
        cast=bool,
    )
    compression_base_url = _env("PIKAQIU_COMPRESSION_BASE_URL", default=compression.get("base_url", ""))
    compression_api_key = _env("PIKAQIU_COMPRESSION_API_KEY", "OPENAI_API_KEY", default=compression.get("api_key", ""))
    compression_model = _env(
        "PIKAQIU_COMPRESSION_MODEL",
        default=_default_if_blank(compression.get("model"), DEFAULT_COMPRESSION_MODEL),
    )
    compression_reasoning_effort = _normalize_compression_reasoning_effort(
        _env(
            "PIKAQIU_COMPRESSION_REASONING_EFFORT",
            default=_default_if_blank(
                compression.get("reasoning_effort"),
                DEFAULT_COMPRESSION_REASONING_EFFORT,
            ),
        ),
    )
    compression_use_responses_api = _env(
        "PIKAQIU_COMPRESSION_USE_RESPONSES_API",
        default=compression.get("use_responses_api", True),
        cast=bool,
    )
    compression_disable_response_storage = _env(
        "PIKAQIU_COMPRESSION_DISABLE_RESPONSE_STORAGE",
        default=compression.get("disable_response_storage", True),
        cast=bool,
    )

    sandbox_containers = _sandbox_container_list(
        primary=_env("PIKAQIU_SANDBOX_CONTAINER", default=sb.get("container", "")),
        containers=_env("PIKAQIU_SANDBOX_CONTAINERS", default=sb.get("containers", [])),
    )
    _sb_default = sandbox_containers[0]

    raw_difficulty_params = ag.get("difficulty_params", {})
    difficulty_params: dict[str, DifficultyParams] = {}
    if isinstance(raw_difficulty_params, dict):
        for diff_name, vals in raw_difficulty_params.items():
            if isinstance(vals, dict):
                difficulty_params[diff_name.lower()] = DifficultyParams(
                    initial_rounds=vals.get("initial_rounds", 4),
                    initial_commands=vals.get("initial_commands", 64),
                    max_rounds=vals.get("max_rounds", 16),
                    max_commands=vals.get("max_commands", 400),
                )

    settings = AgentSettings(
        workspace_root=root.resolve(),
        db_path=(root / ".pikaqiu_agent" / "state.sqlite3").resolve(),
        sandbox_container=_sb_default,
        sandbox_workdir=sb.get("workdir", "/tmp/pikaqiu-agent-workspace"),
        sandbox_containers=sandbox_containers,
        sandbox_public_ip=sb.get("public_ip", ""),
        llm_base_url=llm_base_url,
        llm_api_key=llm_api_key,
        llm_model=llm_model,
        llm_chat_model="",
        llm_thinking=llm_thinking,
        llm_reasoning_effort=llm_reasoning_effort,
        llm_use_responses_api=llm_use_responses_api,
        llm_disable_response_storage=llm_disable_response_storage,
        llm_timeout_sec=ag.get("llm_timeout_sec", 240),
        llm_max_retries=ag.get("llm_max_retries", 10),
        compression_base_url=compression_base_url,
        compression_api_key=compression_api_key,
        compression_model=compression_model,
        compression_reasoning_effort=compression_reasoning_effort,
        compression_use_responses_api=compression_use_responses_api,
        compression_disable_response_storage=compression_disable_response_storage,
        compression_timeout_sec=_env(
            "PIKAQIU_COMPRESSION_TIMEOUT_SEC",
            default=_default_if_blank(compression.get("timeout_sec"), DEFAULT_COMPRESSION_TIMEOUT_SEC),
            cast=int,
        ),
        observer_base_url=observer_base_url,
        observer_api_key=observer_api_key,
        observer_model=observer_model,
        observer_thinking=observer_thinking,
        observer_reasoning_effort=observer_reasoning_effort,
        observer_use_responses_api=observer_use_responses_api,
        observer_disable_response_storage=observer_disable_response_storage,
        initial_rounds=ag.get("initial_rounds", ag.get("max_rounds", 4)),
        initial_commands=ag.get("initial_commands", ag.get("max_commands_per_round", 64)),
        command_timeout_sec=_clamp_command_timeout(ag.get("command_timeout_sec", 300)),
        stdout_limit=ag.get("stdout_limit", 8000),
        context_compress_threshold=ag.get("context_compress_threshold", 80000),
        memory_compress_interval=_env(
            "PIKAQIU_MEMORY_COMPRESS_INTERVAL",
            default=ag.get("memory_compress_interval", DEFAULT_MEMORY_COMPRESS_INTERVAL),
            cast=int,
        ),
        knowledge_top_k=ag.get("knowledge_top_k", 6),
        knowledge_dir=ag.get("knowledge_dir", "./knowledge"),
        skills_dir=ag.get("skills_dir", "./skills"),
        skills_auto_use=ag.get("skills_auto_use", True),
        skill_catalog_limit=ag.get("skill_catalog_limit", 50),
        skill_prompt_max_chars=ag.get("skill_prompt_max_chars", 12000),
        skill_reference_max_chars=ag.get("skill_reference_max_chars", 20000),
        max_rounds=ag.get("max_rounds_ceiling", ag.get("retry_max_rounds", 16)),
        max_commands=ag.get("max_commands_ceiling", ag.get("retry_max_commands_per_round", 128)),
        max_retries=ag.get("max_retries", 2),
        mission_timeout_sec=ag.get("mission_timeout_sec", 0),
        difficulty_params=difficulty_params,
        multi_flag_scaling=MultiFlagScaling(
            extra_rounds_per_flag=ag.get("multi_flag_scaling", {}).get("extra_rounds_per_flag", 3),
            extra_commands_per_flag=ag.get("multi_flag_scaling", {}).get("extra_commands_per_flag", 12),
        ),
        host=web.get("host", "127.0.0.1"),
        port=web.get("port", 8765),
        mock=False,
        model_pool=model_pool,
        disable_memory_rebase=_env(
            "PIKAQIU_DISABLE_MEMORY_REBASE",
            "PIKAQIU_DISABLE_MEMORY_CLEANING",
            default=ag.get("disable_memory_rebase", ag.get("disable_memory_cleaning", False)),
            cast=bool,
        ),
    )

    logger.info("Loaded config from %s: %d models in pool",
                yml_path, len(model_pool))
    return settings
