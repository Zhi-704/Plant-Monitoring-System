'''File used for testing the extract file for the pipeline'''

from unittest.mock import patch, MagicMock
import requests

import extract


class TestExtractRelevantData:
    '''Contains test for if function extracts relevant data'''

    def test_extract_returns_necessary_information(self) -> None:
        '''Tests if information such as image is removed correctly'''

        sample_base_data = {
            'botanist': 'John Doe',
            'last_watered': '2024-06-10',
            'plant_id': 1,
            'recording_taken': '2024-06-11',
            'soil_moisture': 80,
            'image': "fake url",
            'temperature': 25,
            'origin_location': 'South America',
            'name': 'Aloe Vera',
            'scientific_name': 'Aloe vera',
            'response': 200
        }
        extracted_data = extract.extract_relevant_data(sample_base_data)
        assert 'image' not in extracted_data

    def test_extract_returns_input_if_missing_key(self) -> None:
        '''Tests if function returns original input if there are missing keys'''

        sample_missing_data = {
            'botanist': 'John Doe',
            'last_watered': '2024-06-10',
            'plant_id': 1,
            'response': 200,
            'fake_key': 'fake value'
        }
        extracted_data = extract.extract_relevant_data(sample_missing_data)
        assert 'botanist' in extracted_data

    def test_extract_returns_input_if_missing_key_error_data(self) -> None:
        '''Tests if error message is preserved when passed into function'''
        sample_error_data = {
            'error': 'plant sensor fault',
            'plant_id': 8
        }
        extracted_data = extract.extract_relevant_data(sample_error_data)
        assert extracted_data == {'plant_id': 8}


class TestGetResponseFromAPI:
    '''Contains test for GetResponse function'''

    @patch("requests.get")
    @patch("json.loads")
    def test_success_response_from_api(self, mock_load, mock_request_get) -> None:
        '''Assert that relevent functions are only called the required amount of times'''

        sample_data = {
            'botanist': 'John Doe',
            'last_watered': '2024-06-10',
            'plant_id': 1,
            'fake_key': 'fake value'
        }

        mock_response = MagicMock()
        mock_response.content = "Fake values"
        mock_response.status_code = 555

        mock_request_get.return_value = mock_response
        mock_load.return_value = sample_data

        contents = extract.get_response_from_api(2)

        assert 'response' in contents
        assert contents['response'] == 555
        assert 'fake_key' in contents
        assert mock_load.call_count == 1
        assert mock_request_get.call_count == 1

    @patch("requests.get")
    def test_timeout_response_from_api(self, mock_request_get) -> None:
        '''Tests the function if timeout error occurs'''

        mock_request_get.side_effect = requests.exceptions.Timeout()

        contents = extract.get_response_from_api(2)

        assert 'error' in contents
        assert contents['response'] == 400
        assert contents['error'] == 'request timed out'


class TestGetAllPlantData:
    '''Contains get plant data function'''

    @patch("extract.get_response_from_api")
    def test_number_of_retrieval_matches(self, mock_get_response) -> None:
        '''Tests if the function calls other member functions the expected amount of times'''

        extract.get_all_plant_data()

        assert mock_get_response.call_count == extract.PLANT_DATA_RANGE
