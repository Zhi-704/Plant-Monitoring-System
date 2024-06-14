'''This file is used to move old data from the database into a long-term storage system'''

import os
from os import environ as ENV
from datetime import datetime
import csv
import json
import logging

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
        logging.error("An error has occurred: %s", e)
        conn.rollback()
        return None


def delete_all_reading_data_from_rds(conn: Connection) -> None:
    '''Deletes all reading data from the rds database'''
    query = '''
DELETE FROM delta.reading
'''
    try:
        with conn.cursor() as cur:
            cur.execute(query)
            conn.commit()
    except exceptions.ProgrammingError as e:
        logging.error("An error has occurred: %s", e)
        conn.rollback()

    logging.info("All reading data deleted!")


def load_into_csv(data: list[dict], filename: str) -> None:
    '''Creates a csv file inside a folder named after today's date'''

    if not data:
        error_message = f"The data list is empty. No CSV file was created for {
            filename}."
        logging.error(error_message)
        return
    if not isinstance(data, list):
        return
    if not isinstance(data[0], dict):
        return

    headers = data[0].keys()

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.DictWriter(csvfile, fieldnames=headers)

        csvwriter.writeheader()

        for row in data:
            csvwriter.writerow(row)

    logging.info("File %s successfully created!", filename)


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
        log_message = f"File {filename} uploaded to {
            bucket_name}/{object_name}"
        logging.info(log_message)
    except Exception as e:
        error_message = f"Error uploading file: {e}"
        logging.error(error_message)


def upload_data_to_s3(s3_client: client,
                      conn: Connection,
                      folder_path: str,
                      curr_time: str) -> list[dict]:
    '''Uploads all metadata folder to s3 bucket'''

    for table in TABLES_IN_DATABASE:
        local_filename = f"{folder_path}/{table}_data.csv"
        if table == 'reading':
            remote_filename = f"{curr_time}/{table}_data.csv"
        else:
            remote_filename = f"{table}_data.csv"
        table_data = get_data_from_rds(conn, table)
        if isinstance(table_data, list) and len(table_data) >= 1:
            load_into_csv(table_data, local_filename)
        else:
            logging.info("No table data for %s", table)
            continue

        if table != 'reading':
            upload_file_to_bucket(s3_client, local_filename, ENV["BUCKET_NAME"],
                                  METADATA_FOLDER+remote_filename)
        else:
            upload_file_to_bucket(s3_client, local_filename, ENV["BUCKET_NAME"],
                                  READING_FOLDER+remote_filename)


def create_today_folder(folder_name: str) -> str:
    '''Creates a directory for today's data'''
    folder_name = os.path.join('tmp', folder_name)
    os.makedirs(folder_name, exist_ok=True)
    return folder_name


def lambda_handler(event, context):
    '''Function that runs when ran as a lambda function'''
    logging.basicConfig(level=logging.INFO)
    logging.info("Lambda function has started")
    load_dotenv()
    current_date = get_uk_time()
    db_conn = get_connection()
    s3_clt = load_s3_client()
    folder_path = create_today_folder(current_date)
    upload_data_to_s3(s3_clt, db_conn, folder_path, current_date)
    delete_all_reading_data_from_rds(db_conn)

    logging.info("Lambda function has finished")

    return {
        'statusCode': 200,
        'body': json.dumps('Process completed successfully!')
    }
