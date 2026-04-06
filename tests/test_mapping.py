from pathlib import Path

from core.mapping import TestFamilyMapper
from core.models import FeaturePoint


def test_login_feature_maps_to_auth_related_families() -> None:
    mapper = TestFamilyMapper.from_file(Path("config/test_family_mapping.json"))
    feature = FeaturePoint.from_description(
        "Admin login endpoint /api/login uses username password and captcha for administrators."
    )

    recommendations = mapper.recommend(feature)
    family_ids = [item.family.id for item in recommendations]

    assert "auth_bypass" in family_ids
    assert "session_management" in family_ids
    assert family_ids[0] == "auth_bypass"
