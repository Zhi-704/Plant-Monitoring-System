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
            "images": {
                "license": 45,
                "license_name": "Attribution-ShareAlike 3.0 Unported (CC BY-SA 3.0)",
                "license_url": "https://creativecommons.org/licenses/by-sa/3.0/deed.en",
                "medium_url": "https://perenual.com/storage/species_image.jpg",
                "original_url": "https://perenual.com/storage/species_image.jpg",
                "regular_url": "https://perenual.com/storage/species_image.jpg",
                "small_url": "https://perenual.com/storage/species_image.jpg",
                "thumbnail": "https://perenual.com/storage/species_image.jpg"
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
            "temperature": 13.137477117877957
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

    def test_transform_returns_necessary_information(self) -> None:
        '''Tests if information such as image is removed correctly'''
        extracted_data = transform_data(self.sample_data)
        assert 'image' not in extracted_data

    def test_tranform_data_invalid(self) -> None:
        """Miss out any invalid data"""
        self.sample_data = [{
            "error": "plant not found",
            "plant_id": 7
        }]
        assert not transform_data(self.sample_data)

    def test_transform_error_data(self) -> None:
        '''Tests if data with error message are removed'''
        sample_error_data = [{
            'error': 'plant sensor fault',
            'plant_id': 8
        }]
        extracted_data = transform_data(sample_error_data)
        assert not extracted_data
