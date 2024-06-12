"""Script for loading the transformed plant data to the Microsoft SQL Server Database"""

from os import environ as ENV
from dotenv import load_dotenv
from pymssql import connect, Connection, exceptions


def get_connection() -> Connection:
    """Creates a connection to the database, returning a connection object."""

    try:
        return connect(
            server=ENV["DB_HOST"],
            port=ENV["DB_PORT"],
            user=ENV["DB_USER"],
            password=ENV["DB_PASSWORD"],
            database=ENV["DB_NAME"],
            as_dict=True,
        )
    except KeyError as e:
        raise KeyError(f"{e} missing from environment variables.") from e
    except exceptions.OperationalError as e:
        raise exceptions.OperationalError(
            f"Error connecting to database: {e}") from e


def insert_reading()


if __name__ == "__main__":

    load_dotenv()

    connection = get_connection()
    connection.close()
