# We can use this command to build the Elementary report - it writes out to
# ./edr_target/ by default
elementary:
	@export GOOGLE_APPLICATION_CREDENTIALS=$(realpath ../service_accounts/tmc-changemakers-2025-a5d74b23cad8.json) && \
		edr report -p .

# This is a simple dbt command to run our whole project
basic:
	@unset RUN_ML_MODELS && \
		dbt build --exclude elementary --full-refresh


# Build applicable models incrementally
incremental:
	@unset RUN_ML_MODELS && \
		dbt build --exclude elementary


# Run our ML models
ml:
	@dbt build --exclude elementary --vars "{'RUN_ML_MODELS': true}"