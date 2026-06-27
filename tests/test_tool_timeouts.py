from types import SimpleNamespace

from pikaqiu_agent.tools import create_all_tools, create_bash_tool, create_python_tool, create_web_fetch_tool


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


def test_web_fetch_uses_mission_timeout_semantics():
    sandbox = FakeSandbox()
    tool = create_web_fetch_tool(sandbox, "/work", max_timeout=300)

    tool.invoke({"url": "https://example.com"})
    tool.invoke({"url": "https://example.com", "timeout": 70})
    tool.invoke({"url": "https://example.com", "timeout": 999})

    assert [call[2] for call in sandbox.calls] == [300, 70, 300]


def test_all_tools_expose_only_expected_default_names():
    sandbox = FakeSandbox()
    tools = create_all_tools(sandbox, "/work", command_timeout_sec=300)
    names = {tool.name for tool in tools}

    assert names == {"bash_exec", "python_exec", "web_fetch"}
