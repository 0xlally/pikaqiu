from pathlib import Path

from core.models import StateItem, StateTableDelta
from core.state_table import StateTableStore


def test_state_table_merge_update_json_and_markdown(tmp_path: Path) -> None:
    store = StateTableStore()
    store.update(
        identities=[StateItem(title="admin-cookie", content="role=admin", refs=["e1"], source="node-1")],
        notes=["Need csrf token before password reset"],
    )
    store.merge(
        StateTableDelta(
            session_materials=[StateItem(title="jwt", content="Bearer token from login", refs=["e2"])],
            key_entrypoints=[StateItem(title="login", content="/api/login", refs=["e3"])],
            workflow_prerequisites=[StateItem(title="captcha", content="captcha required before submit")],
            reusable_artifacts=[StateItem(title="request-template", content="login request with headers")],
            session_risks=[StateItem(title="fixation", content="token not rotated after auth")],
            notes=["Need csrf token before password reset", "Captcha may be bypassable"],
        )
    )

    saved_path = store.save_json(tmp_path / "state_table.json")
    loaded_store = StateTableStore.load_json(saved_path)
    markdown = loaded_store.to_markdown()

    assert saved_path.exists()
    assert len(loaded_store.model.identities) == 1
    assert len(loaded_store.model.notes) == 2
    assert loaded_store.model.key_entrypoints[0].content == "/api/login"
    assert "## session_risks" in markdown
    assert "Captcha may be bypassable" in markdown
