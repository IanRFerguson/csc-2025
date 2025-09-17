# Run the ELT pipeline in Docker
pipeline:
	@docker compose up --build

reset:
	@echo "Resetting the data pipeline..."
	@python src/reset_for_demo.py


# Runs the individual ELT steps
# NOTE - This is the Docker command executed in `make pipeline`
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
	@cd csc_dbt && dbt build