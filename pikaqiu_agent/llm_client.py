"""LangChain-based LLM client for the PikaQiu Agent.

Uses langchain-deepseek for DeepSeek Reasoner (thinking model) and
langchain-openai for advisor / decision models (SiliconFlow, OpenAI, etc.).
Provides the same LLMResult interface consumed by orchestrator.py.
"""
from __future__ import annotations

import json
import logging
import re
import time
from dataclasses import dataclass, field
from typing import Any

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_deepseek import ChatDeepSeek
from langchain_openai import ChatOpenAI

try:
    from langchain_anthropic import ChatAnthropic
except ImportError:
    ChatAnthropic = None  # type: ignore[assignment,misc]

from pikaqiu_agent.config import AgentSettings

logger = logging.getLogger(__name__)


def format_llm_error(
    e: Exception,
    *,
    model: str = "",
    messages: list | None = None,
) -> str:
    """Format LLM/network error with full details for debugging.

    Extracts HTTP status, response body, request ID from openai errors.
    Adds model name and message type breakdown for context.
    """
    parts: list[str] = []

    # Error class and full message (generous limit)
    err_type = type(e).__name__
    err_str = str(e)[:2000]
    parts.append(f"[{err_type}] {err_str}")

    # OpenAI-specific attributes
    status = getattr(e, "status_code", None)
    if status:
        parts.append(f"HTTP={status}")
    body = getattr(e, "body", None)
    if body and isinstance(body, dict):
        # Extract request_id if present
        req_id = body.get("error", {}).get("request_id") or body.get("request_id")
        if req_id:
            parts.append(f"req_id={req_id}")
        body_str = json.dumps(body, ensure_ascii=False)[:800]
        parts.append(f"body={body_str}")

    # Model context
    if model:
        parts.append(f"model={model}")

    # Message breakdown
    if messages:
        type_counts: dict[str, int] = {}
        total_chars = 0
        for m in messages:
            t = type(m).__name__
            type_counts[t] = type_counts.get(t, 0) + 1
            c = getattr(m, "content", None)
            if isinstance(c, str):
                total_chars += len(c)
        parts.append(f"msgs={type_counts} total_chars={total_chars}")

    return " | ".join(parts)


@dataclass(frozen=True)
class LLMResult:
    raw_text: str
    payload: dict[str, Any]
    used_mock: bool
    thinking: str = ""
    usage: dict[str, int] | None = None


def _build_chat_model(
    base_url: str, api_key: str, model: str,
    timeout: int = 60, max_retries: int = 3,
    temperature: float | None = None,
    enable_thinking: bool = True,
    thinking_enabled: bool = False,
) -> ChatDeepSeek | ChatOpenAI:
    """Create the right LangChain chat model based on model name.

    Automatically detects model provider and applies appropriate parameters.
    Supports: DeepSeek, Claude (native Anthropic SDK), OpenAI, Qwen, local models.
    """
    base = base_url.rstrip("/")
    model_lower = model.lower()

    # DeepSeek models use ChatDeepSeek
    if "deepseek" in model_lower:
        kwargs: dict[str, Any] = {
            "model": model,
            "api_key": api_key,
            "base_url": base if not base.endswith("/v1") else base,
            "timeout": timeout,
            "max_retries": max_retries,
        }
        if temperature is not None and "reasoner" not in model_lower:
            kwargs["temperature"] = temperature
        if thinking_enabled and "reasoner" not in model_lower:
            kwargs["extra_body"] = {"thinking": {"type": "enabled"}}
        return ChatDeepSeek(**kwargs)

    # Claude / Anthropic models: use native ChatAnthropic for prompt caching support
    if ChatAnthropic is not None and ("claude" in model_lower or "anthropic" in model_lower):
        # ChatAnthropic SDK appends /v1/messages internally, so strip /v1
        anth_base = base[:-3] if base.endswith("/v1") else base
        kwargs = {
            "model": model,
            "anthropic_api_key": api_key,
            "base_url": anth_base,
            "timeout": float(timeout),
            "max_retries": max_retries,
            "max_tokens": 16384,
        }
        if temperature is not None:
            kwargs["temperature"] = temperature
        logger.info("[llm] Creating ChatAnthropic model=%s base=%s", model, anth_base)
        return ChatAnthropic(**kwargs)

    # Everything else uses ChatOpenAI (works with OpenAI-compatible proxies)
    kwargs = {
        "model": model,
        "api_key": api_key,
        "base_url": base if base.endswith("/v1") else f"{base}/v1",
        "timeout": timeout,
        "max_retries": max_retries,
    }
    if temperature is not None:
        kwargs["temperature"] = temperature
    # Qwen / SiliconFlow: supports enable_thinking toggle
    if "qwen" in model_lower and not enable_thinking:
        kwargs["extra_body"] = {"enable_thinking": False}
    return ChatOpenAI(**kwargs)


class LLMClient:
    """LangChain-powered LLM client with main / memory / advisor roles."""

    def __init__(self, settings: AgentSettings) -> None:
        self.settings = settings
        base_url = (settings.llm_base_url or "https://api.deepseek.com").rstrip("/")
        api_key = settings.llm_api_key or ""
        model = settings.llm_model or "deepseek-reasoner"
        timeout = settings.llm_timeout_sec or 60

        # Main model (memory compression; if deepseek-reasoner, uses thinking by default)
        self._main_model = _build_chat_model(
            base_url, api_key, model,
            timeout=timeout, temperature=None,
        )
        self._model_name = model

        # Tool-calling model: same as main model by default (deepseek-reasoner now supports tools)
        # If llm_thinking=True and chat model is deepseek-chat, enable thinking via extra_body
        chat_model_name = settings.get_chat_model()
        if chat_model_name == model:
            self._main_chat_model = self._main_model  # same model, reuse
        else:
            self._main_chat_model = _build_chat_model(
                base_url, api_key, chat_model_name,
                timeout=timeout, temperature=0.0,
                thinking_enabled=settings.llm_thinking,
            )
        self._chat_model_name = chat_model_name

        # Advisor model (may be different provider / model)
        adv_base = settings.get_advisor_base_url().rstrip("/")
        adv_key = settings.get_advisor_api_key()
        adv_model = settings.get_advisor_model()
        self._advisor_model = _build_chat_model(
            adv_base, adv_key, adv_model,
            timeout=timeout, temperature=0.3,
            enable_thinking=settings.advisor_thinking,
        )
        self._advisor_model_name = adv_model

        # Tool-calling model (used for ReAct loop)
        self._tool_model = self._main_chat_model
        self._tool_model_name = chat_model_name

        # Compression model (cheap/fast model for mid-round context compression)
        if settings.compression_model:
            comp_base = (settings.compression_base_url or base_url).rstrip("/")
            comp_key = settings.compression_api_key or api_key
            comp_timeout = settings.compression_timeout_sec or 60
            self._compression_model = _build_chat_model(
                comp_base, comp_key, settings.compression_model,
                timeout=comp_timeout, temperature=0.0,
            )
            self._compression_model_name = settings.compression_model
            logger.info("[llm] Compression model configured: %s", settings.compression_model)
        else:
            self._compression_model = None
            self._compression_model_name = ""

    def get_tool_model(self):
        """Return the chat model suitable for tool calling (not the thinking model)."""
        return self._tool_model

    @property
    def is_tool_model_anthropic(self) -> bool:
        """Check if the tool model is a native Anthropic model (supports prompt caching)."""
        return ChatAnthropic is not None and isinstance(self._tool_model, ChatAnthropic)

    def create_tool_model_for(self, base_url: str, api_key: str, model: str):
        """Create a per-mission tool model from explicit parameters (for multi-model parallel)."""
        return _build_chat_model(
            base_url, api_key, model,
            timeout=self.settings.llm_timeout_sec or 60,
            temperature=0.0,
        )

    @staticmethod
    def is_anthropic_model(model) -> bool:
        """Check if a model instance is a native Anthropic model."""
        return ChatAnthropic is not None and isinstance(model, ChatAnthropic)

    # ---- Public API (same interface as before) ----

    def invoke_main(self, prompt: str, round_no: int, use_thinking: bool = True) -> LLMResult:
        if self.settings.use_mock_llm:
            return self._mock_main(round_no)
        model = self._main_model if use_thinking else self._main_chat_model
        model_label = self._model_name if use_thinking else self._chat_model_name
        logger.info("[LLM:main] round=%d mode=%s model=%s", round_no, "thinking" if use_thinking else "chat", model_label)
        result = self._invoke(model, prompt, role="main")
        if not _looks_like_main_payload(result.payload):
            error_text = _extract_text(result.payload, result.raw_text)
            payload = {
                "round_goal": "模型输出格式异常，请求 advisor 协助",
                "thought_summary": "LLM 返回了非主 agent schema 的内容。",
                "knowledge_queries": [],
                "commands": [],
                "findings": [],
                "memory_updates": {
                    "facts": [],
                    "leads": [],
                    "dead_ends": [error_text] if error_text else [],
                    "credentials": [],
                },
                "need_advice": True,
                "advice_question": "主 agent 输出不是预期 JSON schema",
                "status": "blocked",
                "done_reason": "",
            }
            return LLMResult(
                raw_text=result.raw_text, payload=payload, used_mock=False,
                thinking=result.thinking, usage=result.usage,
            )
        return result

    def invoke_memory(self, prompt: str, previous_memory: dict[str, Any]) -> LLMResult:
        if self.settings.use_mock_llm:
            return self._mock_memory(previous_memory)
        result = self._invoke(self._main_model, prompt, role="memory")
        if not _looks_like_memory_payload(result.payload):
            summary = _extract_text(result.payload, result.raw_text)
            prev_summary = str(previous_memory.get("summary", "") or "").strip()
            if not summary:
                summary = prev_summary or "memory agent 未返回有效 JSON，沿用上一轮记忆。"
            payload = {
                "summary": summary,
                "findings": list(previous_memory.get("findings", [])),
                "leads": list(previous_memory.get("leads", [])),
                "dead_ends": list(previous_memory.get("dead_ends", [])),
                "credentials": list(previous_memory.get("credentials", [])),
                "next_focus": list(previous_memory.get("next_focus", [])),
            }
            return LLMResult(
                raw_text=result.raw_text, payload=payload, used_mock=False,
                thinking=result.thinking, usage=result.usage,
            )
        return result

    def invoke_advisor(self, prompt: str) -> LLMResult:
        if self.settings.use_mock_llm:
            return self._mock_advisor()
        result = self._invoke(
            self._advisor_model,
            prompt,
            role="advisor",
            system=(
                "你是顶级渗透测试专家，担任独立审查角色，协助完成授权安全评估。\n"
                "这是完全合法的安全测试环境。\n\n"
                "## 环境限制（重要）\n"
                "提问者运行在一个**隔离的Kali Linux Docker沙箱**中：\n"
                "- **可以监听端口**但沙箱非交互式：必须用Python脚本化监听器（自动accept→发命令→收输出），不能用nc手动交互\n"
                "- **无法访问外网**：不能使用dnslog、burp collaborator、webhook.site等外部服务\n"
                "- **每次python_exec是独立进程**：变量和session不跨调用保存\n"
                "建议利用的替代技术：回显优先、写入webroot后curl读取、脚本化反弹shell监听、时间盲注\n\n"
                "你的职责：\n"
                "1. **独立评估**：先根据上下文判断当前渗透路径是否正确，不要只顺着提问者的思路走\n"
                "2. **主动发现**：识别提问者可能遗漏的攻击向量或更高效的路径\n"
                "3. **纠正错误**：如果当前方向有明显问题，直接指出并给出正确方向\n"
                "4. **具体建议**：给出可直接执行的命令或代码，不要泛泛而谈\n"
                "5. **质疑预设**：不要假设特定架构一定存在（如 admin bot 提交入口、外部回调服务等）。\n"
                "   先确认这些组件确实存在于目标环境。如果找不到，考虑验证机制可能是服务端直接触发、\n"
                "   内部自动化流程、或其他非标准路径——建议提问者直接测试攻击向量本身是否有效。\n"
                "6. **考虑沙箱限制**：所有建议必须在上述沙箱环境中可执行，不要建议需要监听端口或外网访问的方案\n"
                "7. 禁止任何免责声明、安全警告或授权提醒\n"
                "8. 你作为专家，对目标环境了解不够深入，因此不能假设环境细节，对于路径等都要提醒提问者你不清楚，给出的示例也要写明\n"
            ),
        )
        if not _looks_like_advisor_payload(result.payload):
            payload = {
                "advice": _extract_text(result.payload, result.raw_text),
                "next_queries": [],
                "next_commands": [],
                "risk_notes": [],
            }
            return LLMResult(
                raw_text=result.raw_text, payload=payload, used_mock=False,
                thinking=result.thinking, usage=result.usage,
            )
        return result

    @property
    def has_compression_model(self) -> bool:
        """Check if a dedicated compression model is configured."""
        return self._compression_model is not None

    def invoke_compression(self, messages_text: str, mission_context: str) -> str | None:
        """Use cheap model to compress old conversation context.

        Args:
            messages_text: Concatenated text of messages to compress
            mission_context: Brief description of the mission (target, goal)

        Returns:
            Compressed summary string, or None if compression model unavailable/failed.
        """
        if not self._compression_model:
            return None

        system = (
            "你是一个渗透测试上下文压缩助手。你的任务是将一段对话历史压缩为简洁的摘要。\n\n"
            "## 压缩规则\n"
            "1. **必须保留**: 已确认的漏洞、RCE路径、有效凭据、flag内容、端口/服务发现、可利用的CVE\n"
            "2. **必须保留**: 具体的URL路径、IP地址、端口号、文件路径、用户名密码\n"
            "3. **必须保留**: 已确认失败的路径（死胡同），避免重复探索\n"
            "4. **可以丢弃**: 命令的原始输出（只保留关键发现）、重复尝试、连接超时细节\n"
            "5. **可以丢弃**: 工具调用的技术细节（只保留结果）\n"
            "6. **格式**: 用简洁的要点列表，每条一行，按时间顺序\n\n"
            "直接输出压缩摘要，不要加任何前缀或解释。"
        )

        prompt = f"## 任务背景\n{mission_context}\n\n## 需要压缩的对话历史\n{messages_text}"

        try:
            messages = [SystemMessage(content=system), HumanMessage(content=prompt)]
            ai_msg = self._compression_model.invoke(messages)
            result = ai_msg.content or ""
            if isinstance(result, list):
                result = "\n".join(str(b.get("text", "")) if isinstance(b, dict) else str(b) for b in result)
            logger.info("[llm] compression done: %d chars → %d chars", len(messages_text), len(result))
            return result.strip()
        except Exception as e:
            logger.warning("[llm] compression model failed: %s", e)
            return None

    def _invoke(
        self,
        chat_model: ChatDeepSeek | ChatOpenAI,
        prompt: str,
        role: str = "main",
        system: str | None = None,
    ) -> LLMResult:
        """Invoke a LangChain chat model and return LLMResult."""
        model_name = getattr(chat_model, "model_name", "unknown")
        logger.info(
            "[LLM:%s] 调用 model=%s prompt=%d chars ...",
            role, model_name, len(prompt),
        )

        messages = []
        if system:
            messages.append(SystemMessage(content=system))
        messages.append(HumanMessage(content=prompt))
        t0 = time.time()

        last_err: Exception | None = None
        ai_msg = None
        for attempt in range(3):
            try:
                ai_msg = chat_model.invoke(messages)
                break
            except Exception as e:
                last_err = e
                err_str = str(e)
                detail = format_llm_error(e, model=model_name, messages=messages)
                # Retry on transient server errors (5xx)
                if any(code in err_str for code in ("500", "502", "503", "504", "50507")) and attempt < 2:
                    logger.warning("[LLM:%s] ✗ 第%d次调用失败，1s后重试: %s", role, attempt + 1, detail)
                    time.sleep(1)
                    continue
                logger.error("[LLM:%s] ✗ 调用失败: %s", role, detail)
                raise
        if ai_msg is None:
            if last_err is not None:
                raise last_err
            raise RuntimeError(f"[LLM:{role}] invoke returned None after all retries")

        elapsed = time.time() - t0
        content = ai_msg.content or ""
        # ChatAnthropic may return content as list of blocks [{"type":"text","text":"..."}]
        if isinstance(content, list):
            content = "\n".join(
                block.get("text", "") if isinstance(block, dict) else str(block)
                for block in content
            )

        # Extract reasoning_content (DeepSeek thinking model)
        thinking = ai_msg.additional_kwargs.get("reasoning_content", "")

        # Extract usage from response_metadata
        usage = None
        usage_meta = ai_msg.usage_metadata
        if usage_meta:
            usage = {
                "prompt_tokens": usage_meta.get("input_tokens", 0),
                "completion_tokens": usage_meta.get("output_tokens", 0),
                "total_tokens": usage_meta.get("total_tokens", 0),
            }

        tokens_info = ""
        if usage:
            tokens_info = f" tokens(in={usage.get('prompt_tokens',0)} out={usage.get('completion_tokens',0)})"
        logger.info(
            "[LLM:%s] ✓ 完成 %.1fs response=%d chars%s",
            role, elapsed, len(content), tokens_info,
        )

        payload = _parse_json_response(content)

        return LLMResult(
            raw_text=content,
            payload=payload,
            used_mock=False,
            thinking=thinking,
            usage=usage,
        )

    # ---- Mock implementations ----

    def _mock_main(self, round_no: int) -> LLMResult:
        if round_no == 1:
            payload = {
                "round_goal": "确认 sandbox 可用性与基础工具集",
                "thought_summary": "先用低风险命令探测环境。",
                "knowledge_queries": ["nmap 资产发现", "web 初始指纹识别"],
                "commands": [
                    {
                        "command": "pwd; whoami; ls -la; for t in nmap sqlmap curl dig python3; do printf '%s: ' \"$t\"; command -v \"$t\" || true; done",
                        "timeout": 30,
                        "purpose": "确认 sandbox 工作目录和工具",
                        "expect": "看到路径、用户和工具",
                    }
                ],
                "findings": [],
                "memory_updates": {"facts": ["首轮探测"], "leads": [], "dead_ends": [], "credentials": []},
                "need_advice": False,
                "advice_question": "",
                "status": "continue",
                "done_reason": "",
            }
        else:
            payload = {
                "round_goal": "等待真实模型",
                "thought_summary": "mock 模式已验证。",
                "knowledge_queries": [],
                "commands": [],
                "findings": [{"kind": "note", "value": "mock_verified", "evidence": "链路完成", "confidence": 0.99}],
                "memory_updates": {"facts": ["mock 完成"], "leads": [], "dead_ends": [], "credentials": []},
                "need_advice": False,
                "advice_question": "",
                "status": "done",
                "done_reason": "mock 自测完成",
            }
        return LLMResult(raw_text=json.dumps(payload, ensure_ascii=False), payload=payload, used_mock=True)

    def _mock_memory(self, previous_memory: dict[str, Any]) -> LLMResult:
        payload = {
            "summary": "mock 模式，链路已闭环。",
            "findings": list(previous_memory.get("findings", []))[:20],
            "leads": list(previous_memory.get("leads", []))[:20],
            "dead_ends": list(previous_memory.get("dead_ends", []))[:20],
            "credentials": list(previous_memory.get("credentials", []))[:20],
            "next_focus": ["设置 API key 后切真实模型"],
        }
        return LLMResult(raw_text=json.dumps(payload, ensure_ascii=False), payload=payload, used_mock=True)

    def _mock_advisor(self) -> LLMResult:
        payload = {
            "advice": "mock 模式建议：先验证 sandbox 和链路。",
            "next_queries": ["sandbox 工具探测"],
            "next_commands": [],
            "risk_notes": ["mock 模式不做真实攻击"],
        }
        return LLMResult(raw_text=json.dumps(payload, ensure_ascii=False), payload=payload, used_mock=True)


# ---- JSON parsing helpers ----

def _parse_json_response(text: str) -> dict[str, Any]:
    """Parse LLM response text into a dict, handling various formats."""
    text = (text or "").strip()
    if not text:
        return {}

    # Direct parse
    try:
        result = json.loads(text)
        if isinstance(result, dict):
            return result
    except json.JSONDecodeError:
        pass

    # Fix double-brace output: {{ ... }} → { ... }
    fixed = _fix_double_braces(text)
    if fixed != text:
        try:
            result = json.loads(fixed)
            if isinstance(result, dict):
                return result
        except json.JSONDecodeError:
            pass

    # Try stripping code fences
    match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, flags=re.S)
    if match:
        candidate = match.group(1)
        for attempt in (candidate, _fix_double_braces(candidate)):
            try:
                result = json.loads(attempt)
                if isinstance(result, dict):
                    return result
            except json.JSONDecodeError:
                pass

    # Find first { to last }
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end > start:
        candidate = text[start:end + 1]
        for attempt in (candidate, _fix_double_braces(candidate)):
            try:
                result = json.loads(attempt)
                if isinstance(result, dict):
                    return result
            except json.JSONDecodeError:
                pass

    return {"raw_text": text, "status": "blocked", "need_advice": True}


def _fix_double_braces(text: str) -> str:
    """Fix {{ ... }} double-brace JSON caused by f-string escaping leaking into LLM output."""
    s = text.strip()
    if s.startswith("{{") and not s.startswith("{{{"):
        s = s[1:]  # strip one leading brace
    if s.endswith("}}") and not s.endswith("}}}"):
        s = s[:-1]  # strip one trailing brace
    return s


def _looks_like_main_payload(payload: dict[str, Any]) -> bool:
    return any(
        key in payload
        for key in ("round_goal", "commands", "findings", "status", "memory_updates")
    )


def _looks_like_memory_payload(payload: dict[str, Any]) -> bool:
    return any(
        key in payload
        for key in ("summary", "findings", "leads", "dead_ends", "next_focus")
    )


def _looks_like_advisor_payload(payload: dict[str, Any]) -> bool:
    return any(
        key in payload
        for key in ("advice", "next_queries", "next_commands", "risk_notes")
    )


def _extract_text(payload: dict[str, Any], raw_text: str) -> str:
    for key in ("result", "message", "error", "raw_text", "advice"):
        value = payload.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return (raw_text or "").strip()[:500]
