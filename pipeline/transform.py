"""This file receives the plant data from the extract file and transforms it for the load file"""

import logging
from datetime import datetime

import pycountry

from extract import get_all_plant_data


DATE_FORMAT = "%a, %d %b %Y %H:%M:%S GMT"
DATA_FILE = "plant.json"


def get_country(country_code: str) -> str:
    """From the country code, get the country name"""
    country = pycountry.countries.get(alpha_2=country_code)
    if country:
        return country.name
    return None


def transform_data(plant_data: list[dict]) -> list[dict]:
    """Selects useful data and transform to correct data type"""
    data = []
    for plant in plant_data:
        if plant["response"] != 200:
            continue

        name = plant["botanist"]["name"]
        first_name, last_name = name.split()

        country_code = plant["origin_location"][3]
        country_name = get_country(country_code)

        transformed_data = {
            "first_name": first_name,
            "last_name": last_name,
            "email": plant["botanist"]["email"],
            "phone": plant["botanist"]["phone"],
            "soil_moisture": float(plant["soil_moisture"]),
            "temperature": float(plant["temperature"]),
            "timestamp": datetime.fromisoformat(plant["recording_taken"]),
            "plant_id": int(plant["plant_id"]),
            "regular_name": plant.get("name"),
            "scientific_name": plant.get("scientific_name"),
            "last_watered": datetime.strptime(plant["last_watered"], DATE_FORMAT),
            "latitude": plant["origin_location"][0],
            "longitude": plant["origin_location"][1],
            "town_name": plant["origin_location"][2],
            "country_code": country_code,
            "country_name": country_name,
            "TZ_identifier": plant["origin_location"][4]
        }

        logging.info(transformed_data)
        data.append(transformed_data)

    return data


if __name__ == "__main__":
    plants = transform_data(get_all_plant_data())
    for row in plants:
        print(row)
