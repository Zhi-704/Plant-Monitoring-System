from os import environ as ENV
import os
import pandas as pd
from pymssql import connect, Connection, exceptions  # pylint: disable=no-name-in-module
from dotenv import load_dotenv
import boto3
import botocore.exceptions

load_dotenv()

AWS_ACCESS_KEY = ENV.get("ACCESS_KEY")
AWS_SECRET_ACCESS_KEY = ENV.get("SECRET_ACCESS_KEY")
source_bucket = ENV.get("BUCKET_NAME")
destination_path = "./data"


def create_s3_client(access_key: str, secret_access_key: str) -> boto3.client:
    """Creates and returns an S3 client using an AWS Access Key."""
    try:
        return boto3.client(
            "s3",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_access_key
        )
    except botocore.exceptions.ClientError as e:
        raise RuntimeError(f"Error creating S3 client: {e}") from e


def get_bucket_file_info(s3_client: boto3.client, source_bucket: str) -> dict:
    """
    Retrieves information on the files in an s3 bucket.
    """
    try:
        return s3_client.list_objects_v2(Bucket=source_bucket)
    except botocore.exceptions.ClientError as e:
        raise RuntimeError(
            f"Error retrieving files from the S3 bucket: {e}") from e


def download_archived_data(bucket_file_info: dict, s3_client: boto3.client, source_bucket: str) -> None:
    """Downloads all the archived reading data and metadata from the S3 Bucket."""

    for file in bucket_file_info.get("Contents", []):

        filename_and_folder = file.get("Key", "")
        filename = filename_and_folder.split("/")[-1]

        if not filename:
            continue

        if filename_and_folder.startswith("metadata/"):
            s3_client.download_file(source_bucket, filename_and_folder, f"{
                                    destination_path}/{filename}")

        if filename_and_folder.startswith("readings/"):
            date = filename_and_folder.split("/")[1]
            s3_client.download_file(source_bucket, filename_and_folder, f"{
                                    destination_path}/{date}-{filename}")


def merge_reading_files() -> pd.DataFrame:
    """Merges the reading CSVs into a single DataFrame."""

    reading_dfs = []

    for filename in os.listdir(destination_path):
        if filename.endswith("reading_data.csv"):
            file_path = os.path.join(destination_path, filename)
            df = pd.read_csv(file_path)
            reading_dfs.append(df)

    joined_reading_dfs = pd.concat(reading_dfs, ignore_index=True)
    return joined_reading_dfs


def merge_metadata_with_reading(readings: pd.DataFrame) -> pd.DataFrame:
    """Merges metadata CSVs with the reading DataFrame."""

    country_df = pd.read_csv(f'{destination_path}/country_data.csv')
    timezone_df = pd.read_csv(f'{destination_path}/timezone_data.csv')
    town_df = pd.read_csv(f'{destination_path}/town_data.csv')
    botanist_df = pd.read_csv(f'{destination_path}/botanist_data.csv')
    location_df = pd.read_csv(f'{destination_path}/location_data.csv')
    plant_df = pd.read_csv(f'{destination_path}/plant_data.csv')

    merged_df = pd.merge(readings, plant_df, on='plant_id', how='left')
    merged_df = pd.merge(merged_df, location_df, on='location_id', how='left')
    merged_df = pd.merge(merged_df, town_df, on='town_id', how='left')
    merged_df = pd.merge(merged_df, timezone_df, on='timezone_id', how='left')
    merged_df = pd.merge(merged_df, country_df, on='country_id', how='left')
    merged_df = pd.merge(merged_df, botanist_df, on='botanist_id', how='left')

    merged_df.drop(['location_id', 'town_id', 'plant_id',
                   'timezone_id', 'country_id', 'botanist_id', 'reading_id'], inplace=True, axis=1)

    return merged_df


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


def get_live_data(connection: Connection) -> pd.DataFrame:
    """Retrieves plant data from the database, returning it as
        a Pandas DataFrame."""

    print("Fetching live data...")

    try:
        with connection.cursor() as cursor:

            query = """
                    SELECT *
                    FROM delta.country AS c
                    JOIN delta.town AS t ON c.country_id = t.country_id
                    JOIN delta.timezone AS tz ON t.timezone_id = tz.timezone_id
                    JOIN delta.location AS l ON t.town_id = l.town_id
                    JOIN delta.plant AS p ON l.location_id = p.location_id
                    JOIN delta.reading AS r ON p.plant_id = r.plant_id
                    JOIN delta.botanist AS b ON r.botanist_id = b.botanist_id
                    """
            cursor.execute(query)
            data = cursor.fetchall()

        if not data:
            raise ValueError("No reading data found in the database")

        reading_data = pd.DataFrame(data)

        reading_data.drop(['location_id', 'town_id', 'plant_id',
                           'timezone_id', 'country_id', 'botanist_id', 'reading_id'], inplace=True, axis=1)
        return reading_data
    except Exception as e:
        raise Exception(f"Error: {e}") from e
    finally:
        connection.close()


def get_archived_data(aws_access_key: str, aws_secret_access_key: str) -> pd.DataFrame:
    """Downloads the archived data files from S3 bucket, merges them, and returns
        as a Pandas DataFrame."""

    print("Fetching and processing archived data...")

    s3 = create_s3_client(aws_access_key, aws_secret_access_key)
    bucket_file_info = get_bucket_file_info(s3, source_bucket)

    download_archived_data(bucket_file_info, s3, source_bucket)
    reading_data = merge_reading_files()
    return merge_metadata_with_reading(reading_data)
