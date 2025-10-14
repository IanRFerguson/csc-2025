from google.cloud import storage
from constants import BACKUP_PREFIX, BUCKET_NAME, PREFIX
from utilities.logger import logger as eng_logger

#####

if __name__ == "__main__":
    # Initialize clients
    STORAGE_CLIENT = storage.Client()

    # Copy all objects in the bucket
    bucket = STORAGE_CLIENT.bucket(BUCKET_NAME)
    blobs = bucket.list_blobs(prefix=PREFIX)
    for blob in blobs:
        # Define the new blob name by replacing the prefix
        new_blob_name = blob.name.replace(PREFIX, BACKUP_PREFIX, 1)
        new_blob = bucket.blob(new_blob_name)

        # Copy the blob to the new location
        new_blob.rewrite(blob)
        eng_logger.info(f"Copied {blob.name} to {new_blob_name} in {BUCKET_NAME}")
