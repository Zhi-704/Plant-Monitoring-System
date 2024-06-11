'''This file is responsible for extracting plant data from the Heroku API. Returns a list of dictionaries'''

import requests
import json

PLANT_DATA_HOST_URL = "https://data-eng-plants-api.herokuapp.com/plants/"
MANDATORY_KEYS = [
    'botanist',
    'last_watered',
    'plant_id',
    'recording_taken',
    'soil_moisture',
    'temperature',
    'origin_location',
    'name',
    'scientific name'
]


def extract_plant_data(plant_data: dict) -> dict:
    '''Grabs and returns only the relevant information from the plant contents'''
    pass


def get_response_from_API(plant_id: int, host_url: str = PLANT_DATA_HOST_URL) -> None:
    '''Gets content from URL with specified plant id'''
    response = requests.get(host_url + str(plant_id))
    print("Response:", response)

    json_contents = json.loads(response.content)
    print("json_stuff")
    print(json_contents)
    return json_contents


def is_keys_in_json(dict_to_be_checked: dict, keys: list) -> bool:
    '''Checks if the keys exist in the dictionary'''
    for key in keys:
        if key not in dict_to_be_checked:
            return False
    return True


if __name__ == "__main__":
    dict_to_check = get_response_from_API(8)
    print("City: ", dict_to_check['origin_location'][2])
