from __future__ import annotations

import json
import logging
import re
import threading
import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeout
from typing import Any

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage

from pikaqiu_agent.config import AgentSettings, MAX_AGENT_SLOTS
from pikaqiu_agent import flag_capture as _flag_capture
from pikaqiu_agent import experience as _experience
from pikaqiu_agent.knowledge import KnowledgeIndexer
from pikaqiu_agent.llm_client import LLMClient, format_llm_error
from pikaqiu_agent.memory import normalize_memory_enhanced, detect_stall, score_importance, retrieve_forgotten_context
from pikaqiu_agent.observer import ObserverAgent, ObserverDecision, should_inject_decision
from pikaqiu_agent.observer_runtime import ObserverRuntime
from pikaqiu_agent.prompts import (
    build_tool_system_prompt,
    build_volatile_context,
    build_tool_memory_prompt,
    build_memory_cleaning_prompt,
)
from pikaqiu_agent.sandbox import SandboxExecutor
from pikaqiu_agent.skill_loader import SkillLoader
from pikaqiu_agent.storage import MissionStore
from pikaqiu_agent import success_guards as _success_guards
from pikaqiu_agent.tools import create_all_tools

logger = logging.getLogger(__name__)

_EXIT_CODE_RE = re.compile(r"\[EXIT_CODE:\s*(-?\d+)\]")


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


# Keep older private imports pointed at the dependency-light implementation.
_truncate_middle = _flag_capture.truncate_middle
_is_placeholder_flag = _flag_capture.is_placeholder_flag
_extract_flag_candidates = _flag_capture.extract_flag_candidates
_trusted_tool_flag_candidates = _flag_capture.trusted_tool_flag_candidates
_append_flag_candidate_summary = _flag_capture.append_flag_candidate_summary
_auto_capture_trusted_flags = _flag_capture.auto_capture_trusted_flags
_is_scan_like_tool_call = _success_guards.is_scan_like_tool_call
_is_broad_scan_tool_call = _success_guards.is_broad_scan_tool_call
_highest_value_lead = _success_guards.highest_value_lead
_next_verification_hint = _success_guards.next_verification_hint
_summarize_guidance_result = _success_guards.summarize_guidance_result
_round_time_guidance = _success_guards.round_time_guidance
_route_guard_guidance = _success_guards.route_guard_guidance
_post_partial_flag_guidance = _success_guards.post_partial_flag_guidance
_broad_scan_block_message = _success_guards.broad_scan_block_message
_mission_scan_cooldown_blocks = _success_guards.mission_scan_cooldown_blocks
_missing_tool_name = _success_guards.missing_tool_name
_known_missing_tool_blocks = _success_guards.known_missing_tool_blocks
_missing_tools_from_memory = _success_guards.missing_tools_from_memory
_missing_tool_block_message = _success_guards.missing_tool_block_message
_low_evidence_stop_block_message = _success_guards.low_evidence_stop_block_message
_stale_observer_steer_block_message = _success_guards.stale_observer_steer_block_message


def _tool_result_timed_out(row: dict[str, Any]) -> bool:
    return "[TIMEOUT" in str(row.get("result_full") or row.get("result_summary") or "")


def _observer_result_view(text: str, limit: int = 20000) -> str:
    """Return a head+tail view for Observer route audit.

    The tail often contains exit codes, stderr, final status, and flags, so a
    prefix-only summary is too lossy for supervision.
    """
    text = str(text or "")
    if len(text) <= limit:
        return text
    marker = f"\n\n... [observer view truncated {len(text) - limit} chars] ...\n\n"
    head_size = max(1000, int(limit * 0.35))
    tail_size = max(1000, limit - head_size - len(marker))
    return text[:head_size] + marker + text[-tail_size:]


def _asset_access_capabilities(
    *,
    mission: dict[str, Any],
    env_info: str,
    mission_workdir: str,
) -> dict[str, Any]:
    capabilities = {
        "blackbox_target_access": bool(str(mission.get("target") or "").strip()),
        "challenge_workdir": mission_workdir,
        "sandbox_env_info_available": bool(str(env_info or "").strip()),
        "source_access": "unknown",
        "container_access": "sandbox_executor",
        "mounted_volume_access": "unknown",
        "database_access": "unknown",
        "environment_variable_access": "sandbox_env_info" if env_info else "unknown",
        "startup_chain_access": "unknown",
        "use_policy": (
            "Start with black-box evidence. When blocked, use available asset views only to close "
            "the missing evidence boundary; do not hard-code target traits or treat asset access as a direct flag shortcut."
        ),
    }
    scope = str(mission.get("scope") or "")
    if scope:
        capabilities["declared_scope"] = scope
    return capabilities


def _tool_call_memory_view(tool_call_log: list[dict[str, Any]], *, limit: int = 30) -> list[dict[str, Any]]:
    rows = tool_call_log[-limit:]
    return [
        {
            "tool": row.get("tool"),
            "args_summary": row.get("args_summary"),
            "result_summary": row.get("result_summary"),
            "result_len": row.get("result_len"),
            "exit_code": row.get("exit_code"),
        }
        for row in rows
    ]


def _is_benign_sigpipe(display_cmd: str, result_str: str, exit_code: int) -> bool:
    """Treat common help-output truncation as success.

    Commands like `tool -h | head -40` can make the producer exit with
    SIGPIPE after `head` closes the pipe. With `set -o pipefail`, bash returns
    141 even though the requested preview was produced successfully.
    """
    if exit_code != 141:
        return False
    cmd = display_cmd.lower()
    if "|" not in cmd or "head" not in cmd:
        return False
    return "[stderr]" not in result_str.lower()


def _infer_tool_exit_code(result_str: str, display_cmd: str = "") -> int:
    """Infer event success for both sandbox commands and in-process tools.

    Sandbox-backed tools include an explicit [EXIT_CODE: n] marker. In-process
    tools such as skill_search return structured JSON without that marker, so
    absence of [EXIT_CODE: 0] must not be treated as failure.
    """
    match = _EXIT_CODE_RE.search(result_str)
    if match:
        try:
            exit_code = int(match.group(1))
        except ValueError:
            return -1
        if _is_benign_sigpipe(display_cmd, result_str, exit_code):
            return 0
        return exit_code

    lowered = result_str.lower()
    error_markers = (
        "[tool error]",
        "[unknown tool:",
        "[knowledge_search error]",
        "[search_cve error]",
        "[skill_read_reference error]",
    )
    if any(marker in lowered for marker in error_markers):
        return -1

    text = result_str.strip()
    if text.startswith("{"):
        try:
            payload = json.loads(text)
        except json.JSONDecodeError:
            payload = {}
        if isinstance(payload, dict):
            if payload.get("ok") is False:
                return -1
            top_error = payload.get("error")
            if isinstance(top_error, str) and top_error.strip():
                return -1
            if top_error and not isinstance(top_error, (list, dict)):
                return -1

    return 0


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


def _observer_should_inject(decision: ObserverDecision, *, phase: str) -> bool:
    """Keep Observer low-noise: UI/event memory always records it, but main-agent
    injection is reserved for stop-the-line issues or clear stalls."""
    return should_inject_decision(decision, phase=phase)


class OrchestratorManager:
    def __init__(
        self,
        settings: AgentSettings,
        store: MissionStore,
        knowledge: KnowledgeIndexer,
        sandbox: SandboxExecutor,
        llm: LLMClient,
        skills: SkillLoader | None = None,
    ) -> None:
        self.settings = settings
        self.store = store
        self.knowledge = knowledge
        self.sandbox = sandbox
        self.llm = llm
        self.skills = skills
        self._threads: dict[str, threading.Thread] = {}
        self._lock = threading.Lock()
        self._mission_meta: dict[str, dict] = {}  # mission_id -> extra params (e.g. mission_timeout_sec)
        self._sandbox_alloc: dict[str, SandboxExecutor] = {}
        containers = list(dict.fromkeys(settings.sandbox_containers or [settings.sandbox_container]))
        self._container_pool: list[str] = containers[:MAX_AGENT_SLOTS] or [settings.sandbox_container]
        self._container_usage: dict[str, str] = {container: "" for container in self._container_pool}
        self.observer = ObserverAgent()
        self.observer_runtime = ObserverRuntime(settings, store, llm, self.observer, skills=skills)

    def _allocate_sandbox(self, mission_id: str) -> SandboxExecutor:
        """Allocate a dedicated sandbox container for a mission."""
        with self._lock:
            existing = self._sandbox_alloc.get(mission_id)
            if existing:
                return existing
            for container, user in self._container_usage.items():
                if not user:
                    self._container_usage[container] = mission_id
                    executor = SandboxExecutor(self.settings, container_override=container)
                    self._sandbox_alloc[mission_id] = executor
                    logger.info("[sandbox-pool] allocated %s -> mission %s", container, mission_id[:8])
                    return executor
            raise RuntimeError("all agent slots are busy")

    def _release_sandbox(self, mission_id: str) -> None:
        """Release the sandbox allocated to a mission."""
        with self._lock:
            self._sandbox_alloc.pop(mission_id, None)
            for container, user in self._container_usage.items():
                if user == mission_id:
                    self._container_usage[container] = ""
                    logger.info("[sandbox-pool] released %s <- mission %s", container, mission_id[:8])
                    break

    def has_available_agent_slot(self) -> bool:
        with self._lock:
            return any(not mission_id for mission_id in self._container_usage.values())

    def agent_slots(self) -> list[dict[str, Any]]:
        with self._lock:
            usage = dict(self._container_usage)
            thread_alive = {
                mission_id: bool(self._threads.get(mission_id) and self._threads[mission_id].is_alive())
                for mission_id in usage.values()
                if mission_id
            }

        slots: list[dict[str, Any]] = []
        for index, container in enumerate(self._container_pool, start=1):
            mission_id = usage.get(container, "")
            mission = self.store.get_mission(mission_id) if mission_id else None
            captured_flags = mission.get("captured_flags", []) if mission else []
            captured_count = len(captured_flags)
            alive = bool(thread_alive.get(mission_id, False))
            if not mission_id or not mission:
                status = "idle"
                reason = "not_started"
            elif captured_count > 0:
                status = "idle"
                reason = "flag_captured"
            elif not alive:
                status = "idle"
                reason = "not_running"
            else:
                status = "running"
                reason = "running"
            slots.append({
                "slot": index,
                "agent_id": f"agent-{index}",
                "container": container,
                "status": status,
                "status_reason": reason,
                "allocated": bool(mission_id and mission),
                "mission_id": mission_id if mission else "",
                "mission_name": mission.get("name", "") if mission else "",
                "target": mission.get("target", "") if mission else "",
                "mission_status": mission.get("status", "") if mission else "",
                "captured_flag_count": captured_count,
                "thread_alive": alive,
            })
        return slots

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
        skills: list[str] | None = None,
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
        if not self.has_available_agent_slot():
            raise RuntimeError("all agent slots are busy")
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
            skills=skills or [],
        )
        try:
            self._allocate_sandbox(mission_id)
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
        except Exception:
            self._release_sandbox(mission_id)
            self._mission_meta.pop(mission_id, None)
            with self._lock:
                self._threads.pop(mission_id, None)
            self.store.delete_mission(mission_id)
            raise
        return mission_id

    def resume_mission(
        self,
        mission_id: str,
        *,
        extra_rounds: int,
        mission_timeout_sec: int = 0,
    ) -> dict[str, Any] | None:
        with self._lock:
            existing = self._threads.get(mission_id)
            if existing and existing.is_alive():
                raise RuntimeError("mission is already running")

        mission = self.store.get_mission(mission_id)
        if not mission:
            return None
        if mission["status"] in {"queued", "running"}:
            raise RuntimeError("mission is already queued or running")
        if not self.has_available_agent_slot():
            raise RuntimeError("all agent slots are busy")

        self._allocate_sandbox(mission_id)
        try:
            resumed = self.store.prepare_mission_resume(mission_id, extra_rounds)
            if not resumed:
                self._release_sandbox(mission_id)
                return None

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
                existing = self._threads.get(mission_id)
                if existing and existing.is_alive():
                    raise RuntimeError("mission is already running")
                self._threads[mission_id] = thread
            thread.start()
        except Exception:
            self._release_sandbox(mission_id)
            self._mission_meta.pop(mission_id, None)
            with self._lock:
                self._threads.pop(mission_id, None)
            raise
        return resumed

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
            flag_events = [
                event for event in self.store.get_events(mission_id)
                if event.get("type") == "flag"
            ]
            if flag_events:
                flags = self.store.get_captured_flags(mission_id)
                completion_finding = (
                    "mission_complete=true; captured_flags="
                    + ", ".join(flags)
                    + "; source_event_ids="
                    + ",".join(str(event.get("id")) for event in flag_events)
                )
                enriched_memory = dict(memory)
                findings = list(enriched_memory.get("findings") or [])
                if completion_finding not in findings:
                    findings.append(completion_finding)
                enriched_memory.update({
                    "mission_complete": True,
                    "captured_flags": flags,
                    "captured_flag_event_ids": [event.get("id") for event in flag_events],
                    "blocked_reason": "",
                    "findings": findings,
                })
                memory = enriched_memory
                self.store.add_event(
                    mission_id=mission_id,
                    round_no=round_no,
                    event_type="memory_agent",
                    title="Final completion context",
                    content=completion_finding,
                    metadata={
                        "mission_complete": True,
                        "captured_flags": flags,
                        "captured_flag_event_ids": [event.get("id") for event in flag_events],
                    },
                )
            memory_prompt = build_tool_memory_prompt(
                mission=mission,
                previous_memory=memory,
                round_no=round_no,
                tool_call_log=_tool_call_memory_view(tool_call_log),
            )
            pool = ThreadPoolExecutor(max_workers=1)
            try:
                future = pool.submit(self.llm.invoke_memory, memory_prompt, memory)
                memory_result = future.result(timeout=self.settings.llm_timeout_sec)
            finally:
                pool.shutdown(wait=False)
            new_memory = normalize_memory_enhanced(memory_result.payload, memory)
            if flag_events:
                new_memory["mission_complete"] = True
                new_memory["captured_flags"] = flags
                new_memory["captured_flag_event_ids"] = [event.get("id") for event in flag_events]
                new_memory["blocked_reason"] = ""
                findings = list(new_memory.get("findings") or [])
                if completion_finding not in findings:
                    findings.append(completion_finding)
                new_memory["findings"] = findings
            self.store.set_memory(mission_id, new_memory)
            self.store.add_event(
                mission_id=mission_id,
                round_no=round_no,
                event_type="memory_agent",
                title=f"最终记忆压缩 ({outcome})",
                content=_compact_json(new_memory),
            )
            if flag_events and outcome == "success":
                self._craft_success_experience(
                    mission_id=mission_id,
                    mission=mission,
                    memory=new_memory,
                    round_no=round_no,
                    tool_call_log=tool_call_log,
                )
        except Exception as e:
            logger.warning("[orchestrator] final memory compression failed: %s", e)

    def _build_experience_hints(
        self,
        mission: dict[str, Any],
        memory: dict[str, Any],
    ) -> str:
        try:
            query = _experience.build_experience_query(mission, memory)
            results = _experience.search_experience(
                self.settings.workspace_root,
                query,
                limit=5,
            )
            return _experience.format_experience_hints(results, limit=3)
        except Exception as e:
            logger.warning("[orchestrator] experience hint search failed: %s", e)
            return ""

    def _craft_success_experience(
        self,
        *,
        mission_id: str,
        mission: dict[str, Any],
        memory: dict[str, Any],
        round_no: int,
        tool_call_log: list[dict[str, Any]],
    ) -> None:
        flag_events = [event for event in self.store.get_events(mission_id) if event.get("type") == "flag"]
        if not flag_events:
            return
        mission_with_id = dict(mission)
        mission_with_id["id"] = mission_id
        flags = self.store.get_captured_flags(mission_id)
        prompt = (
            "Draft a human-reviewable experience craft from this successful authorized CTF/pentest mission.\n"
            "Use only the provided evidence. Do not invent payloads, vulnerability types, or commands.\n"
            "If a payload or command is not visible in evidence, write 'unknown from evidence'.\n\n"
            "Required Markdown sections:\n"
            "# Experience Craft\n"
            "source_mission_id: <mission id>\n"
            "review_status: pending_review\n"
            "confidence: high|medium|low\n\n"
            "## Vulnerability Type\n"
            "## Applicable Scenario\n"
            "## Key Entry Point\n"
            "## Successful Payload / Command Chain\n"
            "## Evidence Chain\n"
            "## Failed Paths\n"
            "## Reuse Rules\n\n"
            f"Mission:\n{_compact_json(mission_with_id, max_len=4000)}\n\n"
            f"Captured flags:\n{_compact_json(flags, max_len=2000)}\n\n"
            f"Flag events:\n{_compact_json(flag_events, max_len=6000)}\n\n"
            f"Final shared memory:\n{_compact_json(memory, max_len=10000)}\n\n"
            f"Recent tool calls:\n{_compact_json(_tool_call_memory_view(tool_call_log, limit=20), max_len=12000)}\n"
        )
        try:
            pool = ThreadPoolExecutor(max_workers=1)
            try:
                future = pool.submit(self.llm.invoke_experience_distill, prompt)
                markdown = future.result(timeout=min(self.settings.llm_timeout_sec, 60))
            finally:
                pool.shutdown(wait=False, cancel_futures=True)
            if "source_mission_id" not in markdown:
                markdown = f"source_mission_id: {mission_id}\nreview_status: pending_review\nconfidence: low\n\n{markdown}"
            path = _experience.write_experience_craft(
                self.settings.workspace_root,
                mission=mission_with_id,
                markdown=markdown,
            )
            self.store.add_event(
                mission_id=mission_id,
                round_no=round_no,
                event_type="knowledge",
                title="Experience craft written",
                content=str(path.relative_to(self.settings.workspace_root)),
                metadata={
                    "experience_craft_path": str(path),
                    "review_status": "pending_review",
                    "note": "Craft is not injected into the active experience index until human approval.",
                },
            )
        except Exception as e:
            logger.warning("[orchestrator] success experience craft failed: %s", e)
            self.store.add_event(
                mission_id=mission_id,
                round_no=round_no,
                event_type="warning",
                title="Experience craft failed",
                content=str(e)[:2000],
            )

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
                    reasoning_effort=entry.reasoning_effort,
                    use_responses_api=entry.use_responses_api,
                    disable_response_storage=entry.disable_response_storage,
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
        self.observer_runtime.ensure_session(mission_id)
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
                "如果不确定该尝试什么，回到已验证证据，优先用 knowledge_search/search_cve/web_search 或最小可观测探针推进。"
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
        exit_code = _infer_tool_exit_code(result_str, display_cmd)
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

    def _inject_human_guidance(
        self,
        *,
        mission_id: str,
        round_no: int,
        messages: list[Any],
    ) -> bool:
        guidance_items = self.store.consume_pending_human_guidance(mission_id)
        if not guidance_items:
            return False

        guidance_text = "\n".join(
            f"- {item['content']}" for item in guidance_items if str(item.get("content", "")).strip()
        )
        if not guidance_text.strip():
            return False

        injection = (
            "[HUMAN_GUIDANCE]\n"
            "The operator has provided high-priority guidance for this authorized mission.\n"
            "Before the next tool call, re-evaluate the current memory, revise the penetration path, "
            "and choose actions that align with the guidance. Stay within the mission scope and avoid "
            "repeating dead ends unless the guidance explicitly asks for it.\n\n"
            f"{guidance_text}\n"
            "[/HUMAN_GUIDANCE]"
        )
        messages.append(HumanMessage(content=injection))
        self.store.add_event(
            mission_id=mission_id,
            round_no=round_no,
            event_type="human_guidance",
            title=f"Human guidance injected ({len(guidance_items)})",
            content=guidance_text,
        )
        return True

    def _record_observer_decision(
        self,
        *,
        mission_id: str,
        round_no: int,
        decision: ObserverDecision,
        phase: str,
    ) -> None:
        decision = decision.normalised()
        if decision.severity == "none" and not decision.actionable:
            return
        self.store.add_event(
            mission_id=mission_id,
            round_no=round_no,
            event_type="observer_agent",
            title=f"Observer {phase}: {decision.state}/{decision.action}",
            content=self.observer.format_event_content(decision),
            metadata={"observer": decision.to_dict(), "phase": phase},
        )

    def _apply_observer_memory_patch(
        self,
        *,
        mission_id: str,
        round_no: int,
        memory: dict[str, Any],
        decision: ObserverDecision,
    ) -> dict[str, Any]:
        if not decision.memory_patch:
            return memory
        patched, changed = self.observer.apply_memory_patch(memory, decision.memory_patch)
        if changed:
            self.store.set_memory(mission_id, patched)
            patched = self.store.get_memory(mission_id)
            self.store.add_event(
                mission_id=mission_id,
                round_no=round_no,
                event_type="observer_agent",
                title="Observer memory sync applied",
                content=_compact_json(decision.memory_patch, max_len=2000),
                metadata={"observer_memory_patch": decision.memory_patch},
            )
            return patched
        return memory

    def _inject_observer_steer(
        self,
        *,
        mission_id: str | None = None,
        round_no: int | None = None,
        messages: list[Any] | None,
        pending_guidance: list[str] | None,
        decision: ObserverDecision,
        phase: str = "tool",
    ) -> bool:
        decision = decision.normalised()
        if not _observer_should_inject(decision, phase=phase):
            return False
        injection = self.observer.format_injection(decision)
        if messages is not None:
            messages.append(HumanMessage(content=injection))
            injected = True
        elif pending_guidance is not None:
            pending_guidance.append(injection)
            injected = True
        else:
            return False
        if mission_id and round_no is not None:
            self.store.add_event(
                mission_id=mission_id,
                round_no=round_no,
                event_type="observer_agent",
                title="Observer steer injected",
                content=decision.steer_message or decision.skill_instruction or decision.route_assessment,
                metadata={
                    "observer": decision.to_dict(),
                    "injected": True,
                    "phase": phase,
                    "injection_signature": decision.signature(),
                    "next_step": decision.steer_message or decision.skill_instruction or decision.route_assessment,
                },
            )
        return injected

    def _audit_give_up_request(
        self,
        *,
        mission_id: str,
        round_no: int,
        mission: dict[str, Any],
        memory: dict[str, Any],
        tool_call_log: list[dict[str, Any]],
        captured_flags: list[str],
        reason: str,
    ) -> tuple[bool, ObserverDecision, dict[str, Any]]:
        decision = self.observer.audit_give_up(
            reason=reason,
            mission=mission,
            memory=memory,
            tool_call_log=tool_call_log,
            captured_flags=captured_flags,
        ).normalised()
        self._record_observer_decision(
            mission_id=mission_id,
            round_no=round_no,
            decision=decision,
            phase="give_up",
        )
        patched = self._apply_observer_memory_patch(
            mission_id=mission_id,
            round_no=round_no,
            memory=memory,
            decision=decision,
        )
        return decision.observer_enforcement_state == "allow_stop", decision, patched

    def _update_pending_observer_steer(
        self,
        current: ObserverDecision | None,
        decision: ObserverDecision,
    ) -> ObserverDecision | None:
        decision = decision.normalised()
        if decision.observer_enforcement_state == "resolved":
            return None
        if decision.action == "steer" and decision.severity in {"warn", "critical"}:
            if decision.next_verification or decision.required_next_evidence or decision.steer_message:
                return decision
        return current

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
        asset_capabilities = _asset_access_capabilities(
            mission=mission,
            env_info=env_info,
            mission_workdir=mission_workdir,
        )
        self.store.add_event(
            mission_id=mission_id,
            round_no=0,
            event_type="system",
            title="Asset access capabilities bound",
            content=_compact_json(asset_capabilities, max_len=2000),
            metadata={"asset_access_capabilities": asset_capabilities},
        )

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
                        reasoning_effort=entry.reasoning_effort,
                        use_responses_api=entry.use_responses_api,
                        disable_response_storage=entry.disable_response_storage,
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
        pending_observer_guidance: list[str] = []
        pending_observer_steer: ObserverDecision | None = None
        observer_review_interval = max(1, int(getattr(self.settings, "observer_review_interval", 16) or 16))
        observer_turns_since_review = 0
        mission_scan_timeout_count = 0
        missing_tools_seen: set[str] = _missing_tools_from_memory(memory)

        start_round = max(1, self.store.get_max_round_no(mission_id) + 1)
        if start_round > max_rounds:
            self.store.update_mission_status(
                mission_id,
                "stopped",
                error_message="No remaining rounds; resume the mission to add more rounds.",
            )
            self.store.add_event(
                mission_id=mission_id,
                round_no=max_rounds,
                event_type="warning",
                title="No remaining rounds",
                content=f"start_round={start_round} max_rounds={max_rounds}",
            )
            return

        last_logged_skill_ids: tuple[str, ...] = ()
        last_logged_missing_skill_ids: tuple[str, ...] = ()

        for round_no in range(start_round, max_rounds + 1):
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
            missing_tools_seen.update(_missing_tools_from_memory(memory))

            manual_skill_ids = [
                str(item).strip()
                for item in mission.get("skills", [])
                if str(item).strip()
            ]
            activated_skill_ids = [
                str(item).strip()
                for item in mission.get("activated_skills", [])
                if str(item).strip()
            ]
            active_skill_ids = list(dict.fromkeys(manual_skill_ids + activated_skill_ids))
            selected_skills = []
            missing_skills = active_skill_ids
            skill_catalog: list[dict[str, Any]] = []
            if self.skills:
                self.skills.refresh()
                selected_skills, missing_skills = self.skills.resolve(active_skill_ids)
                if self.settings.skills_auto_use:
                    skill_catalog = self.skills.catalog(limit=self.settings.skill_catalog_limit)

            skill_prompt_data = [
                skill.to_dict(include_prompt=True)
                for skill in selected_skills
            ]
            current_skill_ids = tuple(skill.id for skill in selected_skills)
            if current_skill_ids != last_logged_skill_ids:
                if current_skill_ids:
                    self.store.add_event(
                        mission_id=mission_id,
                        round_no=round_no,
                        event_type="system",
                        title="Skills enabled",
                        content=", ".join(current_skill_ids),
                    )
                last_logged_skill_ids = current_skill_ids

            current_missing_skill_ids = tuple(missing_skills)
            if current_missing_skill_ids and current_missing_skill_ids != last_logged_missing_skill_ids:
                self.store.add_event(
                    mission_id=mission_id,
                    round_no=round_no,
                    event_type="warning",
                    title="Skills unavailable",
                    content=", ".join(current_missing_skill_ids),
                )
                last_logged_missing_skill_ids = current_missing_skill_ids

            # Build STABLE system prompt (rules/tools/goal/env — does NOT change within a mission)
            # Volatile context (memory/round/flags) goes into a separate HumanMessage
            # so the system prompt prefix stays identical → API prompt caching kicks in
            system_prompt = build_tool_system_prompt(
                mission=mission,
                env_info=env_info,
                mission_workdir=mission_workdir,
                public_ip=self.settings.sandbox_public_ip,
                skills=skill_prompt_data,
                skill_catalog=skill_catalog,
            )
            experience_hints = self._build_experience_hints(mission, memory)
            volatile_context = build_volatile_context(
                round_no=round_no,
                memory=memory,
                captured_flags=captured_flags,
                expected_flags=mission.get("expected_flags", 1),
                experience_hints=experience_hints,
            )
            tool_call_log: list[dict[str, Any]] = []

            def on_flag(flag: str) -> str:
                for existing in captured_flags:
                    if flag.lower() == existing.lower():
                        return f"[FLAG_DUPLICATE] {flag} already submitted"
                captured_flags.append(flag)
                remaining = max(0, expected_flags - len(captured_flags))
                self.store.add_event(
                    mission_id=mission_id,
                    round_no=round_no,
                    event_type="flag",
                    title="Flag captured",
                    content=f"{flag} ({len(captured_flags)}/{expected_flags})",
                )
                if remaining == 0:
                    flag_captured.set()
                    return f"[FLAG_CAPTURED] {flag} - all {expected_flags} flag(s) found; mission complete."
                return f"[FLAG_CAPTURED] {flag} - {remaining} flag(s) still needed; continue from this exact lead."

            def on_give_up(reason: str) -> str:
                nonlocal memory
                allowed, decision, patched_memory = self._audit_give_up_request(
                    mission_id=mission_id,
                    round_no=round_no,
                    mission=mission,
                    memory=memory,
                    tool_call_log=tool_call_log,
                    captured_flags=captured_flags,
                    reason=reason,
                )
                memory = patched_memory
                if not allowed:
                    self.store.add_event(
                        mission_id=mission_id,
                        round_no=round_no,
                        event_type="warning",
                        title="Give up rejected by Observer",
                        content=decision.steer_message or _low_evidence_stop_block_message(memory),
                        metadata={"observer": decision.to_dict()},
                    )
                    return (
                        "[GIVE_UP_REJECTED]\n"
                        + (decision.steer_message or _low_evidence_stop_block_message(memory))
                    )
                self.store.add_event(
                    mission_id=mission_id,
                    round_no=round_no,
                    event_type="system",
                    title="AI gave up",
                    content=f"Reason: {reason}\nObserver boundary: {decision.failure_boundary}",
                    metadata={"observer": decision.to_dict()},
                )
                self.store.request_stop(mission_id)
                return "[GIVE_UP] Mission marked to stop."

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
                            experience_hints=self._build_experience_hints(mission, memory),
                        )
                    except Exception as clean_err:
                        logger.warning("[orchestrator] memory cleaning failed: %s", clean_err)

            user_msg = self._build_round_user_message(round_no, _stall_rounds, mission["target"])
            route_guard = _route_guard_guidance(memory)
            if route_guard:
                user_msg = f"{user_msg}\n\n{route_guard}"

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
            initial_human_content = f"{volatile_context}\n\n---\n\n{user_msg}"
            if pending_observer_guidance:
                initial_human_content += "\n\n---\n\n" + "\n\n".join(pending_observer_guidance)
                pending_observer_guidance.clear()
            messages: list[Any] = [
                sys_msg,
                HumanMessage(content=initial_human_content),
            ]

            tools = create_all_tools(
                sandbox=sbx,
                workdir=mission_workdir,
                store=self.store,
                knowledge=self.knowledge,
                skills=self.skills if self.settings.skills_auto_use else None,
                mission=mission,
                on_flag=on_flag,
                on_give_up=on_give_up,
                stop_fn=lambda: self.store.should_stop(mission_id),
                on_chunk=_on_chunk,
                knowledge_top_k=self.settings.knowledge_top_k,
                command_timeout_sec=self.settings.command_timeout_sec,
                skill_prompt_max_chars=self.settings.skill_prompt_max_chars,
                skill_reference_max_chars=self.settings.skill_reference_max_chars,
            )
            tool_map = {t.name: t for t in tools}
            model_with_tools = tool_model.bind_tools(tools)

            llm_call_count = 0  # number of LLM invocations this round (one call = one AI "turn")
            tool_exec_count = 0  # total individual tool executions this round (for logging)
            round_tool_call_log: list[dict[str, Any]] = []
            consecutive_no_tool = 0
            round_start_time = time.monotonic()
            round_timeout_sec = mission.get("round_timeout_sec", self.settings.round_timeout_sec)
            round_broad_scan_count = 0
            last_time_guidance_tag = ""
            round_memory_before_observer = memory

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
                remaining_round_time = round_timeout_sec - elapsed
                time_guidance = _round_time_guidance(remaining_round_time)
                time_guidance_tag = ""
                if time_guidance:
                    time_guidance_tag = "[ROUND_TIME_CRITICAL]" if "[ROUND_TIME_CRITICAL]" in time_guidance else "[ROUND_TIME_LIMITED]"
                if time_guidance and time_guidance_tag != last_time_guidance_tag:
                    messages.append(HumanMessage(content=time_guidance))
                    last_time_guidance_tag = time_guidance_tag

                if self._inject_human_guidance(
                    mission_id=mission_id,
                    round_no=round_no,
                    messages=messages,
                ):
                    consecutive_no_tool = 0

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
                observer_turns_since_review += 1
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
                            "立即调用一个工具（bash_exec/python_exec/knowledge_search/search_cve/skill_search等）继续推进攻击。"
                            "如果不确定下一步，先用当前证据做一个最小可观测验证，或用 skill_search 检索相关专项流程；"
                            "需要具体payload时优先用 knowledge_search/search_cve/web_search 查证后再执行。"
                        )))
                    continue
                consecutive_no_tool = 0

                # Execute each tool call in this response
                # IMPORTANT: All ToolMessages must be adjacent after AIMessage —
                # inserting HumanMessage between them causes Claude 400 errors.
                deferred_guidance: list[str] = []
                batch_memory_before = memory
                pending_at_batch_start = pending_observer_steer
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
                    is_broad_scan = _is_broad_scan_tool_call(tool_name, str(display_cmd))

                    blocked_missing_tool = _known_missing_tool_blocks(str(display_cmd), missing_tools_seen)
                    if blocked_missing_tool:
                        running_event_id = None
                        tool_result = _missing_tool_block_message(blocked_missing_tool)
                    elif is_broad_scan and round_broad_scan_count >= 1:
                        running_event_id = None
                        tool_result = _broad_scan_block_message(memory, reason="per-round broad scan")
                    elif _mission_scan_cooldown_blocks(tool_name, str(display_cmd), mission_scan_timeout_count):
                        running_event_id = None
                        tool_result = _broad_scan_block_message(memory, reason="mission scan timeout cooldown")
                    elif tool_name in tool_map:
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
                    flag_candidates = _flag_capture.trusted_tool_flag_candidates(tool_name, result_str)
                    auto_flag_events = _flag_capture.auto_capture_trusted_flag_events(
                        tool_name=tool_name,
                        result_str=result_str,
                        captured_flags=captured_flags,
                        on_flag=on_flag,
                        is_complete=flag_captured.is_set,
                    )
                    auto_flag_results = [message for _, message in auto_flag_events]
                    truncated_result = _summarize_guidance_result(tool_name, result_str, stdout_limit)
                    truncated_result = _flag_capture.append_flag_candidate_summary(truncated_result, flag_candidates)
                    if auto_flag_results:
                        truncated_result += "\n\n[AUTO_FLAG_CAPTURE]\n" + "\n".join(auto_flag_results)
                        for flag, _message in auto_flag_events:
                            self.store.add_event(
                                mission_id=mission_id,
                                round_no=round_no,
                                event_type="auto_flag_capture",
                                title=f"Auto flag capture from {tool_name}",
                                content=_flag_capture.flag_context(result_str, flag) or flag,
                                command=str(display_cmd)[:1000],
                                metadata={
                                    "tool": tool_name,
                                    "flag": flag,
                                    "tool_call_id": tool_id,
                                    "complete": flag_captured.is_set(),
                                },
                            )
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

                    missing_tool = _missing_tool_name(result_str)
                    if missing_tool:
                        missing_tools_seen.add(missing_tool)
                        patch = {
                            "dead_ends": [
                                f"`{missing_tool}` is unavailable in the sandbox; use curl/raw headers/body/HTML parsing instead."
                            ]
                        }
                        memory = self._apply_observer_memory_patch(
                            mission_id=mission_id,
                            round_no=round_no,
                            memory=memory,
                            decision=ObserverDecision(
                                severity="info",
                                state="progressing",
                                intervention="memory_sync",
                                action="memory_patch",
                                memory_patch=patch,
                            ),
                        )

                    if is_broad_scan:
                        if "[BROAD_SCAN_BLOCKED]" not in result_str:
                            round_broad_scan_count += 1
                        if round_broad_scan_count > 1:
                            lead = _highest_value_lead(memory)
                            deferred_guidance.append(
                                "[BROAD_SCAN_LIMIT]\n"
                                "This round already used a broad enumeration/scanning command. Stop starting more broad scans. "
                                "Next action must be a targeted verification tied to a concrete endpoint, parameter, response "
                                f"difference, or this lead: {lead or 'the strongest current memory lead'}.\n"
                                "[/BROAD_SCAN_LIMIT]"
                            )

                    # Defer timeout guidance — cannot insert HumanMessage between ToolMessages
                    if "[TIMEOUT" in result_str:
                        deferred_guidance.append(
                            f"命令 `{str(display_cmd)[:100]}` 已超时。"
                            "考虑：缩小扫描范围、使用更快的工具、"
                            "或后台运行（nohup ... &）后用 tail 检查结果。"
                        )

                    if "[TIMEOUT" in result_str:
                        recent_scan_timeouts = sum(
                            1 for row in round_tool_call_log[-3:]
                            if _tool_result_timed_out(row)
                            and _is_scan_like_tool_call(
                                str(row.get("tool") or ""),
                                str(row.get("args_full") or ""),
                            )
                        )
                        if _is_scan_like_tool_call(tool_name, str(display_cmd)):
                            recent_scan_timeouts += 1
                        if recent_scan_timeouts >= 2:
                            deferred_guidance.append(
                                "连续扫描/爆破类工具超时。停止扩大扫描，回到当前 memory 中最高价值的已验证线索，"
                                "下一步只做一个小范围、可解释、能产出原始证据的验证。"
                            )

                    if "[TIMEOUT" in result_str:
                        deferred_guidance.append(
                            f"Command `{str(display_cmd)[:100]}` timed out. Shrink the scope, use a faster targeted probe, "
                            "or run a background job only when it preserves a concrete result to inspect."
                        )
                        if _is_scan_like_tool_call(tool_name, str(display_cmd)):
                            mission_scan_timeout_count += 1
                            if mission_scan_timeout_count >= 2:
                                deferred_guidance.append(
                                    "[MISSION_SCAN_TIMEOUT_GUARD]\n"
                                    "This mission has already had at least two scan-like timeouts. Lower priority for ffuf/arjun/nuclei/sqlmap "
                                    f"and prefer exact verification from memory: {_highest_value_lead(memory) or 'current highest-value lead'}.\n"
                                    "[/MISSION_SCAN_TIMEOUT_GUARD]"
                                )

                    tool_call_entry = {
                        "tool": tool_name,
                        "args_summary": str(display_cmd)[:300],
                        "args_full": str(display_cmd),
                        "result_summary": result_str[:500],
                        "result_observer": _observer_result_view(result_str),
                        "result_full": result_str,
                        "result_len": len(result_str),
                        "exit_code": _infer_tool_exit_code(result_str, str(display_cmd)),
                    }
                    tool_call_log.append(tool_call_entry)
                    round_tool_call_log.append(tool_call_entry)
                    tool_exec_count += 1

                    if auto_flag_results and not flag_captured.is_set():
                        deferred_guidance.append(_post_partial_flag_guidance(captured_flags, expected_flags))

                    if auto_flag_results and flag_captured.is_set():
                        break

                    if flag_captured.is_set():
                        break

                # Now safe to inject deferred guidance after ALL ToolMessages
                if deferred_guidance:
                    messages.append(HumanMessage(content="\n".join(deferred_guidance)))

                if pending_at_batch_start:
                    override_decision = self.observer.audit_override(
                        pending_decision=pending_at_batch_start,
                        next_tool_calls=round_tool_call_log[-len(response.tool_calls):],
                        memory_before=batch_memory_before,
                        memory_after=memory,
                        agent_override_reason=response_text[:500],
                    ).normalised()
                    if override_decision.actionable:
                        self._record_observer_decision(
                            mission_id=mission_id,
                            round_no=round_no,
                            decision=override_decision,
                            phase="override",
                        )
                        memory = self._apply_observer_memory_patch(
                            mission_id=mission_id,
                            round_no=round_no,
                            memory=memory,
                            decision=override_decision,
                        )
                        pending_observer_steer = self._update_pending_observer_steer(
                            pending_observer_steer,
                            override_decision,
                        )
                        if override_decision.severity == "critical":
                            messages.append(
                                HumanMessage(
                                    content=(
                                        self.observer.format_injection(override_decision)
                                        + "\n\n"
                                        + _stale_observer_steer_block_message(
                                            override_decision.next_verification
                                        )
                                    )
                                )
                            )
                        elif override_decision.observer_enforcement_state == "resolved":
                            pending_observer_steer = None

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
                tool_call_log=_tool_call_memory_view(round_tool_call_log),
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

            if observer_turns_since_review >= observer_review_interval:
                round_observer_decision = self.observer_runtime.review_round(
                    mission_id=mission_id,
                    round_no=round_no,
                    mission=mission,
                    memory_before=memory,
                    memory_after=new_memory,
                    tool_call_log=tool_call_log,
                    round_tool_call_log=round_tool_call_log,
                    llm_call_count=llm_call_count,
                    stall_rounds=_stall_rounds,
                    captured_flags=captured_flags,
                )
                observer_turns_since_review = 0
                self._record_observer_decision(
                    mission_id=mission_id,
                    round_no=round_no,
                    decision=round_observer_decision,
                    phase="round",
                )
                new_memory = self._apply_observer_memory_patch(
                    mission_id=mission_id,
                    round_no=round_no,
                    memory=new_memory,
                    decision=round_observer_decision,
                )
                if round_observer_decision.actionable:
                    self._inject_observer_steer(
                        mission_id=mission_id,
                        round_no=round_no,
                        messages=None,
                        pending_guidance=pending_observer_guidance,
                        decision=round_observer_decision,
                        phase="round",
                    )
                    pending_observer_steer = self._update_pending_observer_steer(
                        pending_observer_steer,
                        round_observer_decision,
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

        memory = self.store.get_memory(mission_id)
        stop_allowed, stop_decision, memory = self._audit_give_up_request(
            mission_id=mission_id,
            round_no=max_rounds,
            mission=mission,
            memory=memory,
            tool_call_log=tool_call_log,
            captured_flags=captured_flags,
            reason="max_rounds reached; Observer failure-boundary audit required before stopped status",
        )
        stop_message = (
            "Reached max_rounds with Observer failure-boundary audit."
            if stop_allowed
            else "Reached max_rounds; Observer recorded missing failure-boundary evidence."
        )
        self.store.update_mission_status(
            mission_id, "stopped",
            error_message=stop_message,
        )
        self.store.add_event(
            mission_id=mission_id,
            round_no=max_rounds,
            event_type="system",
            title="Max rounds reached",
            content=stop_message,
            metadata={"observer": stop_decision.to_dict()},
        )
        # Final memory compression for DA analysis
        self._do_final_memory_compression(
            mission_id, mission, memory, max_rounds, tool_call_log, "max_rounds"
        )
