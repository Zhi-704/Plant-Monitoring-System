"""Test Transform file"""

import datetime
from transform import get_country, transform_data

plant_data = [
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
            "medium_url": "https://perenual.com/storage/species_image/2773_epipremnum_aureum/medium/2560px-Epipremnum_aureum_31082012.jpg",
            "original_url": "https://perenual.com/storage/species_image/2773_epipremnum_aureum/og/2560px-Epipremnum_aureum_31082012.jpg",
            "regular_url": "https://perenual.com/storage/species_image/2773_epipremnum_aureum/regular/2560px-Epipremnum_aureum_31082012.jpg",
            "small_url": "https://perenual.com/storage/species_image/2773_epipremnum_aureum/small/2560px-Epipremnum_aureum_31082012.jpg",
            "thumbnail": "https://perenual.com/storage/species_image/2773_epipremnum_aureum/thumbnail/2560px-Epipremnum_aureum_31082012.jpg"
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


def test_get_country_valid() -> None:
    """Test valid country"""
    country_code = "BR"
    assert get_country(country_code) == "Brazil"


def test_tranform_data_name() -> None:
    """Test valid name"""
    data = transform_data(plant_data)[0]
    assert data["first_name"], data["last_name"] == "Carl Linnaeus"


def test_tranform_data_valid() -> None:
    """Transform the useful data"""
    assert transform_data(plant_data) == [{
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
        'town_name': 'Resplendor',
        'TZ_identifier': 'America/Sao_Paulo',
        'country_code': 'BR',
        'country_name': 'Brazil'}]


def test_tranform_data_invalid() -> None:
    """Miss out any invalid data"""
    plant_data = [{
        "error": "plant not found",
        "plant_id": 7,
        "response": 400
    }]
    assert not transform_data(plant_data)
