'''File used for testing the archive file for the storing long term data'''
import pytest
from unittest.mock import patch, MagicMock
from archive import get_connection, get_data_from_rds, upload_data_to_s3
from os import environ as ENV
from pymssql import exceptions


class TestGetConnection:
    '''Contains tests for get connection function'''

    @patch("archive.connect")
    def test_get_connection_successful(self, mock_connect):
        """Tests that a connection is made successfully."""

        mock_connect.return_value = MagicMock()

        ENV["DB_HOST"] = "test_host"
        ENV["DB_PORT"] = "1234"
        ENV["DB_USER"] = "test_user"
        ENV["DB_PASSWORD"] = "test_password"
        ENV["DB_NAME"] = "test_db"

        connection = get_connection()

        assert connection == mock_connect.return_value

        mock_connect.assert_called_once_with(
            server="test_host",
            port="1234",
            user="test_user",
            password="test_password",
            database="test_db",
            as_dict=True,
        )

    @patch("archive.connect")
    def test_get_connection_missing_key(self, mock_connect):
        """Tests that a KeyError is raised if a credential is missing
            from the .env file."""

        mock_connect.return_value = MagicMock()

        ENV = {
            "DB_HOST": "test_host",
            "DB_PORT": "1234",
            "DB_PASSWORD": "test_password",
            "DB_NAME": "test_db",
        }

        with patch.dict("os.environ", ENV, clear=True):
            with pytest.raises(KeyError) as exc_info:
                get_connection()

        mock_connect.assert_not_called()
        assert str(
            exc_info.value) == "\"'DB_USER' missing from environment variables.\""


class TestGetDataFromRDS:
    '''Contains tests for getting data from the database function'''

    @patch('archive.Connection')
    def test_get_data_success(self, mock_connection):
        """Test successful data retrieval from the RDS database."""
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [{'id': 1, 'value': 'test'}]

        data = get_data_from_rds(mock_connection, 'test_table')

        assert mock_cursor.execute.call_count == 1
        assert data == [{'id': 1, 'value': 'test'}]

    @patch('archive.Connection')
    def test_get_data_programming_error(self, mock_connection):
        """Test handling of a ProgrammingError during data retrieval."""
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.execute.side_effect = exceptions.ProgrammingError(
            "Error in query")

        data = get_data_from_rds(mock_connection, 'test_table')

        assert mock_cursor.execute.call_count == 1
        assert not data
        assert mock_connection.rollback.call_count == 1


class TestUploadDataToS3:
    '''Contains tests for uploading data to an s3 bucket'''

    @patch('archive.upload_file_to_bucket')
    @patch('archive.load_into_csv')
    @patch('archive.get_data_from_rds')
    def test_upload_data_to_s3(self, mock_get_data_from_rds, mock_load_into_csv, mock_upload_file_to_bucket):
        """Test the upload_data_to_s3 function including missing data."""

        mock_s3_client = MagicMock()
        mock_conn = MagicMock()
        curr_time = '2024-06-13-15-30-00'
        mock_tables = ['table1', 'table2', 'reading']
        mock_metadata = 'metadata/'
        mock_reading = 'reading/'
        fake_folder_path = 'humpty-dumpty'
        ENV["BUCKET_NAME"] = "my_bucket"

        mock_get_data_from_rds.side_effect = [
            [{'id': 1, 'value': 'test1'}],
            [{'id': 2, 'value': 'test2'}],
            []
        ]

        with patch('archive.TABLES_IN_DATABASE', mock_tables), \
                patch('archive.METADATA_FOLDER', mock_metadata), \
                patch('archive.READING_FOLDER', mock_reading):
            upload_data_to_s3(mock_s3_client, mock_conn,
                              fake_folder_path, curr_time)

        mock_get_data_from_rds.assert_any_call(mock_conn, 'table1')
        mock_get_data_from_rds.assert_any_call(mock_conn, 'table2')
        mock_get_data_from_rds.assert_any_call(mock_conn, 'reading')

        mock_load_into_csv.assert_any_call(
            [{'id': 1, 'value': 'test1'}], f'{fake_folder_path}/table1_data.csv')
        mock_load_into_csv.assert_any_call(
            [{'id': 2, 'value': 'test2'}], f'{fake_folder_path}/table2_data.csv')

        mock_upload_file_to_bucket.assert_any_call(
            mock_s3_client, f'{fake_folder_path}/table1_data.csv', ENV["BUCKET_NAME"], f'{mock_metadata}table1_data.csv')
        mock_upload_file_to_bucket.assert_any_call(
            mock_s3_client, f'{fake_folder_path}/table2_data.csv', ENV["BUCKET_NAME"], f'{mock_metadata}table2_data.csv')

        assert mock_get_data_from_rds.call_count == 3
        assert mock_load_into_csv.call_count == 2
        assert mock_upload_file_to_bucket.call_count == 2
