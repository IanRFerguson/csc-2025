import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from google.cloud import bigquery, storage

from src.constants import BUCKET_NAME, DESTINATION_DATASET_NAME, PREFIX
from src.utilities.logger import logger as eng_logger

#####

if __name__ == "__main__":
    # Initialize clients
    STORAGE_CLIENT = storage.Client()
    BIGQUERY_CLIENT = bigquery.Client()

    # Delete all objects in the bucket
    bucket = STORAGE_CLIENT.bucket(BUCKET_NAME)
    blobs = bucket.list_blobs(prefix=PREFIX)
    for blob in blobs:
        blob.delete()
        eng_logger.info(f"Deleted {blob.name} from {BUCKET_NAME}")

    # Drop the dbt datasets in BigQuery
    datasets = BIGQUERY_CLIENT.list_datasets()
    for dataset in datasets:
        if "dbt" in dataset.dataset_id:
            BIGQUERY_CLIENT.delete_dataset(dataset.dataset_id, delete_contents=True)
            eng_logger.info(f"Deleted dataset {dataset.dataset_id} from BigQuery")

    # Delete the tables in main
    dataset_ref = BIGQUERY_CLIENT.dataset(DESTINATION_DATASET_NAME)
    tables = BIGQUERY_CLIENT.list_tables(dataset_ref)
    for table in tables:
        BIGQUERY_CLIENT.delete_table(f"{DESTINATION_DATASET_NAME}.{table.table_id}")
        eng_logger.info(f"Deleted table {table.table_id} from BigQuery")
