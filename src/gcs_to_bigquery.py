import logging
import os
from datetime import datetime

import backoff
from google.cloud import bigquery, storage

from utilities.logger import logger as eng_logger
from utilities.pipeline_helpers import (
    filter_flat_files,
    randomly_fail,
    setup_full_refresh,
    setup_log_table,
)

#####


@backoff.on_exception(
    backoff.constant,
    RuntimeError,
    interval=1,
    max_tries=5,
    logger=eng_logger,
    backoff_log_level=logging.WARNING,
)
def load_gcs_to_bigquery(
    bucket_name: str,
    source_blob_name: str,
    dataset_name: str,
    table_name: str,
    bigquery_client: bigquery.Client,
    autodetect: bool = False,
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

    if randomly_fail():
        raise RuntimeError("Simulated transient error")

    # Define the GCS URI
    gcs_uri = f"gs://{bucket_name}/{source_blob_name}"

    # Define the BigQuery table reference
    table_ref = bigquery_client.dataset(dataset_name).table(table_name)

    # Configure the load job
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,  # Skip header row if present
        autodetect=autodetect,  # Let BigQuery auto-detect the schema
    )

    # Load data from GCS to BigQuery
    load_job = bigquery_client.load_table_from_uri(
        source_uris=[gcs_uri],
        destination=table_ref,
        job_config=job_config,
    )
    load_job.result()  # Wait for the job to complete

    if load_job.state == "DONE" and load_job.error_result is None:
        table_ref = bigquery_client.dataset(dataset_name).table("log")
        bigquery_client.insert_rows_json(
            table=table_ref,
            json_rows=[
                {
                    "blob_name": source_blob_name,
                    "uploaded_at": datetime.now().isoformat(),
                }
            ],
        )

    eng_logger.info(
        f"Job finished. Loaded {load_job.output_rows} rows into {dataset_name}.{table_name}"
    )


def run(
    bigquery_client: bigquery.Client,
    storage_client: storage.Client,
    bucket_name: str,
    prefix: str,
    destination_table_name: str,
    full_refresh: bool = False,
) -> None:

    dataset, table = destination_table_name.split(".")
    setup_log_table(
        bigquery_client=bigquery_client, dataset_name=dataset, full_refresh=full_refresh
    )

    # Get all the files in the bucket
    all_flat_files = [
        file.name
        for file in storage_client.list_blobs(bucket_or_name=bucket_name, prefix=prefix)
    ]
    filtered_flat_files = filter_flat_files(
        bigquery_client=bigquery_client,
        dataset=dataset,
        incoming_flat_files=all_flat_files,
    )

    if full_refresh:
        eng_logger.warning("Full refresh requested")
        setup_full_refresh(
            bigquery_client=bigquery_client,
            destination_table_name=destination_table_name,
        )

    # Loop through each file and load it into BigQuery
    # NOTE - We could also batch these into a larger load job!
    eng_logger.info(f"Beginning to process {len(filtered_flat_files)} files...")
    for flat_file in filtered_flat_files:
        eng_logger.info(f"Processing file {flat_file}...")
        load_gcs_to_bigquery(
            bucket_name=bucket_name,
            source_blob_name=flat_file,
            dataset_name=dataset,
            table_name=table,
            bigquery_client=bigquery_client,
            autodetect=True if full_refresh else False,
        )


#####

if __name__ == "__main__":
    # Instantiate the Google Cloud Storage client
    STORAGE_CLIENT = storage.Client()
    BIGQUERY_CLIENT = bigquery.Client()

    BUCKET_NAME = "csc-scratch"
    PREFIX = "nba_data/"
    DESTINATION_TABLE_NAME = "csc_main.nba_player_data"

    FULL_REFRESH = os.environ.get("FULL_REFRESH", "false").lower() == "true"

    # Load all the NBA player data into GCS
    run(
        storage_client=STORAGE_CLIENT,
        bigquery_client=BIGQUERY_CLIENT,
        bucket_name=BUCKET_NAME,
        prefix=PREFIX,
        destination_table_name=DESTINATION_TABLE_NAME,
        full_refresh=FULL_REFRESH,
    )
