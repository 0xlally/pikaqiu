from __future__ import annotations

import json
from pathlib import Path

import api_server


VISIBLE_RUN_KEYS = [
    "runId",
    "target",
    "goal",
    "status",
    "currentStage",
    "startedAt",
    "updatedAt",
    "currentNodeId",
    "currentActor",
    "nodes",
    "timeline",
    "toolCalls",
    "actionLogs",
    "parsingResults",
    "reasoningResults",
    "stateTable",
    "outputFile",
    "outputFileRelative",
]


def _reset_run_state() -> None:
    api_server._LATEST_RUN = None
    api_server._RUN_HISTORY.clear()
    api_server._RUN_INDEX.clear()


def test_upsert_persists_single_file_with_all_visible_run_fields(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("PIKAQIU_RUN_OUTPUT_DIR", str(tmp_path))
    _reset_run_state()

    run_summary = api_server._build_running_run_summary(
        run_id="run-test-001",
        feature_description="http://127.0.0.1:8080, get flag",
        reasoning_hint="focus auth",
    )

    api_server._upsert_run_summary_locked(run_summary)

    output_file = Path(run_summary["outputFile"])
    assert output_file.exists()

    payload = json.loads(output_file.read_text(encoding="utf-8"))
    assert payload["runId"] == "run-test-001"

    visible = payload["visibleRunData"]
    for key in VISIBLE_RUN_KEYS:
        assert key in visible

    assert visible["runId"] == run_summary["runId"]
    assert visible["timeline"] == run_summary["timeline"]
    assert visible["toolCalls"] == run_summary["toolCalls"]
    assert visible["actionLogs"] == run_summary["actionLogs"]

    _reset_run_state()
