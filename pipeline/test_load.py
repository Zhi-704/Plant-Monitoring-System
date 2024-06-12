"""Contains the tests for the load scrip"""

from load import dictionary_to_tuple
import datetime


def test_dictionary_to_tuple():
    test_data = [{'soil_moisture': 90.62276785339806,
                  'temperature': 13.60574842875693,
                  'timestamp': datetime.datetime(2024, 6, 12, 16, 46, 56),
                  'plant_id': 33,
                  'last_watered': datetime.datetime(2024, 6, 12, 14, 5, 58),
                  'botanist_id': 1}]

    assert dictionary_to_tuple(test_data) == [
        (90.62276785339806, 13.60574842875693, datetime.datetime(2024, 6, 12, 16, 46, 56), 33, datetime.datetime(2024, 6, 12, 14, 5, 58), 1)]
