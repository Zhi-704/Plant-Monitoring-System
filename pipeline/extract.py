"""This file is responsible for extracting plant data from the Heroku API."""

from time import time, perf_counter
from os import path, mkdir
import logging
import asyncio

import aiohttp

LOG_FOLDER = "log"
PLANT_DATA_HOST_URL = "https://data-eng-plants-api.herokuapp.com/plants/"
PLANT_DATA_RANGE = 51
MAX_TIMEOUT_IN_SECONDS = 100
MANDATORY_KEYS = [
    "botanist",
    "soil_moisture",
    "temperature",
    "recording_taken",
    "plant_id",
    "last_watered",
    "response"
]


async def fetch_data_from_api(session, plant_id: int,
                              host_url: str = PLANT_DATA_HOST_URL,
                              max_timeout: int = MAX_TIMEOUT_IN_SECONDS) -> dict:
    """Gets content from URL with specified plant id"""
    try:
        async with session.get(host_url + str(plant_id), timeout=max_timeout) as response:
            logging.info("Plant id %s data called.", plant_id)
            return await response.json()

    except asyncio.TimeoutError:
        logging.error("Plant id %s timed out.", plant_id)
        return {"error": "request timed out",
                "plant_id": plant_id,
                "response": 400}


def create_log() -> None:
    """Creates log folder and starts logging"""
    if not path.exists(LOG_FOLDER):
        mkdir(LOG_FOLDER)
    logging.basicConfig(filename=path.join(LOG_FOLDER, f"pipeline_{int(time())}.log"),
                        encoding="utf-8", level=logging.INFO)


async def get_all_plant_data() -> list[dict]:
    """Gets all plant data hosted from an API"""
    create_log()

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_data_from_api(session, plant_id)
                 for plant_id in range(PLANT_DATA_RANGE)]
        responses = await asyncio.gather(*tasks)

    return responses


if __name__ == "__main__":
    start = perf_counter()
    plants = asyncio.run(get_all_plant_data())

    for plant in plants:
        print(plant)
        print("----------------------------")
    print(perf_counter() - start)
