import pytest

from streamlit import get_country


class TestGetCountry:
    """Tests the get country function"""

    @pytest.mark.parametrize("country_code, expected_country", [
        ("BR", "Brazil"),
        ("US", "United States"),
        ("IN", "India"),
        ("CN", "China"),
        ("JP", "Japan"),
    ])
    def test_get_country_valid(self, country_code: str, expected_country: str) -> None:
        """Test valid country"""
        assert get_country(country_code) == expected_country

    @pytest.mark.parametrize("invalid_input, output", [
        ("BfdsfsdfdsR", None),
        ("12213", None),
        ("IND", None),
        ("C3", None),
        ("", None),
    ])
    def test_get_country_invalid(self, invalid_input: str, output: str) -> None:
        """Test invalid country codes"""
        assert get_country(invalid_input) == output
