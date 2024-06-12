"""This file is responsible for extracting plant data from the Heroku API."""

import json
import logging
from time import time
from os import path, mkdir

import requests

LOG_FOLDER = "log"
PLANT_DATA_HOST_URL = "https://data-eng-plants-api.herokuapp.com/plants/"
PLANT_DATA_RANGE = 51
MAX_TIMEOUT_IN_SECONDS = 10
MANDATORY_KEYS = [
    "botanist",
    "soil_moisture",
    "temperature",
    "recording_taken",
    "plant_id",
    "last_watered",
    "response"
]


def extract_relevant_data(plant_data: dict) -> dict:
    """Grabs and returns only the relevant information from the plant contents"""
    relevant_data = {}
    for key in MANDATORY_KEYS:
        if key in plant_data:
            relevant_data[key] = plant_data[key]
        else:
            logging.error("Missing key: %s", key)

    logging.info(relevant_data)
    return relevant_data


def get_response_from_api(plant_id: int,
                          host_url: str = PLANT_DATA_HOST_URL,
                          max_timeout: int = MAX_TIMEOUT_IN_SECONDS) -> dict:
    """Gets content from URL with specified plant id"""
    try:
        response = requests.get(host_url + str(plant_id), timeout=max_timeout)
        logging.info("Plant id %s retrieved.", plant_id)
    except requests.exceptions.Timeout:
        logging.error("Plant id %s timed out.", plant_id)
        return {"error": "request timed out",
                "plant_id": plant_id,
                "response": 400}

    json_contents = json.loads(response.content)
    json_contents["response"] = response.status_code
    return json_contents


def create_log() -> None:
    """Creates log folder and starts logging"""
    if not path.exists(LOG_FOLDER):
        mkdir(LOG_FOLDER)
    logging.basicConfig(filename=path.join(LOG_FOLDER, f"pipeline_{int(time())}.log"),
                        encoding="utf-8", level=logging.INFO)


def get_all_plant_data() -> list[dict]:
    """Gets all plant data hosted from an API"""
    create_log()
    list_of_plants = []

    for plant_id in range(PLANT_DATA_RANGE):
        plant_data = get_response_from_api(plant_id)
        list_of_plants.append(extract_relevant_data(plant_data))

    return list_of_plants


if __name__ == "__main__":
    plants = get_all_plant_data()

    for plant in plants:
        print("----------------------------")
        print(plant)
        print("----------------------------")
