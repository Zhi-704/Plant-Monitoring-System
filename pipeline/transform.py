"""This file receives the plant data from the extract file and transforms it for the load file"""

import logging
from datetime import datetime

from extract import get_all_plant_data


DATE_FORMAT = "%a, %d %b %Y %H:%M:%S GMT"


def transform_data(plant_data: list[dict]) -> list[dict]:
    """Selects useful data and transform to correct data type"""
    data = []
    for plant in plant_data:
        if plant["response"] == 200:
            reading_data = {
                "email": plant["botanist"]["email"],
                "soil_moisture": float(plant["soil_moisture"]),
                "temperature": float(plant["temperature"]),
                "timestamp": datetime.fromisoformat(plant["recording_taken"]),
                "plant_id": int(plant["plant_id"]),
                "last_watered": datetime.strptime(plant["last_watered"], DATE_FORMAT)
            }

            logging.info(reading_data)
            data.append(reading_data)

    return data


if __name__ == "__main__":
    plants = transform_data(get_all_plant_data())
    for row in plants:
        print(row)
