'''This file is used to move old data from the database into a long-term storage system'''

import os
from os import environ as ENV
from datetime import datetime
import csv
from dotenv import load_dotenv
from pymssql import connect, Connection, exceptions
from boto3 import client
import pytz

TABLES_IN_DATABASE = [
    'town',
    'country',
    'timezone',
    'location',
    'botanist',
    'plant',
    'reading'
]
METADATA_FOLDER = "metadata/"
READING_FOLDER = "readings/"
BUCKET_NAME = "c11-kappa-group-s3-bucket"


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
        return None


def delete_all_reading_data_from_rds(conn: Connection) -> None:
    '''Deletes all reading data from the rds database'''
    query = '''
DELETE FROM delta.reading
'''
    with conn.cursor() as cur:
        cur.execute(query)
        conn.commit()


def load_into_csv(data: list[dict], filename: str) -> None:
    '''Creates a csv file inside a folder named after today's date'''

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


def get_uk_time() -> str:
    '''Gets uk timezone as a string'''
    uk_timezone = pytz.timezone('Europe/London')
    return datetime.now(uk_timezone).strftime("%d_%m_%Y")


def upload_file_to_bucket(s3_client: client,
                          filename: str,
                          bucket_name: str,
                          object_name: str) -> None:
    '''Uploads a file to the bucket.'''
    try:
        s3_client.upload_file(filename, bucket_name, object_name)
        print(f"File {filename} uploaded to {bucket_name}/{object_name}")
    except Exception as e:
        print(f"Error uploading file: {e}")


def upload_data_to_s3(s3_client: client, conn: Connection, curr_time: str) -> list[dict]:
    '''Uploads all metadata folder to s3 bucket'''

    for table in TABLES_IN_DATABASE:
        filename = f"{curr_time}/{table}_data.csv"
        table_data = get_data_from_rds(conn, table)
        if table_data:
            load_into_csv(table_data, filename)
        else:
            print("No table data for ", table)
            continue

        if table != 'reading':
            upload_file_to_bucket(s3_client, filename, BUCKET_NAME,
                                  METADATA_FOLDER+filename)
        else:
            upload_file_to_bucket(s3_client, filename, BUCKET_NAME,
                                  READING_FOLDER+filename)


def create_today_folder(folder_name: str) -> None:
    '''Creates a directory for today's data'''
    os.makedirs(folder_name, exist_ok=True)


if __name__ == "__main__":
    load_dotenv()
    current_date = get_uk_time()
    db_conn = get_connection()
    s3_clt = load_s3_client()
    create_today_folder(current_date)
    upload_data_to_s3(s3_clt, db_conn, current_date)

    # delete_all_reading_data_from_rds(conn)
