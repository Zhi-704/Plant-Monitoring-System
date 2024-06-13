"""Contains the tests for the load script"""

from unittest.mock import patch, MagicMock
from os import environ as ENV
import pytest
from load import get_connection, dictionary_to_tuple, \
    retrieve_botanist_ids_and_remove_botanist_emails, insert_readings


@patch("load.connect")
def test_get_connection_successful(mock_connect):
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


@patch("load.connect")
def test_get_connection_missing_key(mock_connect):
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


def test_dictionary_to_tuple():
    """Tests that all dictionaries are successfully turned into tuples."""

    test_input = [{"key1": "value1", "key2": "value2"},
                  {"key1": "value3", "key2": "value4"}]
    expected_output = [("value1", "value2"), ("value3", "value4")]

    assert dictionary_to_tuple(test_input) == expected_output


def test_retrieve_botanist_ids_and_remove_botanist_emails():
    """Tests that the output is as expected, and all methods are called
        the correct number of times."""

    mock_connection = MagicMock()
    mock_cursor_instance = MagicMock()
    mock_connection.cursor.return_value.__enter__.return_value = mock_cursor_instance

    mock_cursor_instance.fetchone.side_effect = [
        {"botanist_id": 1}, {"botanist_id": 2}]

    reading_dicts = [
        {"email": "email1@test.com", "other_key": "value1"},
        {"email": "email2@test.com", "other_key": "value2"},
    ]

    expected_output = [
        {"botanist_id": 1, "other_key": "value1"},
        {"botanist_id": 2, "other_key": "value2"},
    ]

    result = retrieve_botanist_ids_and_remove_botanist_emails(
        reading_dicts, mock_connection)

    assert result == expected_output

    assert mock_cursor_instance.execute.call_count == 2
    assert mock_cursor_instance.fetchone.call_count == 2


def test_insert_readings():
    """Tests that the method is called correctly, and only once."""

    mock_connection = MagicMock()
    mock_cursor_instance = MagicMock()
    mock_connection.cursor.return_value.__enter__.return_value = mock_cursor_instance

    reading_tuples = [
        (1, 2, "2021-01-01 00:00:00", 1, "2021-01-01", 1),
        (3, 4, "2021-01-01 00:00:00", 2, "2021-01-01", 2),
    ]

    insert_readings(reading_tuples, mock_connection)

    statement = """
                    INSERT INTO delta.reading(soil_moisture, temperature, timestamp, plant_id, last_watered, botanist_id)
                    VALUES
                        (%s, %s, %s, %s, %s, %s)
                    """

    mock_cursor_instance.executemany.assert_called_once_with(
        statement, reading_tuples)

    mock_connection.commit.assert_called_once()
