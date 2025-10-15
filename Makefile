# Run the ELT pipeline in Docker
pipeline:
	@docker compose up --build

# Runs the individual ELT steps
# NOTE - This is the Docker command executed in `make pipeline`
# See devops/Dockerfile for more details
elt:
	@echo "Running the data pipeline..."
	
	@echo ""
	@echo "** Step 1: Fetching NBA data and uploading to GCS **"
	@make extract
	
	@echo ""
	@echo "** Step 2: Loading data from GCS to BigQuery **"
	@make load

	@echo ""
	@echo "** Step 3: Transforming data in BigQuery using dbt **"
	@make transform

# Individual ELT steps
extract:
	@python src/nba_to_gcs.py

load:
	@python src/gcs_to_bigquery.py

transform:
	@cd csc_dbt && dbt build --exclude elementary


### Utilities

# Reset BigQuery and Cloud Storage to a known state for demos
# Also runs Elementary models for on-end hooks to work
reset:
	@echo "Resetting the data pipeline..."
	@python src/demo_setup/reset_for_demo.py
	@echo "Making Elementary models to avoid errors later..."
	@cd csc_dbt && dbt run -s elementary --vars "{'RUN_ML_MODELS': 'true', 'disable_dbt_artifacts_autoupload': 'false'}"
	@rm -rf csc_dbt/target


# Backup the Cloud Storage files to an isolated prefix
# This is useful if we run into rate limits during the demo
backup:
	@echo "Backing up the data pipeline..."
	@python src/demo_setup/backup_for_demo.py


# Run formatting checks
ruff:
	@ruff check --fix .
	@ruff format .