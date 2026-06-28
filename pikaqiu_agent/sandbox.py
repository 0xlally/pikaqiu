from __future__ import annotations

import base64
import logging
import queue
import re
import subprocess
import threading
import time
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Callable

from pikaqiu_agent.config import AgentSettings
from pikaqiu_agent.output_truncation import HeadTailBuffer

_ANSI_ESCAPE = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
logger = logging.getLogger(__name__)


def _strip_ansi(text: str) -> str:
    """Remove ANSI escape codes (colors, cursor movement) from terminal output."""
    return _ANSI_ESCAPE.sub("", text)


@dataclass(frozen=True)
class CommandResult:
    command: str
    exit_code: int
    output: str
    stdout: str
    stderr: str
    started_at: str
    ended_at: str

    def to_log_text(self) -> str:
        pieces = [f"$ {self.command}", f"[exit={self.exit_code}]"]
        if self.output:
            pieces.append("OUTPUT:\n" + self.output)
        return "\n\n".join(pieces).strip()


class SandboxExecutor:
    def __init__(self, settings: AgentSettings, container_override: str = "") -> None:
        self.settings = settings
        self._container = container_override or settings.sandbox_container

    def ensure_workspace(self, stop_fn: Callable[[], bool] | None = None) -> CommandResult:
        return self.run(
            f"mkdir -p {self.settings.sandbox_workdir} && cd {self.settings.sandbox_workdir} && pwd",
            timeout_sec=20,
            stop_fn=stop_fn,
        )

    @staticmethod
    def _script_preamble(workdir: str) -> str:
        return (
            "set -o pipefail\n"
            f"mkdir -p {workdir}\n"
            f"cd {workdir}\n"
        )

    def _build_result(
        self,
        *,
        command: str,
        raw_stdout: str,
        raw_stderr: str,
        raw_output: str,
        exit_code: int,
        started_at: str,
    ) -> CommandResult:
        ended_at = datetime.now().astimezone().isoformat(timespec="seconds")
        return CommandResult(
            command=command,
            exit_code=exit_code,
            output=raw_output,
            stdout=raw_stdout,
            stderr=raw_stderr,
            started_at=started_at,
            ended_at=ended_at,
        )

    def _run_popen(
        self,
        cmd: list[str],
        timeout_sec: int,
        stop_fn: Callable[[], bool] | None,
        on_chunk: Callable[[str], None] | None = None,
    ) -> tuple[str, str, str, int]:
        """Run a subprocess with streaming output via threads. Returns (stdout, stderr, combined, exit_code)."""
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        line_queue: queue.Queue[tuple[str, bytes | None]] = queue.Queue(maxsize=256)

        def _reader(stream, tag: str) -> None:
            while True:
                chunk = stream.read(8192)
                if not chunk:
                    break
                line_queue.put((tag, chunk))
            line_queue.put((tag, None))  # EOF sentinel

        threading.Thread(target=_reader, args=(proc.stdout, "out"), daemon=True).start()
        threading.Thread(target=_reader, args=(proc.stderr, "err"), daemon=True).start()

        stdout_buffer = HeadTailBuffer()
        stderr_buffer = HeadTailBuffer()
        output_buffer = HeadTailBuffer()
        eof_count = 0
        deadline = time.time() + timeout_sec
        last_chunk_at = time.time()
        CHUNK_INTERVAL = 1.5  # seconds between on_chunk calls

        def _stdout_text() -> str:
            return _strip_ansi(stdout_buffer.to_text_lossy())

        def _stderr_text() -> str:
            return _strip_ansi(stderr_buffer.to_text_lossy())

        def _output_text() -> str:
            return _strip_ansi(output_buffer.to_text_lossy())

        def _terminate_process() -> None:
            try:
                proc.terminate()
                proc.wait(timeout=2)
            except subprocess.TimeoutExpired:
                proc.kill()
                try:
                    proc.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    pass

        def _push_output(tag: str, line: bytes | None) -> bool:
            if line is None:
                return True
            if tag == "out":
                stdout_buffer.push_chunk(line)
            else:
                stderr_buffer.push_chunk(line)
            output_buffer.push_chunk(line)
            return False

        def _drain_queue() -> None:
            while True:
                try:
                    tag, line = line_queue.get_nowait()
                except queue.Empty:
                    return
                _push_output(tag, line)

        def _drain_queue_until_closed(grace_sec: float = 2.0) -> None:
            eof_seen = 0
            deadline_at = time.time() + max(0.0, grace_sec)
            while eof_seen < 2 and time.time() < deadline_at:
                try:
                    tag, line = line_queue.get(timeout=0.02)
                except queue.Empty:
                    continue
                if _push_output(tag, line):
                    eof_seen += 1

        def _emit_chunk() -> None:
            if not on_chunk:
                return
            try:
                on_chunk(_stdout_text())
            except Exception:
                logger.warning("[sandbox] on_chunk callback failed", exc_info=True)

        def _timeout_result() -> tuple[str, str, str, int]:
            proc.kill()
            try:
                proc.wait(timeout=2)
            except subprocess.TimeoutExpired:
                proc.kill()
                try:
                    proc.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    pass
            _drain_queue_until_closed()
            _drain_queue()
            stdout = _stdout_text()
            stderr = _stderr_text()
            output = _output_text()
            timeout_note = f"\n[TIMEOUT after {timeout_sec}s]"
            return stdout + timeout_note, stderr, output + timeout_note, 124

        while eof_count < 2:
            if time.time() > deadline:
                return _timeout_result()

            if stop_fn and stop_fn():
                _terminate_process()
                _drain_queue_until_closed()
                _drain_queue()
                stdout = _stdout_text() + "\n[KILLED: stop requested]"
                stderr = _stderr_text()
                output = _output_text() + "\n[KILLED: stop requested]"
                return stdout, stderr, output, -15

            try:
                tag, line = line_queue.get(timeout=0.5)
                if line is None:
                    eof_count += 1
                else:
                    _push_output(tag, line)
                # Fire on_chunk periodically with current stdout
                if on_chunk and (time.time() - last_chunk_at) >= CHUNK_INTERVAL:
                    _emit_chunk()
                    last_chunk_at = time.time()
            except queue.Empty:
                # Timeout getting a line — fire chunk update if due
                if on_chunk and stdout_buffer.retained_bytes() and (time.time() - last_chunk_at) >= CHUNK_INTERVAL:
                    _emit_chunk()
                    last_chunk_at = time.time()
                # Check hard deadline
                if time.time() > deadline:
                    return _timeout_result()

        proc.wait()
        return (
            _stdout_text(),
            _stderr_text(),
            _output_text(),
            proc.returncode,
        )

    def run(
        self,
        command: str,
        timeout_sec: int | None = None,
        workdir: str | None = None,
        stop_fn: Callable[[], bool] | None = None,
        on_chunk: Callable[[str], None] | None = None,
    ) -> CommandResult:
        work = workdir or self.settings.sandbox_workdir
        started_at = datetime.now().astimezone().isoformat(timespec="seconds")
        timeout = timeout_sec or self.settings.command_timeout_sec
        shell_script = self._script_preamble(work) + f"{command}\n"
        raw_stdout, raw_stderr, raw_output, exit_code = self._run_popen(
            ["docker", "exec", self._container, "bash", "-lc", shell_script],
            timeout_sec=timeout,
            stop_fn=stop_fn,
            on_chunk=on_chunk,
        )
        return self._build_result(
            command=command,
            exit_code=exit_code,
            raw_stdout=raw_stdout,
            raw_stderr=raw_stderr,
            raw_output=raw_output,
            started_at=started_at,
        )

    def run_python(
        self,
        code: str,
        timeout_sec: int | None = None,
        workdir: str | None = None,
        stop_fn: Callable[[], bool] | None = None,
        on_chunk: Callable[[str], None] | None = None,
    ) -> CommandResult:
        """Execute Python code directly in sandbox, avoiding bash quoting issues.
        
        Each call is fully isolated — no session persistence between calls.
        AI must handle login/auth in every call that needs it.
        """
        work = workdir or self.settings.sandbox_workdir
        started_at = datetime.now().astimezone().isoformat(timespec="seconds")
        encoded = base64.b64encode(code.encode("utf-8")).decode("ascii")
        # Use workdir-based script path to isolate concurrent missions
        script_path = f"{work}/_pikaqiu_script.py"
        timeout = timeout_sec or self.settings.command_timeout_sec
        shell_script = (
            self._script_preamble(work)
            + f"echo '{encoded}' | base64 -d > {script_path}\n"
            + f"python3 {script_path}\n"
        )
        raw_stdout, raw_stderr, raw_output, exit_code = self._run_popen(
            ["docker", "exec", self._container, "bash", "-lc", shell_script],
            timeout_sec=timeout,
            stop_fn=stop_fn,
            on_chunk=on_chunk,
        )
        command_preview = f"[python3 script]\n{code[:200]}{'...' if len(code) > 200 else ''}"
        return self._build_result(
            command=command_preview,
            exit_code=exit_code,
            raw_stdout=raw_stdout,
            raw_stderr=raw_stderr,
            raw_output=raw_output,
            started_at=started_at,
        )
