"""Testing Transform file"""

import datetime

from transform import transform_data


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
            "scientific_name": ["Epipremnum aureum"],
            "soil_moisture": 93.0958352536302,
            "temperature": 13.137477117877957,
            "response": 200
        }]

    def test_tranform_data_valid(self) -> None:
        """Transform the useful data"""
        assert transform_data(self.sample_data) == [{
            'email': 'carl.linnaeus@lnhm.co.uk',
            'soil_moisture': 93.0958352536302,
            'temperature': 13.137477117877957,
            'timestamp': datetime.datetime(2024, 6, 10, 16, 1, 56),
            "plant_id": 0,
            'last_watered': datetime.datetime(2024, 6, 10, 14, 3, 4)
        }]

    def test_tranform_data_invalid(self) -> None:
        """Miss out any invalid data"""
        self.sample_data = [{
            "error": "plant not found",
            "plant_id": 7,
            "response": 400
        }]
        assert not transform_data(self.sample_data)
