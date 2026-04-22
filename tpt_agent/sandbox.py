from __future__ import annotations

import base64
import queue
import re
import subprocess
import threading
import time
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Callable

from tpt_agent.config import AgentSettings

_ANSI_ESCAPE = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")


def _strip_ansi(text: str) -> str:
    """Remove ANSI escape codes (colors, cursor movement) from terminal output."""
    return _ANSI_ESCAPE.sub("", text)


@dataclass(frozen=True)
class CommandResult:
    command: str
    exit_code: int
    stdout: str
    stderr: str
    started_at: str
    ended_at: str

    def to_log_text(self) -> str:
        pieces = [f"$ {self.command}", f"[exit={self.exit_code}]"]
        if self.stdout:
            pieces.append("STDOUT:\n" + self.stdout)
        if self.stderr:
            pieces.append("STDERR:\n" + self.stderr)
        return "\n\n".join(pieces).strip()


class SandboxExecutor:
    def __init__(self, settings: AgentSettings, container_override: str = "") -> None:
        self.settings = settings
        self._container = container_override or settings.sandbox_container

    def ensure_workspace(self) -> CommandResult:
        return self.run(
            f"mkdir -p {self.settings.sandbox_workdir} && cd {self.settings.sandbox_workdir} && pwd",
            timeout_sec=20,
        )

    def _run_popen(
        self,
        cmd: list[str],
        timeout_sec: int,
        stop_fn: Callable[[], bool] | None,
        on_chunk: Callable[[str], None] | None = None,
    ) -> tuple[str, str, int]:
        """Run a subprocess with streaming output via threads. Returns (stdout, stderr, exit_code)."""
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        line_queue: queue.Queue[tuple[str, str | None]] = queue.Queue()

        def _reader(stream, tag: str) -> None:
            for line in iter(stream.readline, ""):
                line_queue.put((tag, line))
            line_queue.put((tag, None))  # EOF sentinel

        threading.Thread(target=_reader, args=(proc.stdout, "out"), daemon=True).start()
        threading.Thread(target=_reader, args=(proc.stderr, "err"), daemon=True).start()

        stdout_parts: list[str] = []
        stderr_parts: list[str] = []
        eof_count = 0
        deadline = time.time() + timeout_sec
        last_chunk_at = time.time()
        CHUNK_INTERVAL = 1.5  # seconds between on_chunk calls

        while eof_count < 2:
            if stop_fn and stop_fn():
                try:
                    proc.terminate()
                    proc.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    proc.kill()
                return _strip_ansi("".join(stdout_parts)) + "\n[KILLED: stop requested]", "", -15

            try:
                tag, line = line_queue.get(timeout=0.5)
                if line is None:
                    eof_count += 1
                elif tag == "out":
                    stdout_parts.append(line)
                else:
                    stderr_parts.append(line)
                # Fire on_chunk periodically with current stdout
                if on_chunk and (time.time() - last_chunk_at) >= CHUNK_INTERVAL:
                    on_chunk(_strip_ansi("".join(stdout_parts)))
                    last_chunk_at = time.time()
            except queue.Empty:
                # Timeout getting a line — fire chunk update if due
                if on_chunk and stdout_parts and (time.time() - last_chunk_at) >= CHUNK_INTERVAL:
                    on_chunk(_strip_ansi("".join(stdout_parts)))
                    last_chunk_at = time.time()
                # Check hard deadline
                if time.time() > deadline:
                    proc.kill()
                    # Drain remaining lines
                    while True:
                        try:
                            tag2, line2 = line_queue.get_nowait()
                            if line2 and tag2 == "out":
                                stdout_parts.append(line2)
                            elif line2 and tag2 == "err":
                                stderr_parts.append(line2)
                        except queue.Empty:
                            break
                    stdout = _strip_ansi("".join(stdout_parts))
                    stderr = _strip_ansi("".join(stderr_parts))
                    return stdout + f"\n[TIMEOUT after {timeout_sec}s]", stderr, 124

        proc.wait()
        return _strip_ansi("".join(stdout_parts)), _strip_ansi("".join(stderr_parts)), proc.returncode

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
        shell_script = (
            "set -o pipefail\n"
            f"mkdir -p {work}\n"
            f"cd {work}\n"
            f"{command}\n"
        )
        timeout = timeout_sec or self.settings.command_timeout_sec
        cmd = [
            "docker", "exec",
            self._container,
            "bash", "-lc", shell_script,
        ]
        raw_stdout, raw_stderr, exit_code = self._run_popen(cmd, timeout, stop_fn, on_chunk=on_chunk)
        stdout = self._truncate(raw_stdout)
        stderr = self._truncate(raw_stderr)
        ended_at = datetime.now().astimezone().isoformat(timespec="seconds")
        return CommandResult(
            command=command,
            exit_code=exit_code,
            stdout=stdout,
            stderr=stderr,
            started_at=started_at,
            ended_at=ended_at,
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
        script_path = f"{work}/_tpt_script.py"
        shell_script = (
            "set -o pipefail\n"
            f"mkdir -p {work}\n"
            f"cd {work}\n"
            f"echo '{encoded}' | base64 -d > {script_path}\n"
            f"python3 {script_path}\n"
        )
        timeout = timeout_sec or self.settings.command_timeout_sec
        cmd = [
            "docker", "exec",
            self._container,
            "bash", "-lc", shell_script,
        ]
        raw_stdout, raw_stderr, exit_code = self._run_popen(cmd, timeout, stop_fn, on_chunk=on_chunk)
        stdout = self._truncate(raw_stdout)
        stderr = self._truncate(raw_stderr)
        ended_at = datetime.now().astimezone().isoformat(timespec="seconds")
        return CommandResult(
            command=f"[python3 script]\n{code[:200]}{'...' if len(code)>200 else ''}",
            exit_code=exit_code,
            stdout=stdout,
            stderr=stderr,
            started_at=started_at,
            ended_at=ended_at,
        )

    def _truncate(self, value: str) -> str:
        limit = self.settings.stdout_limit
        if len(value) <= limit:
            return value
        return value[: limit // 2] + "\n...<truncated>...\n" + value[-limit // 2 :]
