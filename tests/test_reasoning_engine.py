from pathlib import Path

import pytest

from agents.reasoning import ReasoningAgent
from core.mapping import TestFamilyMapper
from reasoning.engine import FeatureReasoningEngine
from reasoning.models import ParsingObservation, make_observation_item
from tests.fakes import FakeRuntime


def build_engine() -> FeatureReasoningEngine:
    return FeatureReasoningEngine.from_file(Path("config/reasoning_family_rules.json"))


@pytest.mark.parametrize(
    ("observation", "expected_primary_family", "expected_secondary_families"),
    [
        (
            ParsingObservation(
                discovered_endpoints=[make_observation_item("/api/users/{user_id}", "e1")],
                discovered_actions=[make_observation_item("view user detail", "e2")],
            ),
            "object_access_control",
            [],
        ),
        (
            ParsingObservation(
                discovered_actions=[make_observation_item("edit profile", "e1")],
                discovered_fields=[
                    make_observation_item("nickname", "e2"),
                    make_observation_item("avatar", "e3"),
                    make_observation_item("signature", "e4"),
                    make_observation_item("role", "e5"),
                ],
            ),
            "property_access_control",
            [],
        ),
        (
            ParsingObservation(
                discovered_actions=[make_observation_item("admin export all orders", "e1")],
                discovered_roles=[make_observation_item("admin", "e2")],
                discovered_objects=[make_observation_item("orders", "e3")],
            ),
            "function_access_control",
            ["quota_abuse_logic"],
        ),
        (
            ParsingObservation(
                discovered_flows=[make_observation_item("apply -> approve order", "e1")],
                discovered_actions=[make_observation_item("approve order", "e2")],
            ),
            "workflow_state_logic",
            ["function_access_control"],
        ),
        (
            ParsingObservation(
                discovered_actions=[make_observation_item("send code by sms", "e1")],
                discovered_endpoints=[make_observation_item("/api/send-code", "e2")],
            ),
            "quota_abuse_logic",
            [],
        ),
        (
            ParsingObservation(
                discovered_actions=[make_observation_item("search users", "e1")],
                discovered_fields=[make_observation_item("query", "e2"), make_observation_item("filter", "e3")],
            ),
            "server_input_interpretation",
            [],
        ),
        (
            ParsingObservation(
                discovered_upload_points=[make_observation_item("upload attachment", "e1")],
                discovered_actions=[make_observation_item("preview attachment", "e2")],
            ),
            "file_content_handling",
            [],
        ),
        (
            ParsingObservation(
                discovered_flows=[make_observation_item("login and token refresh flow", "e1")],
                discovered_endpoints=[make_observation_item("/api/token/refresh", "e2")],
            ),
            "auth_session_security",
            [],
        ),
        (
            ParsingObservation(
                discovered_render_points=[make_observation_item("comment markdown display", "e1")],
                discovered_actions=[make_observation_item("render comment preview", "e2")],
            ),
            "client_render_execution",
            ["file_content_handling"],
        ),
        (
            ParsingObservation(
                discovered_callback_points=[make_observation_item("webhook callback url configuration", "e1")],
                discovered_fields=[make_observation_item("callback url", "e2")],
            ),
            "server_outbound_callback",
            [],
        ),
    ],
)
def test_reasoning_engine_maps_feature_cases(
    observation: ParsingObservation,
    expected_primary_family: str,
    expected_secondary_families: list[str],
) -> None:
    decision = build_engine().analyze(observation)

    assert len(decision.identified_features) >= 1
    assert len(decision.family_mapping) >= 1
    assert decision.family_mapping[0].primary_family_id == expected_primary_family
    assert decision.proposed_test_nodes[0].node_type.value == "test"
    assert decision.proposed_test_nodes[0].primary_family_id == expected_primary_family
    assert decision.family_mapping[0].reasons
    for family_id in expected_secondary_families:
        assert family_id in decision.family_mapping[0].family_ids


def test_reasoning_engine_supports_multiple_features_in_one_observation() -> None:
    decision = build_engine().analyze(
        ParsingObservation(
            discovered_actions=[make_observation_item("login", "e1")],
            discovered_callback_points=[make_observation_item("webhook callback url", "e2")],
        )
    )

    primary_families = {item.primary_family_id for item in decision.family_mapping}

    assert len(decision.identified_features) == 2
    assert "auth_session_security" in primary_families
    assert "server_outbound_callback" in primary_families
    assert len(decision.proposed_test_nodes) == 2


def test_reasoning_agent_exposes_structured_observation_entrypoint() -> None:
    engine = build_engine()
    reasoning_agent = ReasoningAgent(
        runtime=FakeRuntime(),
        mapper=TestFamilyMapper.from_file(Path("config/test_family_mapping.json")),
        feature_engine=engine,
    )

    decision = reasoning_agent.analyze_structured_observation(
        ParsingObservation(
            discovered_actions=[make_observation_item("search users", "e1")],
            discovered_fields=[make_observation_item("query", "e2"), make_observation_item("filter", "e3")],
        )
    )

    assert decision.family_mapping[0].primary_family_id == "server_input_interpretation"
    assert decision.proposed_test_nodes[0].family_ids[0] == "server_input_interpretation"
