import random

from google.cloud import bigquery
from sqlalchemy import func

from utilities.logger import logger as eng_logger


def setup_full_refresh(
    bigquery_client: bigquery.Client,
    destination_table_name: str,
) -> None:
    """
    Placeholder function for any setup needed for a full refresh.
    Currently, no specific setup is required.
    """

    # Delete the existing table data
    dataset, table = destination_table_name.split(".")
    table_ref = bigquery_client.dataset(dataset).table(table)

    bigquery_client.delete_table(table_ref, not_found_ok=True)

    eng_logger.warning(f"Deleted table {destination_table_name}.")


def randomly_fail():
    """
    Randomly raise a RuntimeError to simulate transient failures.
    """

    if random.random() < 0.25:  # 25% chance to fail
        raise RuntimeError("Simulated transient error")


def setup_log_table(
    bigquery_client: bigquery.Client, dataset_name: str, full_refresh: bool = False
) -> None:
    """
    Ensure the log table exists in the specified dataset.
    """

    table_ref = bigquery_client.dataset(dataset_name).table("log")
    schema = [
        bigquery.SchemaField("blob_name", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("uploaded_at", "TIMESTAMP", mode="REQUIRED"),
    ]
    table = bigquery.Table(table_ref, schema=schema)

    if full_refresh:
        eng_logger.warning("Full refresh requested - resetting log table")
        bigquery_client.delete_table(table_ref, not_found_ok=True)

    try:
        bigquery_client.get_table(table_ref)
        eng_logger.debug(f"Log table {dataset_name}.log already exists")
    except Exception:
        bigquery_client.create_table(table)
        eng_logger.info(f"Created log table {dataset_name}.log...")


def filter_flat_files(
    bigquery_client: bigquery.Client,
    dataset: str,
    incoming_flat_files: list[str],
    log_table: str = "log",
) -> list[str]:
    """
    Filter the incoming flat files to only include those that are not already loaded
    into BigQuery.

    Args:
        bigquery_client (bigquery.Client): The BigQuery client.
        dataset (str): The dataset name.
        incoming_flat_files (list[str]): The list of incoming flat file names.

    Returns:
        list[str]: The filtered list of flat file names.
    """

    eng_logger.debug(
        f"Filtering {len(incoming_flat_files)} incoming flat files against log table..."
    )

    log_table_values = bigquery_client.query(
        f"SELECT blob_name FROM `{dataset}.{log_table}`"
    ).result()
    existing_files = [row["blob_name"] for row in log_table_values]

    filtered_files = [
        file for file in incoming_flat_files if file not in existing_files
    ]

    return filtered_files
