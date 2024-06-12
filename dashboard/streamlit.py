"""Creates dashboard with streamlit"""

import pycountry


def get_country(country_code: str) -> str | None:
    """From the country code, get the country name"""
    country = pycountry.countries.get(alpha_2=country_code)
    return country.name if country else None


def create_dashboard() -> None:
    """Create a dashboard to view information about the plants"""
    country_code = "BR"  # plant["origin_location"][3]
    country_name = get_country(country_code)


if __name__ == "__main__":
    create_dashboard()
