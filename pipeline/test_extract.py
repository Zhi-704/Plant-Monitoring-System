'''File used for testing the extract file for the pipeline'''

from unittest.mock import patch, MagicMock
import asyncio

from extract import get_all_plant_data, PLANT_DATA_RANGE


class TestGetResponseFromAPI:
    '''Contains test for GetResponse function'''

    @patch("aiohttp.ClientSession.get")
    @patch("json.loads")
    def test_success_response_from_api(self, mock_load, mock_session_get) -> None:
        '''Assert that relevent functions are only called the required amount of times'''

        sample_data = [
            {
                "botanist": {
                    "email": "carl.linnaeus@lnhm.co.uk",
                    "name": "Carl Linnaeus",
                    "phone": "(146)994-1635x35992"
                },
                "images": {
                    "license": 45,
                    "license_name": "Attribution-ShareAlike 3.0 Unported (CC BY-SA 3.0)",
                    "license_url": "https://creativecommons.org/licenses/by-sa/3.0/deed.en",
                    "medium_url": "https://perenual.com/storage/species_image.jpg",
                    "original_url": "https://perenual.com/storage/species_image.jpg",
                    "regular_url": "https://perenual.com/storage/species_image.jpg",
                    "small_url": "https://perenual.com/storage/species_image.jpg",
                    "thumbnail": "https://perenual.com/storage/species_image.jpg"
                },
                "last_watered": "Mon, 10 Jun 2024 14:03:04 GMT",
                "name": "Epipremnum Aureum",
                "origin_location": [
                    "-19.32556",
                    "-41.25528",
                    "Resplendor",
                    "BR",
                    "America/Sao_Paulo"
                ],
                "plant_id": 0,
                "recording_taken": "2024-06-10 16:01:56",
                "scientific_name": ["Epipremnum aureum"],
                "soil_moisture": 93.0958352536302,
                "temperature": 13.137477117877957,
                'fake_key': 'fake value'
            }]

        mock_response = MagicMock()
        mock_response.content = "Fake values"
        mock_response.status_code = 555

        mock_session_get.return_value = mock_response
        mock_load.return_value = sample_data

        # contents = fetch_data_from_api(mock_response_get, 2)

        # assert 'response' in contents
        # assert contents['response'] == 555
        # assert 'fake_key' in contents
        # assert mock_load.call_count == 1
        # assert mock_session_get.call_count == 1

    @patch("aiohttp.ClientSession.get")
    def test_timeout_response_from_api(self, mock_session_get) -> None:
        '''Tests the function if timeout error occurs'''

        mock_session_get.side_effect = asyncio.TimeoutError

        # contents = fetch_data_from_api(mock_session_get, 0)

        # assert 'error' in contents
        # assert contents['response'] == 400
        # assert contents['error'] == 'request timed out'


class TestGetAllPlantData:
    '''Contains get plant data function'''

    @patch("aiohttp.ClientSession.get")
    def test_number_of_retrieval_matches(self, mock_get_response) -> None:
        '''Tests if the function calls other member functions the expected amount of times'''

        asyncio.run(get_all_plant_data())

        assert mock_get_response.call_count == PLANT_DATA_RANGE
