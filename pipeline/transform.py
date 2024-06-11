"""Transform file"""

from datetime import datetime
from json import load
import pycountry


DATE_FORMAT = "%a, %d %b %Y %H:%M:%S GMT"
DATA_FILE = "plant.json"


def get_data() -> list[dict]:
    """Returns data from the herokuapp"""
    with open(DATA_FILE, encoding="utf-8") as f:
        return load(f)


def get_country(country_code: str) -> str:
    """From the country code, get the country name"""
    country = pycountry.countries.get(alpha_2=country_code)
    return country.name


def get_name(name: str) -> list[str]:
    """Splits the full name into first and last name"""
    return name.split()


def transform_data(plant_data: list[dict]) -> list[dict]:
    """Selects useful data and transform to correct data type"""
    data = []
    for plant in plant_data[:1]:
        if plant["response"] != 200:
            continue

        name = plant["botanist"]["name"]
        first_name, last_name = name.split()

        country_code = plant["origin_location"][3]
        country_name = get_country(country_code)

        data.append({
            "first_name": first_name,
            "last_name": last_name,
            "email": plant["botanist"]["email"],
            "phone": plant["botanist"]["phone"],
            "soil_moisture": float(plant["soil_moisture"]),
            "temperature": float(plant["temperature"]),
            "timestamp": datetime.fromisoformat(plant["recording_taken"]),
            "plant_id": int(plant["plant_id"]),
            "regular_name": plant["name"],
            "scientific_name": plant.get("scientific_name"),
            "last_watered": datetime.strptime(plant["last_watered"], DATE_FORMAT),
            "town_name": plant["origin_location"][2],
            "TZ_identifier": plant["origin_location"][4],
            "country_code": country_code,
            "country_name": country_name
        })

    return data


if __name__ == "__main__":
    print(transform_data(get_data()))
