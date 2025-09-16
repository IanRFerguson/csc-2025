import os
import tempfile
from datetime import datetime

import pandas as pd
from google.cloud import storage
from redis import Redis
from rq import Queue
from sqlalchemy import func

#####

TEAM_INITIALS = ["MIL", "ATL", "NYK"]
YEARS = range(2020, 2026)
QUEUE = Queue("nba_to_gcs", connection=Redis())


def get_data_from_nba_reference(year: int, team_initials: str) -> pd.DataFrame:
    """
    Fetch NBA player statistics from Basketball Reference.

    Args:
        year (int): The NBA season year.
        team_initials (str): The three-letter team abbreviation.

    Returns:
        pd.DataFrame: A DataFrame containing the player statistics.
    """

    url = (
        "https://www.basketball-reference.com/teams/{team_initials}/{year}.html".format(
            team_initials=team_initials, year=year
        )
    )

    try:
        scoring_table = pd.read_html(url)[1]

        # Add ELT metadata
        scoring_table["year"] = year
        scoring_table["team_initials"] = team_initials
        scoring_table["_load_timestamp"] = pd.Timestamp(datetime.now())

    except Exception as e:
        print(f"Error occurred: {e}")
        return pd.DataFrame()

    return scoring_table


def write_table_to_gcs(
    df: pd.DataFrame,
    bucket_name: str,
    destination_blob_name: str,
    storage_client: storage.Client,
) -> None:
    """
    Writes a DataFrame to a CSV file in Google Cloud Storage.

    Args:
        df (pd.DataFrame): The DataFrame to write.
        bucket_name (str): The name of the GCS bucket.
        destination_blob_name (str): The destination path in the GCS bucket.
        storage_client (storage.Client): An instance of the Google Cloud Storage client.
    """

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # Convert DataFrame to CSV and upload to GCS
    with tempfile.NamedTemporaryFile() as temp_file:
        df.to_csv(temp_file.name, index=False)
        blob.upload_from_filename(temp_file.name, content_type="text/csv")

    print(f"File uploaded to {destination_blob_name} in bucket {bucket_name}.")


def process_single_team(team: str, storage_client: storage.Client) -> None:
    """
    Writes one CSV per year to Google Cloud Storage for the given team
    """

    for year in YEARS:
        df = get_data_from_nba_reference(year, team)
        if not df.empty:
            write_table_to_gcs(
                df=df,
                bucket_name="csc-scratch",
                destination_blob_name=f"nba_data/{team}/{year}.csv",
                storage_client=storage_client,
            )


def run(storage_client: storage.Client) -> None:
    """
    Imports team data for all 30 teams in parallel
    """

    for team in TEAM_INITIALS:
        _ = QUEUE.enqueue(process_single_team, team=team, storage_client=storage_client)


#####

if __name__ == "__main__":
    # Instantiate the Google Cloud Storage client
    storage_client = storage.Client()

    # Load all the NBA player data into GCS
    run(storage_client=storage_client)
