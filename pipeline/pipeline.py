"""Runs the whole ETL pipeline"""

from extract import get_all_plant_data
from transform import transform_data
from load import insert_to_database
import asyncio

if __name__ == "__main__":
    raw_data = asyncio.run(get_all_plant_data())
    clean_data = transform_data(raw_data)
    insert_to_database(clean_data)
