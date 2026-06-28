import re
import sys
import time
from types import SimpleNamespace

from pikaqiu_agent.orchestrator import _infer_tool_exit_code
from pikaqiu_agent.output_truncation import UNIFIED_EXEC_OUTPUT_MAX_BYTES
from pikaqiu_agent.sandbox import SandboxExecutor
from pikaqiu_agent.tools import create_all_tools, create_bash_tool, create_python_tool, create_web_search_tool


class FakeSandbox:
    def __init__(self):
        self.calls = []

    def run(self, command, timeout_sec=None, workdir=None, stop_fn=None, on_chunk=None):
        self.calls.append(("run", command, timeout_sec, workdir))
        return SimpleNamespace(stdout="ok", stderr="", exit_code=0, command=command)

    def run_python(self, code, timeout_sec=None, workdir=None, stop_fn=None, on_chunk=None):
        self.calls.append(("run_python", code, timeout_sec, workdir))
        return SimpleNamespace(stdout="ok", stderr="", exit_code=0, command=code)


def test_bash_exec_uses_mission_timeout_when_omitted():
    sandbox = FakeSandbox()
    tool = create_bash_tool(sandbox, "/work", max_timeout=300)

    tool.invoke({"command": "echo ok"})

    assert sandbox.calls == [("run", "echo ok", 300, "/work")]


def test_python_exec_uses_mission_timeout_when_omitted():
    sandbox = FakeSandbox()
    tool = create_python_tool(sandbox, "/work", max_timeout=300)

    tool.invoke({"code": "print('ok')"})

    assert sandbox.calls == [("run_python", "print('ok')", 300, "/work")]


def test_explicit_tool_timeout_is_respected_until_mission_cap():
    sandbox = FakeSandbox()
    bash_tool = create_bash_tool(sandbox, "/work", max_timeout=300)
    python_tool = create_python_tool(sandbox, "/work", max_timeout=300)

    bash_tool.invoke({"command": "sleep 1", "timeout": 30})
    bash_tool.invoke({"command": "batch probe", "timeout": 70})
    python_tool.invoke({"code": "print('ok')", "timeout": 999})

    assert sandbox.calls == [
        ("run", "sleep 1", 30, "/work"),
        ("run", "batch probe", 70, "/work"),
        ("run_python", "print('ok')", 300, "/work"),
    ]


def test_max_output_tokens_is_tool_response_setting_not_sandbox_timeout():
    sandbox = FakeSandbox()
    bash_tool = create_bash_tool(sandbox, "/work", max_timeout=300)
    python_tool = create_python_tool(sandbox, "/work", max_timeout=300)

    bash_tool.invoke({"command": "echo ok", "max_output_tokens": 20})
    python_tool.invoke({"code": "print('ok')", "max_output_tokens": 20})

    assert sandbox.calls == [
        ("run", "echo ok", 300, "/work"),
        ("run_python", "print('ok')", 300, "/work"),
    ]


def test_sandbox_tools_return_codex_exec_response_shape():
    sandbox = FakeSandbox()
    bash_tool = create_bash_tool(sandbox, "/work", max_timeout=300)
    python_tool = create_python_tool(sandbox, "/work", max_timeout=300)

    bash_result = bash_tool.invoke({"command": "echo ok"})
    python_result = python_tool.invoke({"code": "print('ok')"})

    for result in (bash_result, python_result):
        assert re.search(r"^Chunk ID: [0-9a-f]{6}$", result, re.M)
        assert "Wall time:" in result
        assert "Process exited with code 0" in result
        assert "Original token count:" in result
        assert "\nOutput:\n" in result
        assert "[EXIT_CODE:" not in result


def test_exit_code_inference_accepts_codex_and_legacy_shapes():
    assert _infer_tool_exit_code("Process exited with code 7\nOutput:\nboom") == 7
    assert _infer_tool_exit_code("[EXIT_CODE: 3]") == 3


def test_max_output_tokens_truncates_sandbox_tool_output_body():
    class LargeOutputSandbox(FakeSandbox):
        def run(self, command, timeout_sec=None, workdir=None, stop_fn=None, on_chunk=None):
            self.calls.append(("run", command, timeout_sec, workdir))
            return SimpleNamespace(
                output="prefix-" + ("A" * 500) + "-suffix",
                stdout="",
                stderr="",
                exit_code=0,
                command=command,
            )

    sandbox = LargeOutputSandbox()
    tool = create_bash_tool(sandbox, "/work", max_timeout=300)

    result = tool.invoke({"command": "large output", "max_output_tokens": 20})

    assert "Warning: truncated output" in result
    assert "tokens truncated" in result
    assert "prefix-" in result
    assert "-suffix" in result


def test_tool_max_output_tokens_cannot_exceed_configured_cap():
    class LargeOutputSandbox(FakeSandbox):
        def run(self, command, timeout_sec=None, workdir=None, stop_fn=None, on_chunk=None):
            self.calls.append(("run", command, timeout_sec, workdir))
            return SimpleNamespace(
                output="prefix-" + ("A" * 500) + "-suffix",
                stdout="",
                stderr="",
                exit_code=0,
                command=command,
            )

    sandbox = LargeOutputSandbox()
    tool = create_bash_tool(sandbox, "/work", max_timeout=300, max_output_tokens_cap=20)

    result = tool.invoke({"command": "large output", "max_output_tokens": 40000})

    assert "Warning: truncated output" in result
    assert "tokens truncated" in result
    assert "prefix-" in result
    assert "-suffix" in result


def test_sandbox_result_prefers_combined_output_when_available():
    class CombinedOutputSandbox(FakeSandbox):
        def run(self, command, timeout_sec=None, workdir=None, stop_fn=None, on_chunk=None):
            self.calls.append(("run", command, timeout_sec, workdir))
            return SimpleNamespace(
                output="combined stdout/stderr order",
                stdout="legacy stdout",
                stderr="legacy stderr",
                exit_code=0,
                command=command,
            )

    sandbox = CombinedOutputSandbox()
    tool = create_bash_tool(sandbox, "/work", max_timeout=300)

    result = tool.invoke({"command": "mixed output"})

    assert "combined stdout/stderr order" in result
    assert "legacy stdout" not in result
    assert "legacy stderr" not in result
    assert "Process exited with code 0" in result


def test_sandbox_result_falls_back_to_stdout_and_stderr_for_legacy_results():
    class LegacyOutputSandbox(FakeSandbox):
        def run(self, command, timeout_sec=None, workdir=None, stop_fn=None, on_chunk=None):
            self.calls.append(("run", command, timeout_sec, workdir))
            return SimpleNamespace(
                stdout="legacy stdout",
                stderr="legacy stderr",
                exit_code=2,
                command=command,
            )

    sandbox = LegacyOutputSandbox()
    tool = create_bash_tool(sandbox, "/work", max_timeout=300)

    result = tool.invoke({"command": "legacy output"})

    assert "legacy stdout" in result
    assert "[STDERR] legacy stderr" in result
    assert "Process exited with code 2" in result


def test_web_search_uses_mission_timeout_semantics():
    sandbox = FakeSandbox()
    tool = create_web_search_tool(sandbox, "/work", max_timeout=300)

    tool.invoke({"open": [{"ref_id": "https://example.com"}]})
    tool.invoke({"open": [{"ref_id": "https://example.com"}], "timeout": 70})
    tool.invoke({"open": [{"ref_id": "https://example.com"}], "timeout": 999})

    assert [call[2] for call in sandbox.calls] == [300, 70, 300]


def test_web_search_uses_hosted_responses_credentials_for_search():
    sandbox = FakeSandbox()
    tool = create_web_search_tool(
        sandbox,
        "/work",
        web_search_base_url="https://proxy.example/v1",
        web_search_api_key="hosted-search-key",
        web_search_model="gpt-test",
    )

    tool.invoke({"search_query": [{"q": "OpenAI"}]})

    code = sandbox.calls[0][1]
    assert "https://proxy.example/v1" in code
    assert "hosted-search-key" in code
    assert "gpt-test" in code
    assert '"tools": [{"type": "web_search"}]' in code
    assert "api.github.com" not in code
    assert "services.nvd.nist.gov" not in code


def test_web_search_embeds_commands_as_valid_python_json():
    sandbox = FakeSandbox()
    tool = create_web_search_tool(
        sandbox,
        "/work",
        web_search_base_url="https://proxy.example/v1",
        web_search_api_key="hosted-search-key",
        web_search_model="gpt-test",
    )

    tool.invoke({"search_query": [{"q": "OpenAI", "recency": None, "domains": None}]})

    code = sandbox.calls[0][1]
    compile(code, "<web_search_generated>", "exec")
    assert "commands = json.loads(" in code


def test_all_tools_expose_only_expected_default_names():
    sandbox = FakeSandbox()
    tools = create_all_tools(sandbox, "/work", command_timeout_sec=300)
    names = {tool.name for tool in tools}

    assert names == {"bash_exec", "python_exec", "web_search"}


def test_run_popen_times_out_even_while_output_is_continuous():
    executor = object.__new__(SandboxExecutor)
    start = time.monotonic()

    stdout, stderr, output, exit_code = executor._run_popen(
        [
            sys.executable,
            "-c",
            (
                "import sys, time\n"
                "end = time.time() + 5\n"
                "while time.time() < end:\n"
                "    sys.stdout.buffer.write(b'A' * 8192)\n"
                "    sys.stdout.buffer.flush()\n"
            ),
        ],
        timeout_sec=1,
        stop_fn=None,
    )

    assert time.monotonic() - start < 3
    assert exit_code == 124
    assert "[TIMEOUT after 1s]" in stdout
    assert "[TIMEOUT after 1s]" in output
    assert stderr == ""


def test_run_popen_retains_head_and_tail_for_large_unbroken_output():
    executor = object.__new__(SandboxExecutor)

    stdout, stderr, output, exit_code = executor._run_popen(
        [
            sys.executable,
            "-c",
            (
                "import sys\n"
                f"sys.stdout.buffer.write(b'HEAD' + b'A' * {UNIFIED_EXEC_OUTPUT_MAX_BYTES // 2 + 32} + "
                f"b'MIDDLE_MARKER' + b'Z' * {UNIFIED_EXEC_OUTPUT_MAX_BYTES // 2 + 32} + b'TAIL')\n"
                "sys.stdout.buffer.flush()\n"
            ),
        ],
        timeout_sec=5,
        stop_fn=None,
    )

    assert exit_code == 0
    assert stderr == ""
    assert len(output.encode("utf-8")) == UNIFIED_EXEC_OUTPUT_MAX_BYTES
    assert stdout == output
    assert output.startswith("HEAD")
    assert output.endswith("TAIL")
    assert "MIDDLE_MARKER" not in output


def test_run_popen_combines_stdout_and_stderr_output():
    executor = object.__new__(SandboxExecutor)

    stdout, stderr, output, exit_code = executor._run_popen(
        [
            sys.executable,
            "-c",
            (
                "import sys\n"
                "sys.stdout.write('OUT1\\n')\n"
                "sys.stdout.flush()\n"
                "sys.stderr.write('ERR1\\n')\n"
                "sys.stderr.flush()\n"
            ),
        ],
        timeout_sec=5,
        stop_fn=None,
    )

    assert exit_code == 0
    assert stdout.replace("\r\n", "\n") == "OUT1\n"
    assert stderr.replace("\r\n", "\n") == "ERR1\n"
    normalized_output = output.replace("\r\n", "\n")
    assert "OUT1\n" in normalized_output
    assert "ERR1\n" in normalized_output


def test_run_popen_retains_head_and_tail_for_large_stderr_output():
    executor = object.__new__(SandboxExecutor)

    stdout, stderr, output, exit_code = executor._run_popen(
        [
            sys.executable,
            "-c",
            (
                "import sys\n"
                f"sys.stderr.buffer.write(b'ERR_HEAD' + b'E' * {UNIFIED_EXEC_OUTPUT_MAX_BYTES // 2 + 32} + "
                f"b'ERR_MIDDLE' + b'R' * {UNIFIED_EXEC_OUTPUT_MAX_BYTES // 2 + 32} + b'ERR_TAIL')\n"
                "sys.stderr.buffer.flush()\n"
            ),
        ],
        timeout_sec=5,
        stop_fn=None,
    )

    assert exit_code == 0
    assert stdout == ""
    assert len(stderr.encode("utf-8")) == UNIFIED_EXEC_OUTPUT_MAX_BYTES
    assert output == stderr
    assert output.startswith("ERR_HEAD")
    assert output.endswith("ERR_TAIL")
    assert "ERR_MIDDLE" not in output


def test_run_popen_stop_request_returns_retained_output():
    executor = object.__new__(SandboxExecutor)
    start = time.monotonic()

    def stop_after_first_chunk() -> bool:
        return time.monotonic() - start > 0.2

    stdout, stderr, output, exit_code = executor._run_popen(
        [
            sys.executable,
            "-c",
            (
                "import sys, time\n"
                "while True:\n"
                "    sys.stdout.buffer.write(b'STOP_HEAD' + b'A' * 8192)\n"
                "    sys.stdout.buffer.flush()\n"
                "    time.sleep(0.01)\n"
            ),
        ],
        timeout_sec=5,
        stop_fn=stop_after_first_chunk,
    )

    assert exit_code == -15
    assert "[KILLED: stop requested]" in stdout
    assert "[KILLED: stop requested]" in output
    assert "STOP_HEAD" in output
    assert stderr == ""


def test_run_popen_stop_request_preserves_stderr():
    executor = object.__new__(SandboxExecutor)
    start = time.monotonic()

    def stop_after_first_chunk() -> bool:
        return time.monotonic() - start > 0.2

    stdout, stderr, output, exit_code = executor._run_popen(
        [
            sys.executable,
            "-c",
            (
                "import sys, time\n"
                "while True:\n"
                "    sys.stderr.buffer.write(b'STOP_ERR' + b'E' * 8192)\n"
                "    sys.stderr.buffer.flush()\n"
                "    time.sleep(0.01)\n"
            ),
        ],
        timeout_sec=5,
        stop_fn=stop_after_first_chunk,
    )

    assert exit_code == -15
    assert "[KILLED: stop requested]" in stdout
    assert "STOP_ERR" in stderr
    assert "STOP_ERR" in output
    assert "[KILLED: stop requested]" in output


def test_run_popen_ignores_on_chunk_callback_failures():
    executor = object.__new__(SandboxExecutor)
    calls = 0

    def failing_callback(_partial: str) -> None:
        nonlocal calls
        calls += 1
        raise RuntimeError("callback failed")

    stdout, stderr, output, exit_code = executor._run_popen(
        [
            sys.executable,
            "-c",
            (
                "import sys, time\n"
                "sys.stdout.write('partial')\n"
                "sys.stdout.flush()\n"
                "time.sleep(2)\n"
            ),
        ],
        timeout_sec=5,
        stop_fn=None,
        on_chunk=failing_callback,
    )

    assert calls >= 1
    assert exit_code == 0
    assert stdout == "partial"
    assert output == "partial"
    assert stderr == ""
