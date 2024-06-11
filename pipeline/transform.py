"""Transform file"""
from json import load


def get_data() -> None:
    """Returns data from the herokuapp"""
    with open("plant.json", encoding="utf-8") as f:
        return load(f)


def get_country(country_code: str) -> str:
    """From the country code, get the country name"""
    print(country_code)


def main() -> None:
    data = get_data()
    for i in data:
        if i.get("origin_location"):
            country_code = i["origin_location"][3]
            country = get_country(country_code)


if __name__ == "__main__":
    main()
