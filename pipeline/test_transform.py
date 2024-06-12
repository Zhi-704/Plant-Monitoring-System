"""Testing Transform file"""

import datetime

import pytest

from transform import get_country, transform_data


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


class TestTransformData:
    """Tests the transform data function"""

    sample_data = [
        {
            "botanist": {
                "email": "carl.linnaeus@lnhm.co.uk",
                "name": "Carl Linnaeus",
                "phone": "(146)994-1635x35992"
            },
            "last_watered": "Mon, 10 Jun 2024 14:03:04 GMT",
            "name": "Epipremnum Aureum",
            "origin_location": [
                    "-19.32556",
                    "-41.25528",
                    "Resplendor",
                    "BR",
                    "America/Sao_Paulo"
            ],
            "plant_id": 0,
            "recording_taken": "2024-06-10 16:01:56",
            "scientific_name": [
                "Epipremnum aureum"
            ],
            "soil_moisture": 93.0958352536302,
            "temperature": 13.137477117877957,
            "response": 200
        }]

    def test_tranform_data_name(self) -> None:
        """Test valid name"""
        data = transform_data(self.sample_data)[0]
        assert data["first_name"], data["last_name"] == "Carl Linnaeus"

    def test_tranform_data_valid(self) -> None:
        """Transform the useful data"""
        assert transform_data(self.sample_data) == [{
            'first_name': 'Carl',
            'last_name': 'Linnaeus',
            'email': 'carl.linnaeus@lnhm.co.uk',
            'phone': '(146)994-1635x35992',
            'soil_moisture': 93.0958352536302,
            'temperature': 13.137477117877957,
            'timestamp': datetime.datetime(2024, 6, 10, 16, 1, 56),
            'plant_id': 0,
            'regular_name': 'Epipremnum Aureum',
            'scientific_name': ['Epipremnum aureum'],
            'last_watered': datetime.datetime(2024, 6, 10, 14, 3, 4),
            'latitude': '-19.32556',
            'longitude': '-41.25528',
            'town_name': 'Resplendor',
            'country_code': 'BR',
            'country_name': 'Brazil',
            'TZ_identifier': 'America/Sao_Paulo'}]

    def test_tranform_data_invalid(self) -> None:
        """Miss out any invalid data"""
        self.sample_data = [{
            "error": "plant not found",
            "plant_id": 7,
            "response": 400
        }]
        assert not transform_data(self.sample_data)
