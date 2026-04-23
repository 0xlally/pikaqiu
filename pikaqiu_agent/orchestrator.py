from __future__ import annotations

import json
import logging
import threading
import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeout
from typing import Any

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage

from pikaqiu_agent.config import AgentSettings
from pikaqiu_agent.knowledge import KnowledgeIndexer
from pikaqiu_agent.llm_client import LLMClient, format_llm_error
from pikaqiu_agent.memory import normalize_memory_enhanced, detect_stall, score_importance, retrieve_forgotten_context
from pikaqiu_agent.prompts import (
    build_tool_system_prompt,
    build_volatile_context,
    build_tool_memory_prompt,
    build_memory_cleaning_prompt,
)
from pikaqiu_agent.sandbox import SandboxExecutor
from pikaqiu_agent.storage import MissionStore
from pikaqiu_agent.tools import create_all_tools

logger = logging.getLogger(__name__)


def _compact_json(obj: Any, max_len: int = 400) -> str:
    """Serialize obj to compact JSON, truncating if too long."""
    try:
        s = json.dumps(obj, ensure_ascii=False, separators=(",", ":"))
    except Exception:
        s = str(obj)
    return s if len(s) <= max_len else s[: max_len - 3] + "..."


def _truncate_middle(text: str, limit: int) -> str:
    """Truncate text by removing the middle portion, keeping head + tail.
    Returns original text if within limit."""
    if len(text) <= limit:
        return text
    # Keep 20% head, 80% tail (tail usually has the latest/most useful results)
    head_size = int(limit * 0.2)
    tail_size = limit - head_size - 80  # reserve space for marker
    marker = f"\n\n... [输出过长，中间省略 {len(text) - head_size - tail_size} 字符] ...\n\n"
    return text[:head_size] + marker + text[-tail_size:]


def _estimate_messages_size(messages: list) -> int:
    """Estimate total character count of all messages in the conversation."""
    total = 0
    for msg in messages:
        content = msg.content if hasattr(msg, "content") else str(msg)
        if isinstance(content, str):
            total += len(content)
        elif isinstance(content, list):
            for part in content:
                if isinstance(part, dict):
                    total += len(str(part.get("text", "")))
                else:
                    total += len(str(part))
    return total


class OrchestratorManager:
    def __init__(
        self,
        settings: AgentSettings,
        store: MissionStore,
        knowledge: KnowledgeIndexer,
        sandbox: SandboxExecutor,
        llm: LLMClient,
    ) -> None:
        self.settings = settings
        self.store = store
        self.knowledge = knowledge
        self.sandbox = sandbox
        self.llm = llm
        self._threads: dict[str, threading.Thread] = {}
        self._lock = threading.Lock()
        self._mission_meta: dict[str, dict] = {}  # mission_id -> extra params (e.g. mission_timeout_sec)
        # Per-mission sandbox allocation
        self._sandbox_alloc: dict[str, SandboxExecutor] = {}  # mission_id -> executor
        containers = settings.sandbox_containers or [settings.sandbox_container]
        self._container_pool: list[str] = list(containers)
        self._container_usage: dict[str, str] = {c: "" for c in containers}  # container -> mission_id

    def _allocate_sandbox(self, mission_id: str) -> SandboxExecutor:
        """Allocate a dedicated sandbox container for a mission."""
        with self._lock:
            for container, user in self._container_usage.items():
                if not user:
                    self._container_usage[container] = mission_id
                    executor = SandboxExecutor(self.settings, container_override=container)
                    self._sandbox_alloc[mission_id] = executor
                    logger.info("[sandbox-pool] allocated %s -> mission %s", container, mission_id[:8])
                    return executor
            # All busy — fall back to first container (shared)
            first = self._container_pool[0]
            logger.warning("[sandbox-pool] all containers busy, sharing %s for mission %s", first, mission_id[:8])
            executor = SandboxExecutor(self.settings, container_override=first)
            self._sandbox_alloc[mission_id] = executor
            return executor

    def _release_sandbox(self, mission_id: str) -> None:
        """Release the sandbox allocated to a mission."""
        with self._lock:
            self._sandbox_alloc.pop(mission_id, None)
            for container, user in self._container_usage.items():
                if user == mission_id:
                    self._container_usage[container] = ""
                    logger.info("[sandbox-pool] released %s <- mission %s", container, mission_id[:8])
                    break

    def start_mission(
        self,
        *,
        name: str,
        target: str,
        goal: str,
        scope: str,
        domains: list[str],
        max_rounds: int,
        max_commands: int,
        command_timeout_sec: int,
        model_id: str | None = None,
        expected_flags: int = 1,
        mission_timeout_sec: int = 0,
    ) -> str:
        # model_id override allows picking per-mission model
        if model_id and model_id != "default":
            entry = self.settings.get_model_by_id(model_id)
            if entry:
                model_name = entry.model
            else:
                model_name = self.settings.llm_model
        else:
            model_name = "mock" if self.settings.use_mock_llm else self.settings.llm_model
        mission_id = self.store.create_mission(
            name=name,
            target=target,
            goal=goal,
            scope=scope,
            domains=domains,
            max_rounds=max_rounds,
            max_commands=max_commands,
            command_timeout_sec=command_timeout_sec,
            model=model_name,
            expected_flags=expected_flags,
        )
        self._mission_meta[mission_id] = {
            "mission_timeout_sec": mission_timeout_sec,
        }
        thread = threading.Thread(
            target=self._run_mission,
            args=(mission_id,),
            name=f"mission-{mission_id[:8]}",
            daemon=True,
        )
        with self._lock:
            self._threads[mission_id] = thread
        thread.start()
        return mission_id

    def stop_mission(self, mission_id: str) -> None:
        self.store.request_stop(mission_id)

    def thread_alive(self, mission_id: str) -> bool:
        with self._lock:
            thread = self._threads.get(mission_id)
        return bool(thread and thread.is_alive())

    def _collect_env_info(self, mission_id: str, sandbox: SandboxExecutor | None = None) -> str:
        """Run env-info script in sandbox once and return the JSON output."""
        sbx = sandbox or self.sandbox
        try:
            result = sbx.run(
                "python3 /opt/pikaqiu-tools/env-info 2>/dev/null",
                workdir="/tmp",
                timeout_sec=15,
            )
            output = (result.stdout or "").strip()
            if result.exit_code == 0 and output:
                self.store.add_event(
                    mission_id=mission_id,
                    round_no=0,
                    event_type="system",
                    title="环境信息已采集",
                    content=output[:500],
                )
                return output
        except Exception as e:
            logger.warning("[orchestrator] env-info collection failed: %s", e)
        return ""

    def _do_final_memory_compression(
        self,
        mission_id: str,
        mission: dict[str, Any],
        memory: dict[str, Any],
        round_no: int,
        tool_call_log: list[dict[str, Any]],
        outcome: str,
    ) -> None:
        """Run a final memory compression so DA can analyze the mission outcome."""
        try:
            memory_prompt = build_tool_memory_prompt(
                mission=mission,
                previous_memory=memory,
                round_no=round_no,
                tool_call_log=tool_call_log,
            )
            pool = ThreadPoolExecutor(max_workers=1)
            try:
                future = pool.submit(self.llm.invoke_memory, memory_prompt, memory)
                memory_result = future.result(timeout=self.settings.llm_timeout_sec)
            finally:
                pool.shutdown(wait=False)
            new_memory = normalize_memory_enhanced(memory_result.payload, memory)
            self.store.set_memory(mission_id, new_memory)
            self.store.add_event(
                mission_id=mission_id,
                round_no=round_no,
                event_type="memory_agent",
                title=f"最终记忆压缩 ({outcome})",
                content=_compact_json(new_memory),
            )
        except Exception as e:
            logger.warning("[orchestrator] final memory compression failed: %s", e)

    def _invoke_llm_with_retry(
        self,
        model_with_tools,
        messages: list,
        tools: list,
        *,
        mission_id: str,
        round_no: int,
        llm_timeout: int = 120,
        max_retries: int = 10,
    ) -> tuple[AIMessage | None, Any]:
        """Invoke LLM with retry and model failover.

        1. Try current model up to max_retries times (llm_timeout per call)
        2. On exhaustion, switch to next priority model from pool
        3. Only shows UI events on timeout/error (silent on success)
        Returns (AIMessage, new_model_with_tools) — new_model is non-None when fallback succeeded.
        """
        current_model = model_with_tools
        model_name = getattr(current_model, "model_name", None) or getattr(current_model, "model", "unknown")

        for attempt in range(1, max_retries + 1):
            if self.store.should_stop(mission_id):
                return None, None
            pool = ThreadPoolExecutor(max_workers=1)
            try:
                future = pool.submit(current_model.invoke, messages)
                response: AIMessage = future.result(timeout=llm_timeout)
                pool.shutdown(wait=False)
                return response, None  # success with original model
            except FutureTimeout:
                pool.shutdown(wait=False)
                err_msg = f"LLM响应超时 ({llm_timeout}s), 第{attempt}/{max_retries}次重试 | model={model_name}"
                logger.warning("[orchestrator] LLM timeout attempt %d/%d model=%s", attempt, max_retries, model_name)
            except Exception as e:
                pool.shutdown(wait=False)
                detail = format_llm_error(e, model=str(model_name), messages=messages)
                err_msg = f"LLM错误 第{attempt}/{max_retries}次重试 | {detail}"
                logger.warning("[orchestrator] LLM error attempt %d/%d: %s", attempt, max_retries, detail)

            # Show retry event in UI only after 2+ consecutive failures (reduce noise)
            if attempt >= 2:
                self.store.add_event(
                    mission_id=mission_id,
                    round_no=round_no,
                    event_type="warning",
                    title=f"LLM重试 {attempt}/{max_retries}",
                    content=err_msg[:4000],
                )
            # Backoff with stop signal check (1s granularity)
            for _ in range(min(attempt * 2, 10)):
                if self.store.should_stop(mission_id):
                    return None, None
                time.sleep(1)

        # All retries exhausted — try fallback model
        logger.warning("[orchestrator] all %d retries exhausted, attempting model failover", max_retries)
        fallback_model = self._get_fallback_model(tools)
        if fallback_model:
            fallback_bound, fallback_name = fallback_model
            self.store.add_event(
                mission_id=mission_id,
                round_no=round_no,
                event_type="warning",
                title=f"切换备用模型: {fallback_name}",
                content=f"主模型连续{max_retries}次失败，切换到 {fallback_name}（后续请求将持续使用此模型）",
            )
            for attempt in range(1, 4):
                pool = ThreadPoolExecutor(max_workers=1)
                try:
                    future = pool.submit(fallback_bound.invoke, messages)
                    response = future.result(timeout=llm_timeout)
                    pool.shutdown(wait=False)
                    return response, fallback_bound  # fallback succeeded — caller must persist
                except Exception as e:
                    pool.shutdown(wait=False)
                    detail = format_llm_error(e, model=fallback_name, messages=messages)
                    logger.warning("[orchestrator] fallback model attempt %d/3: %s", attempt, detail)
                    time.sleep(5)

        # Complete failure
        self.store.add_event(
            mission_id=mission_id,
            round_no=round_no,
            event_type="error",
            title="LLM完全失败",
            content="所有模型均无法响应",
        )
        return None, None

    def _get_fallback_model(self, tools: list):
        """Get the next available model from the pool (by priority).
        Returns (model_with_tools, model_name) or None."""
        current_model_name = self.settings.llm_model
        sorted_pool = sorted(self.settings.model_pool, key=lambda m: m.priority)
        for entry in sorted_pool:
            if entry.model == current_model_name:
                continue  # skip the failed model
            try:
                fallback = self.llm.create_tool_model_for(
                    entry.base_url, entry.api_key, entry.model,
                )
                return fallback.bind_tools(tools), entry.model
            except Exception:
                continue
        return None

    def _run_mission(self, mission_id: str) -> None:
        mission = self.store.get_mission(mission_id)
        if not mission:
            return

        # Allocate a dedicated sandbox for this mission
        mission_sandbox = self._allocate_sandbox(mission_id)

        self.store.update_mission_status(mission_id, "running")
        self.store.add_event(
            mission_id=mission_id,
            round_no=0,
            event_type="system",
            title="任务启动",
            content=f"mission={mission['name']} target={mission['target']} model={mission['model']} sandbox={mission_sandbox._container}",
        )

        try:
            kb_stats = self.knowledge.ensure_ready()
            self.store.add_event(
                mission_id=mission_id,
                round_no=0,
                event_type="knowledge",
                title="知识库就绪",
                content=f"docs={kb_stats.get('total_docs', 0)} domains={kb_stats.get('domains', {})}",
                metadata=kb_stats,
            )
            sandbox_check = mission_sandbox.ensure_workspace()
            self.store.add_event(
                mission_id=mission_id,
                round_no=0,
                event_type="sandbox",
                title="Sandbox 健康检查",
                content=sandbox_check.to_log_text(),
                command=sandbox_check.command,
                exit_code=sandbox_check.exit_code,
                started_at=sandbox_check.started_at,
                ended_at=sandbox_check.ended_at,
            )
            # Collect sandbox environment info once and cache for prompt injection
            env_info = self._collect_env_info(mission_id, sandbox=mission_sandbox)
            # Delegate to tool-use loop
            self._run_mission_tool_use(mission_id, mission, env_info=env_info, sandbox=mission_sandbox)
        except Exception as exc:
            logger.exception("[orchestrator] mission %s crashed", mission_id)
            self.store.update_mission_status(mission_id, "error", error_message=str(exc))
            self.store.add_event(
                mission_id=mission_id,
                round_no=0,
                event_type="error",
                title="运行异常",
                content=repr(exc),
            )
        finally:
            # Cleanup thread reference, meta, and sandbox allocation
            self._release_sandbox(mission_id)
            with self._lock:
                self._threads.pop(mission_id, None)
            self._mission_meta.pop(mission_id, None)

    def _check_mission_timeout(
        self,
        *,
        mission_id: str,
        round_no: int,
        mission_start_time: float,
        mission_timeout_sec: int,
    ) -> bool:
        if mission_timeout_sec <= 0:
            return False

        mission_elapsed = time.monotonic() - mission_start_time
        if mission_elapsed <= mission_timeout_sec:
            return False

        self.store.add_event(
            mission_id=mission_id,
            round_no=round_no,
            event_type="warning",
            title="Mission 总超时",
            content=f"任务已运行 {int(mission_elapsed)}s（上限 {mission_timeout_sec}s），强制结束",
        )
        logger.warning(
            "[orchestrator] mission %s total timeout after %ds (limit %ds)",
            mission_id[:8],
            int(mission_elapsed),
            mission_timeout_sec,
        )
        self.store.update_mission_status(mission_id, "timeout")
        return True

    @staticmethod
    def _build_round_user_message(round_no: int, stall_rounds: int, target: str) -> str:
        if stall_rounds >= 2:
            return (
                f"[连续 {stall_rounds} 轮无新发现]\n"
                "请**重新评估攻击方向**，选择一个全新的思路。\n"
                "如果不确定该尝试什么，调用 ask_adviser 获取建议。"
            )
        if round_no == 1:
            return f"开始第 {round_no} 轮渗透。目标: {target}。"
        return f"第 {round_no} 轮开始，上一轮记忆已压缩注入系统提示，继续利用。"

    def _record_command_event(
        self,
        *,
        mission_id: str,
        round_no: int,
        tool_name: str,
        display_cmd: str,
        truncated_result: str,
        result_str: str,
        running_event_id: int | None,
    ) -> None:
        content = f"{display_cmd}\n\n---OUTPUT---\n{truncated_result}"
        exit_code = 0 if "[EXIT_CODE: 0]" in result_str else -1
        if running_event_id:
            self.store.finalize_event(
                running_event_id,
                event_type="command",
                title=f"[{tool_name}]",
                content=content,
                command=str(display_cmd)[:1000],
                exit_code=exit_code,
            )
            return

        self.store.add_event(
            mission_id=mission_id,
            round_no=round_no,
            event_type="command",
            title=f"[{tool_name}]",
            content=content,
            command=str(display_cmd)[:1000],
            exit_code=exit_code,
        )

    def _run_mission_tool_use(
        self,
        mission_id: str,
        mission: dict[str, Any],
        *,
        env_info: str = "",
        sandbox: SandboxExecutor | None = None,
    ) -> None:
        """Core tool-calling loop: model calls tools natively until done."""
        sbx = sandbox or self.sandbox
        max_rounds = mission["max_rounds"]
        max_tool_calls_per_round = mission["max_commands"]
        stdout_limit = self.settings.stdout_limit
        mission_workdir = f"{self.settings.sandbox_workdir}/{mission_id[:8]}"
        sbx.run(f"mkdir -p {mission_workdir}", workdir=self.settings.sandbox_workdir)

        memory: dict[str, Any] = self.store.get_memory(mission_id)

        # Per-mission model override: if mission uses a model from the pool,
        # create a dedicated tool model instead of the global one
        mission_model = mission.get("model", "")
        tool_model = self.llm.get_tool_model()
        if mission_model and mission_model != "mock":
            entry = self.settings.get_model_by_model_name(mission_model)
            if entry:
                try:
                    tool_model = self.llm.create_tool_model_for(
                        entry.base_url, entry.api_key, entry.model,
                    )
                    logger.info("[orchestrator] mission %s using per-mission model: %s",
                                mission_id[:8], entry.model)
                except Exception:
                    logger.warning("[orchestrator] failed to create per-mission model, using default")
                    tool_model = self.llm.get_tool_model()

        # Track if tool model is Anthropic (enables prompt caching via cache_control)
        _is_anthropic = LLMClient.is_anthropic_model(tool_model)

        # Stall detection: semantic comparison across rounds
        _stall_rounds: int = 0

        # Mission-level total timeout (0 = no limit)
        meta = self._mission_meta.get(mission_id, {})
        mission_timeout_sec: int = meta.get("mission_timeout_sec", 0)
        mission_start_time = time.monotonic()

        expected_flags = mission.get("expected_flags", 1)
        flag_captured = threading.Event()
        captured_flags: list[str] = []

        for round_no in range(1, max_rounds + 1):
            if self.store.should_stop(mission_id):
                self.store.update_mission_status(mission_id, "stopped")
                return

            if self._check_mission_timeout(
                mission_id=mission_id,
                round_no=round_no,
                mission_start_time=mission_start_time,
                mission_timeout_sec=mission_timeout_sec,
            ):
                return

            mission = self.store.get_mission(mission_id) or mission
            memory = self.store.get_memory(mission_id)

            # Build STABLE system prompt (rules/tools/goal/env — does NOT change within a mission)
            # Volatile context (memory/round/flags) goes into a separate HumanMessage
            # so the system prompt prefix stays identical → API prompt caching kicks in
            system_prompt = build_tool_system_prompt(
                mission=mission,
                env_info=env_info,
                mission_workdir=mission_workdir,
                public_ip=self.settings.sandbox_public_ip,
            )
            volatile_context = build_volatile_context(
                round_no=round_no,
                memory=memory,
                captured_flags=captured_flags,
                expected_flags=mission.get("expected_flags", 1),
            )
            tool_call_log: list[dict[str, Any]] = []

            def on_flag(flag: str) -> str:
                if flag in captured_flags:
                    return f"[FLAG_DUPLICATE] {flag} 已提交过"
                captured_flags.append(flag)
                remaining = max(0, expected_flags - len(captured_flags))
                self.store.add_event(
                    mission_id=mission_id,
                    round_no=round_no,
                    event_type="flag",
                    title="Flag 捕获",
                    content=f"{flag} ({len(captured_flags)}/{expected_flags})",
                )
                if remaining == 0:
                    flag_captured.set()
                    return f"[FLAG_CAPTURED] {flag} — 已找到全部 {expected_flags} 个flag！任务完成。"
                return f"[FLAG_CAPTURED] {flag} — 还需要找到 {remaining} 个flag，继续渗透！"

            def on_give_up(reason: str) -> str:
                self.store.add_event(
                    mission_id=mission_id,
                    round_no=round_no,
                    event_type="system",
                    title="🏳️ AI 主动放弃",
                    content=f"原因: {reason}",
                )
                self.store.request_stop(mission_id)
                return "[GIVE_UP] 已标记放弃，任务将停止。"

            # Streaming state: event_id updated per tool call so on_chunk knows where to write
            _streaming: dict[str, Any] = {"event_id": None, "display_cmd": ""}
            _streaming_lock = threading.Lock()

            def _on_chunk(partial_stdout: str) -> None:
                with _streaming_lock:
                    eid = _streaming.get("event_id")
                    display_cmd = _streaming.get("display_cmd", "")
                if eid:
                    self.store.update_event_content(
                        eid,
                        f"{display_cmd}\n\n---LIVE OUTPUT (partial)---\n{partial_stdout[-3000:]}",
                    )

            # Start fresh conversation for this round
            if _stall_rounds >= 2:
                # P0-3: Recover forgotten context from event log before cleaning
                try:
                    forgotten = retrieve_forgotten_context(self.store, mission_id, memory)
                    if forgotten:
                        # Inject recovered context into memory leads
                        existing_leads = list(memory.get("leads", []))
                        for item in forgotten:
                            if item not in existing_leads:
                                existing_leads.append(f"[恢复] {item}")
                        memory["leads"] = existing_leads[-12:]  # cap at 12
                        self.store.set_memory(mission_id, memory)
                        self.store.add_event(
                            mission_id=mission_id,
                            round_no=round_no,
                            event_type="system",
                            title=f"遗忘上下文恢复 (+{len(forgotten)}条)",
                            content="\n".join(forgotten),
                        )
                except Exception as recover_err:
                    logger.warning("[orchestrator] forgotten context recovery failed: %s", recover_err)

                # P0-4: Memory cleaning (skip if disabled in config)
                if not self.settings.disable_memory_cleaning:
                    cleaning_prompt = build_memory_cleaning_prompt(
                        mission=mission,
                        current_memory=memory,
                        stall_rounds=_stall_rounds,
                    )
                    try:
                        pool = ThreadPoolExecutor(max_workers=1)
                        try:
                            future = pool.submit(self.llm.invoke_memory, cleaning_prompt, memory)
                            cleaning_result = future.result(timeout=self.settings.llm_timeout_sec)
                        finally:
                            pool.shutdown(wait=False)
                        cleaned_memory = normalize_memory_enhanced(cleaning_result.payload, memory)
                        memory = cleaned_memory
                        self.store.set_memory(mission_id, memory)
                        self.store.add_event(
                            mission_id=mission_id,
                            round_no=round_no,
                            event_type="system",
                            title=f"记忆清洗完成 (stall={_stall_rounds})",
                            content=_compact_json(memory),
                        )
                        # Rebuild volatile context with cleaned memory (system prompt stays stable)
                        volatile_context = build_volatile_context(
                            round_no=round_no,
                            memory=memory,
                            captured_flags=captured_flags,
                            expected_flags=mission.get("expected_flags", 1),
                        )
                    except Exception as clean_err:
                        logger.warning("[orchestrator] memory cleaning failed: %s", clean_err)

            user_msg = self._build_round_user_message(round_no, _stall_rounds, mission["target"])

            # Define messages first so tools can capture it by reference
            # messages[0] = SystemMessage (STABLE, never changes within mission → cache-friendly)
            # messages[1] = HumanMessage (volatile context + user instruction)
            # For Anthropic: use content block format with cache_control for prompt caching
            if _is_anthropic:
                sys_msg = SystemMessage(content=[
                    {"type": "text", "text": system_prompt, "cache_control": {"type": "ephemeral"}}
                ])
            else:
                sys_msg = SystemMessage(content=system_prompt)
            messages: list[Any] = [
                sys_msg,
                HumanMessage(content=f"{volatile_context}\n\n---\n\n{user_msg}"),
            ]

            tools = create_all_tools(
                sandbox=sbx,
                workdir=mission_workdir,
                store=self.store,
                llm_client=self.llm,
                mission=mission,
                memory=memory,
                on_flag=on_flag,
                on_give_up=on_give_up,
                stop_fn=lambda: self.store.should_stop(mission_id),
                on_chunk=_on_chunk,
                knowledge_top_k=self.settings.knowledge_top_k,
                current_messages=messages,
                command_timeout_sec=self.settings.command_timeout_sec,
            )
            tool_map = {t.name: t for t in tools}
            model_with_tools = tool_model.bind_tools(tools)

            llm_call_count = 0  # number of LLM invocations this round (one call = one AI "turn")
            tool_exec_count = 0  # total individual tool executions this round (for logging)
            consecutive_no_tool = 0
            round_start_time = time.monotonic()
            round_timeout_sec = mission.get("round_timeout_sec", self.settings.round_timeout_sec)

            self.store.add_event(
                mission_id=mission_id,
                round_no=round_no,
                event_type="system",
                title=f"Round {round_no} 开始",
                content=f"max_llm_calls_per_round={max_tool_calls_per_round}",
            )

            while llm_call_count < max_tool_calls_per_round:
                if self.store.should_stop(mission_id):
                    self.store.update_mission_status(mission_id, "stopped")
                    return
                if flag_captured.is_set():
                    break
                # Round-level timeout
                elapsed = time.monotonic() - round_start_time
                if elapsed > round_timeout_sec:
                    self.store.add_event(
                        mission_id=mission_id,
                        round_no=round_no,
                        event_type="warning",
                        title=f"Round {round_no} 超时",
                        content=f"本轮已运行 {int(elapsed)}s（上限 {round_timeout_sec}s），强制进入下一轮",
                    )
                    logger.warning("[orchestrator] round %d timed out after %ds", round_no, int(elapsed))
                    break

                response, new_model = self._invoke_llm_with_retry(
                    model_with_tools, messages, tools,
                    mission_id=mission_id,
                    round_no=round_no,
                    llm_timeout=self.settings.llm_timeout_sec,
                    max_retries=self.settings.llm_max_retries,
                )
                if new_model is not None:
                    model_with_tools = new_model  # persist fallback for rest of mission
                    # Update Anthropic flag (fallback model may be a different provider)
                    _is_anthropic = LLMClient.is_anthropic_model(
                        getattr(new_model, 'bound', new_model)
                    )
                if response is None:
                    break

                llm_call_count += 1
                messages.append(response)

                # Log AI response text
                response_text = response.content if isinstance(response.content, str) else str(response.content)
                if response_text.strip():
                    self.store.add_event(
                        mission_id=mission_id,
                        round_no=round_no,
                        event_type="main_agent",
                        title=f"Round {round_no} AI [对话 {llm_call_count}]",
                        content=response_text[:4000],
                    )

                if not response.tool_calls:
                    consecutive_no_tool += 1
                    if consecutive_no_tool >= 5:
                        # Model made 5 consecutive responses without calling tools — round done
                        break
                    if consecutive_no_tool >= 2:
                        # Inject a forceful reminder to call tools after 2 idle turns
                        messages.append(HumanMessage(content=(
                            "[系统强制提醒] 你已连续输出纯文本而未调用任何工具，这违反了核心规则。"
                            "你是自主agent，没有人在看你的文本输出。"
                            "立即调用一个工具（bash_exec/python_exec/knowledge_search/ask_adviser等）继续推进攻击。"
                            "如果不确定下一步，调用 ask_adviser 向专家顾问求助。"
                        )))
                    continue
                consecutive_no_tool = 0

                # Execute each tool call in this response
                # IMPORTANT: All ToolMessages must be adjacent after AIMessage —
                # inserting HumanMessage between them causes Claude 400 errors.
                deferred_guidance: list[str] = []
                for tc in response.tool_calls:
                    tool_name = tc.get("name", "")
                    tool_args = tc.get("args", {})
                    tool_id = tc.get("id", f"tc_{tool_exec_count}")

                    # Extract the primary payload for display (full command/code/question)
                    display_cmd = (
                        tool_args.get("command")
                        or tool_args.get("code")
                        or tool_args.get("question")
                        or tool_args.get("query")
                        or tool_args.get("flag")
                        or _compact_json(tool_args)
                    )

                    if tool_name in tool_map:
                        try:
                            # Show "running" indicator immediately so user sees the command
                            running_event_id = self.store.add_event(
                                mission_id=mission_id,
                                round_no=round_no,
                                event_type="command_running",
                                title=f"[{tool_name}] running",
                                content=str(display_cmd),
                                command=str(display_cmd)[:500],
                            )
                            # Wire streaming: on_chunk will update this event with partial output
                            with _streaming_lock:
                                _streaming["event_id"] = running_event_id
                                _streaming["display_cmd"] = str(display_cmd)
                            try:
                                tool_result = tool_map[tool_name].invoke(tool_args)
                            finally:
                                with _streaming_lock:
                                    _streaming["event_id"] = None
                        except Exception as tool_err:
                            tool_result = f"[tool error] {tool_err}"
                    else:
                        running_event_id = None
                        tool_result = f"[unknown tool: {tool_name}]"

                    result_str = str(tool_result)
                    truncated_result = _truncate_middle(result_str, stdout_limit)
                    self._record_command_event(
                        mission_id=mission_id,
                        round_no=round_no,
                        tool_name=tool_name,
                        display_cmd=str(display_cmd),
                        truncated_result=truncated_result,
                        result_str=result_str,
                        running_event_id=running_event_id,
                    )

                    messages.append(ToolMessage(content=truncated_result, tool_call_id=tool_id))

                    # Defer timeout guidance — cannot insert HumanMessage between ToolMessages
                    if "[TIMEOUT" in result_str:
                        deferred_guidance.append(
                            f"命令 `{str(display_cmd)[:100]}` 已超时。"
                            "考虑：缩小扫描范围、使用更快的工具、"
                            "或后台运行（nohup ... &）后用 tail 检查结果。"
                        )

                    tool_call_log.append({
                        "tool": tool_name,
                        "args_summary": str(display_cmd)[:300],
                        "result_summary": result_str[:500],
                    })
                    tool_exec_count += 1

                    if flag_captured.is_set():
                        break

                # Now safe to inject deferred guidance after ALL ToolMessages
                if deferred_guidance:
                    messages.append(HumanMessage(content="\n".join(deferred_guidance)))

                # Mid-round context monitoring: if messages are getting too large,
                # use LLM compression (if available) or fallback to importance-based scoring
                _CONTEXT_COMPRESS_THRESHOLD = self.settings.context_compress_threshold
                msg_size = _estimate_messages_size(messages)
                if msg_size > _CONTEXT_COMPRESS_THRESHOLD and len(messages) > 6:
                    # Selective compression: keep SystemMessage + recent tail intact.
                    # IMPORTANT: tail must start at a valid message boundary (not ToolMessage
                    # without its parent AIMessage), or LLM APIs will reject the conversation.
                    kept_head = 2  # SystemMessage + volatile context HumanMessage
                    kept_tail = 4  # recent context
                    # Adjust tail boundary: walk backwards to find a non-ToolMessage start
                    tail_start = len(messages) - kept_tail
                    while tail_start > kept_head + 1 and isinstance(messages[tail_start], ToolMessage):
                        tail_start -= 1  # include the parent AIMessage
                    middle = messages[kept_head:tail_start]
                    if not middle:
                        continue  # nothing to compress

                    compressed_summary = None

                    # Strategy 1: LLM-based compression (cheap model)
                    if self.llm.has_compression_model:
                        try:
                            middle_text = "\n---\n".join(
                                str(m.content if hasattr(m, "content") else m)[:1500]
                                for m in middle
                            )
                            # Cap input to compression model at ~30K chars
                            if len(middle_text) > 30000:
                                middle_text = middle_text[:30000] + "\n...[truncated]"
                            mission_ctx = f"目标: {mission.get('target', '?')} | 任务: {mission.get('goal', '?')[:200]}"
                            pool = ThreadPoolExecutor(max_workers=1)
                            try:
                                future = pool.submit(
                                    self.llm.invoke_compression, middle_text, mission_ctx
                                )
                                llm_summary = future.result(timeout=self.settings.compression_timeout_sec or 45)
                            except (FutureTimeout, TimeoutError):
                                logger.warning("[orchestrator] LLM compression timed out after %ds", self.settings.compression_timeout_sec)
                                future.cancel()
                                llm_summary = None
                            finally:
                                pool.shutdown(wait=False, cancel_futures=True)
                            if llm_summary and len(llm_summary) > 50:
                                compressed_summary = (
                                    f"[上下文已由压缩模型智能压缩]\n"
                                    f"压缩了 {len(middle)} 条消息（原始约 {msg_size} 字符）。\n"
                                    f"摘要：\n{llm_summary}"
                                )
                                logger.info(
                                    "[orchestrator] LLM compression: %d chars → %d chars",
                                    msg_size, len(compressed_summary),
                                )
                        except Exception as comp_err:
                            logger.warning("[orchestrator] LLM compression failed, using fallback: %s", comp_err)

                    # Strategy 2: Fallback — importance-based truncation
                    if compressed_summary is None:
                        compressed_parts = []
                        for m in middle:
                            content = m.content if hasattr(m, "content") else str(m)
                            text = str(content) if not isinstance(content, str) else content
                            importance = score_importance(text)
                            if importance >= 3:
                                compressed_parts.append(text[:800] + ("..." if len(text) > 800 else ""))
                            elif importance >= 2:
                                compressed_parts.append(text[:400] + ("..." if len(text) > 400 else ""))
                            else:
                                compressed_parts.append(text[:200] + ("..." if len(text) > 200 else ""))
                        compressed_summary = (
                            "[上下文过大，中间对话已按重要性压缩]\n"
                            f"压缩了 {len(middle)} 条消息（原始约 {msg_size} 字符）。\n"
                            "摘要：\n" + "\n".join(f"- {s}" for s in compressed_parts[-15:])
                        )

                    messages = (
                        messages[:kept_head]
                        + [HumanMessage(content=compressed_summary)]
                        + messages[tail_start:]
                    )
                    logger.info(
                        "[orchestrator] mid-round context compression: %d chars → %d chars",
                        msg_size, _estimate_messages_size(messages),
                    )
                    self.store.add_event(
                        mission_id=mission_id,
                        round_no=round_no,
                        event_type="system",
                        title="轮内上下文压缩",
                        content=f"消息总长 {msg_size} 字符超过阈值 {_CONTEXT_COMPRESS_THRESHOLD}，已压缩 {len(middle)} 条中间消息",
                    )

            # === End of tool-calling loop ===

            if flag_captured.is_set():
                flags = ", ".join(captured_flags)
                self.store.update_mission_status(mission_id, "done")
                self.store.add_event(
                    mission_id=mission_id,
                    round_no=round_no,
                    event_type="system",
                    title="任务完成",
                    content=f"Flag(s) captured: {flags}",
                )
                # Final memory compression for DA analysis
                self._do_final_memory_compression(
                    mission_id, mission, memory, round_no, tool_call_log, "success"
                )
                return

            # Memory compression at end of each round
            memory_prompt = build_tool_memory_prompt(
                mission=mission,
                previous_memory=memory,
                round_no=round_no,
                tool_call_log=tool_call_log,
            )
            try:
                pool = ThreadPoolExecutor(max_workers=1)
                try:
                    future = pool.submit(self.llm.invoke_memory, memory_prompt, memory)
                    memory_result = future.result(timeout=self.settings.llm_timeout_sec)
                finally:
                    pool.shutdown(wait=False)
                new_memory = normalize_memory_enhanced(memory_result.payload, memory)
            except Exception as mem_err:
                logger.warning("[orchestrator] memory compression failed: %s", mem_err)
                new_memory = memory
            self.store.set_memory(mission_id, new_memory)
            self.store.add_event(
                mission_id=mission_id,
                round_no=round_no,
                event_type="memory_agent",
                title=f"Round {round_no} 记忆压缩",
                content=_compact_json(new_memory),
            )

            # Stall detection: semantic comparison instead of fragile hash
            if detect_stall(new_memory, memory):
                _stall_rounds += 1
            else:
                _stall_rounds = 0

            if _stall_rounds > 0:
                self.store.add_event(
                    mission_id=mission_id,
                    round_no=round_no,
                    event_type="system",
                    title=f"停滞检测: 连续 {_stall_rounds} 轮无新发现",
                    content=f"stall_rounds={_stall_rounds}, 下轮{'将触发记忆清洗' if _stall_rounds >= 2 else '继续正常'}",
                )

            if llm_call_count == 0:
                self.store.add_event(
                    mission_id=mission_id,
                    round_no=round_no,
                    event_type="error",
                    title="空转警告",
                    content="本轮没有任何工具调用，检查 LLM 响应或 API 连接。",
                )

        self.store.update_mission_status(
            mission_id, "stopped",
            error_message="达到最大轮次，任务未找到 flag。",
        )
        self.store.add_event(
            mission_id=mission_id,
            round_no=max_rounds,
            event_type="system",
            title="达到最大轮次",
            content="已跑满 max_rounds，任务停止。",
        )
        # Final memory compression for DA analysis
        self._do_final_memory_compression(
            mission_id, mission, memory, max_rounds, tool_call_log, "max_rounds"
        )
