from google.cloud import storage, bigquery
import os

#####


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

    # Loop through each file and load it into BigQuery
    # NOTE - We could also batch these into a larger load job!
    for flat_file in all_flat_files:
        print(f"Processing file {flat_file}...")
        load_gcs_to_bigquery(
            bucket_name=bucket_name,
            source_blob_name=flat_file,
            destination_table_name=destination_table_name,
            bigquery_client=bigquery_client,
        )


#####

if __name__ == "__main__":
    # Set the JSON file path for the service account key
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(
        os.path.dirname(__file__), "../service_accounts/use-me.json"
    )

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
