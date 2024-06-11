"""Test Transform file"""

from transform import get_country


def test_get_country_valid() -> None:
    """Test valid country"""
    country_code = "UK"
    assert get_country(country_code) == "United Kingdom"
