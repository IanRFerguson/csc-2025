import os

import backoff
from google.cloud import bigquery, storage
from google.cloud.exceptions import NotFound
from redis import Redis
from rq import Connection, Queue, Worker
from typing import List

#####

QUEUE = Queue("gcs_to_bigquery", connection=Redis())


def load_gcs_to_bigquery(
    bucket_name: str,
    source_blob_name: str,
    destination_table_name: str,
    bigquery_client: bigquery.Client,
) -> None:
    """
    Load data from GCS to BigQuery.

    Args:
        bucket_name (str): Name of the GCS bucket.
        source_blob_name (str): Name of the source blob in GCS.
        dataset_id (str): BigQuery dataset ID.
        table_id (str): BigQuery table ID.
        bigquery_client (bigquery.Client): Initialized BigQuery client.
    """

    # Define the GCS URI
    gcs_uri = f"gs://{bucket_name}/{source_blob_name}"

    # Define the BigQuery table reference
    dataset, table = destination_table_name.split(".")
    table_ref = bigquery_client.dataset(dataset).table(table)

    # Configure the load job
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,  # Skip header row if present
        autodetect=True,  # Let BigQuery auto-detect the schema
    )

    # Load data from GCS to BigQuery
    load_job = bigquery_client.load_table_from_uri(
        source_uris=[gcs_uri],
        destination=table_ref,
        job_config=job_config,
    )
    load_job.result()  # Wait for the job to complete

    print(
        f"Job finished. Loaded {load_job.output_rows} rows into {destination_table_name}"
    )


def filter_flat_files(
    bigquery_client: bigquery.Client,
    all_flat_files: List[str],
    log_table_name: str = "csc_main.log",
) -> List[str]:
    """
    Compare all files in the GCS bucket with the files we've already
    loaded to BigQuery

    Args:
        bigquery_client (bigquery.Client): An instance of the BigQuery client.
        all_flat_files (List[str]): A list of all files in the GCS bucket.
        log_table_name (str): The name of the BigQuery table that logs loaded files.

    Returns:
        List[str]: A list of files that have not yet been loaded to BigQuery.
    """

    try:
        query = f"SELECT * FROM `{log_table_name}`"
        table_values = bigquery_client.query(query)
        loaded_files = [row["blob_name"] for row in table_values]
    except NotFound:
        loaded_files = []

    return [file for file in all_flat_files if file not in loaded_files]


def run(
    bigquery_client: bigquery.Client,
    storage_client: storage.Client,
    bucket_name: str,
    destination_table_name: str,
) -> None:

    # Get all the files in the bucket
    all_flat_files = [
        file.name for file in storage_client.list_blobs(bucket_or_name=bucket_name)
    ]

    filtered_flat_files = filter_flat_files(
        bigquery_client=bigquery_client, all_flat_files=all_flat_files
    )

    # Queue up a GCS-to-BigQuery load per new file
    # NOTE - We could also batch these into a larger load job!
    for flat_file in filtered_flat_files:
        _ = QUEUE.enqueue(
            load_gcs_to_bigquery,
            bucket_name=bucket_name,
            source_blob_name=flat_file,
            destination_table_name=destination_table_name,
            bigquery_client=bigquery_client,
        )


#####

if __name__ == "__main__":
    # Instantiate the Google Cloud Storage client
    storage_client = storage.Client()
    bigquery_client = bigquery.Client()

    bucket_name = "csc-scratch"
    destination_table_name = "csc_main.nba_player_data"

    # Load all the NBA player data into GCS
    run(
        storage_client=storage_client,
        bigquery_client=bigquery_client,
        bucket_name=bucket_name,
        destination_table_name=destination_table_name,
    )
