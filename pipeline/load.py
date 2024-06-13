"""Script for loading the transformed plant data to the Microsoft SQL Server Database"""

from os import environ as ENV
import logging
import asyncio

from dotenv import load_dotenv
from pymssql import connect, Connection, exceptions  # pylint: disable=no-name-in-module

from extract import get_all_plant_data
from transform import transform_data


def get_connection() -> Connection:
    """Creates a connection to the database, returning a connection object."""

    try:
        logging.info("Connected to database")
        return connect(
            server=ENV["DB_HOST"],
            port=ENV["DB_PORT"],
            user=ENV["DB_USER"],
            password=ENV["DB_PASSWORD"],
            database=ENV["DB_NAME"],
            as_dict=True,
        )
    except KeyError as e:
        logging.error("%s missing from environment variables.", e)
        raise KeyError(f"{e} missing from environment variables.") from e
    except exceptions.OperationalError as e:
        logging.error("Error connecting to database: %s", e)
        raise exceptions.OperationalError(
            f"Error connecting to database: {e}") from e


def dictionary_to_tuple(reading_dicts: list[dict]) -> list[tuple]:
    """Converts the transformed plant reading data from a list of dictionaries
        to a list of tuples, returning the list."""
    return [tuple(reading.values()) for reading in reading_dicts]


def retrieve_botanist_ids_and_remove_botanist_emails(
        reading_dicts: list[dict], connection: Connection) -> list[dict]:
    """Queries the database and retrieves the corresponding botanist ID for each reading
        via their associated email in the reading dict, adding it to each plant reading
        data dictionary and removing the email."""

    with connection.cursor() as cursor:
        for reading in reading_dicts:
            email = reading["email"]

            query = "SELECT botanist_id FROM delta.botanist WHERE email = %s"
            cursor.execute(query, email)

            result = cursor.fetchone()
            if result:
                reading["botanist_id"] = result["botanist_id"]
            else:
                logging.error("Botanist with email %s not found in database.", email)
                raise ValueError(f"Botanist with email {\
                                 email} not found in database.")

            reading.pop("email")

    return reading_dicts


def insert_readings(reading_tuples: list[tuple], connection: Connection) -> None:
    """Batch-inserts the plant reading data into the Microsoft SQL Server Database."""

    with connection.cursor() as cursor:
        logging.info("Inserting to database")
        statement = """
                    INSERT INTO delta.reading(soil_moisture, temperature, timestamp, plant_id, last_watered, botanist_id)
                    VALUES
                        (%s, %s, %s, %s, %s, %s)
                    """
        cursor.executemany(statement, reading_tuples)

    connection.commit()
    logging.info("Inserted to database!")

def insert_to_database(transformed_data: list[dict]) -> None:
    """Inserts the transformed plant data into the database"""
    load_dotenv()

    try:
        conn = get_connection()

        reading_data = retrieve_botanist_ids_and_remove_botanist_emails(
            transformed_data, conn)

        reading_tuples = dictionary_to_tuple(reading_data)

        insert_readings(reading_tuples, conn)

    except Exception as e:
        logging.error("An error occurred: %s", e)
        raise Exception(f"An error occurred: {e}") from e
    finally:
        conn.close()


if __name__ == "__main__":
    raw_data = asyncio.run(get_all_plant_data())
    clean_data = transform_data(raw_data)
    insert_to_database(clean_data)
