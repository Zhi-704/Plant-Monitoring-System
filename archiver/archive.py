'''This file is used to move old data from the database into a long-term storage system'''

from datetime import datetime
import csv
from os import environ as ENV
from dotenv import load_dotenv
from pymssql import connect, Connection, exceptions
from boto3 import client
import pytz

TABLES_IN_DATABASE = ['reading',
                      'town',
                      'country',
                      'timezone',
                      'location',
                      'botanist',
                      'plant'
                      ]


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


def load_s3_client() -> client:
    '''Creates client that manipulates s3 bucket'''
    return client('s3',
                  aws_access_key_id=ENV["ACCESS_KEY"],
                  aws_secret_access_key=ENV["SECRET_ACCESS_KEY"]
                  )


def get_data_from_rds(conn: Connection, table_name: str) -> list[dict]:
    '''Queries all reading data from the rds database'''

    query = f'''
SELECT * FROM delta.{table_name}
'''
    try:
        with conn.cursor() as cur:
            cur.execute(query)
            data = cur.fetchall()

        return data
    except exceptions.ProgrammingError as e:
        print("An error has occurred: ", e)
        conn.rollback()


def delete_all_reading_data_from_rds(conn: Connection) -> None:
    '''Deletes all reading data from the rds database'''
    query = '''
DELETE FROM delta.reading
'''
    with conn.cursor() as cur:
        cur.execute(query)
        conn.commit()


def load_into_csv(data: list[dict], filename: str) -> None:
    if not data:
        print(f"The data list is empty. No CSV file was created for {
              filename}.")
        return

    headers = data[0].keys()

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.DictWriter(csvfile, fieldnames=headers)

        csvwriter.writeheader()

        for row in data:
            csvwriter.writerow(row)

    print(f"File {filename} successfully created!")
    return


def get_uk_time() -> str:
    uk_timezone = pytz.timezone('Europe/London')
    return datetime.now(uk_timezone).strftime("%H_%M_%S-%d_%m_%Y")


def upload_file_to_bucket(s3_clt: client, filename: str, bucket_name: str, object_name: str) -> None:
    '''Write a file to bucket.'''
    try:
        s3_clt.upload_file(filename, bucket_name, object_name)
        print(f"File {filename} uploaded to {bucket_name}/{object_name}")
    except Exception as e:
        print(f"Error uploading file: {e}")


def get_metadata(conn: Connection) -> list[dict]:

    pass


if __name__ == "__main__":
    load_dotenv()
    current_time = get_uk_time()
    conn = get_connection()

    reading_data = get_data_from_rds(conn, 'reading')
    town_data = get_data_from_rds(conn, 'town')
    # timezone_data = get_data_from_rds(conn, 'timezone')
    # country_data = get_data_from_rds(conn, 'country')
    # location_data = get_data_from_rds(conn, 'location')
    # botanist_data = get_data_from_rds(conn, 'botanist')
    # plant_data = get_data_from_rds(conn, 'plant')

    load_into_csv(reading_data, f'reading_at_{current_time}.csv')
    load_into_csv(town_data, f'town_at_{current_time}.csv')
    # load_into_csv(timezone_data, f'timezone_at_{current_time}.csv')
    # load_into_csv(country_data, f'country_at_{current_time}.csv')
    # load_into_csv(location_data, f'location_at_{current_time}.csv')
    # load_into_csv(botanist_data, f'botanist_at_{current_time}.csv')
    # load_into_csv(plant_data, f'plant_at_{current_time}.csv')

    # delete_all_reading_data_from_rds(conn)

    s3_client = load_s3_client()
    upload_file_to_bucket(s3_client, f'reading_at_{
                          current_time}.csv', 'c11-kappa-group-s3-bucket', 'reading_data.csv')
