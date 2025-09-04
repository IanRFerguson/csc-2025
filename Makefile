pipeline:
	@echo "Running the data pipeline..."
	@python src/nba_to_gcs.py
	@python src/gcs_to_bq.py