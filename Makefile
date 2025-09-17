elt:
	@echo "Running the data pipeline..."
	
	@echo ""
	@echo "** Step 1: Fetching NBA data and uploading to GCS **"
	@python src/nba_to_gcs.py
	
	@echo ""
	@echo "** Step 2: Loading data from GCS to BigQuery **"
	@python src/gcs_to_bigquery.py

	@echo ""
	@echo "** Step 3: Transforming data in BigQuery using dbt **"
	@cd csc_dbt && dbt build

pipeline:
	@docker compose up --build