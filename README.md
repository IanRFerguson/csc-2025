# Changemakers 2025 - Engineering Source Code

The setup here should be pretty minimal, as long as the cloud infrastructure has been provisioned in your GCP project (see `infra/`) you should be able to run `make reset` && `make pipeline` to stand up the data observability tables and run the pipeline in a Docker container.

## Extract + Load

The extract and load steps are defined in the `src/` directory. You can run each component separately if you want to (e.g., `make extract` `make load`), or run the whole pipeline with `make elt`.

| Source File       | Description                                                                   |
| ----------------- | ----------------------------------------------------------------------------- |
| `nba_to_gcs`      | This code reads raw HTML as a Pandas DataFrame and writes it to GCS           |
| `gcs_to_bigquery` | This code loads flat files from GCS into BigQuery tables                      |
| `constants`       | We're defining constant / static variables in this file to keep our code tidy |
| `reset_for_demo`  | This gets invoked when you run `make reset`                                   |


## Transformation with dbt
There's a full dbt Project in `csc_dbt/` that loads the raw data from the extract / load steps above and transforms it. See the [dbt README](./csc_dbt/README.md) for some basic commands and setup tips.

You can re-run the full analytical pipeline (which includes a dbt-python Machine Learning model) with `dbt run --exclude elementary --vars '{"RUN_ML_MODELS": true}'` (or skip the `--vars` argument to just run the static tables for analysis).

These commands are also wrapped for convenience in the [dbt Makefile](./csc_dbt/Makefile) - e.g., `make basic`, `make ml`

You'll find that Elementary pre- and post-hooks run on every dbt command. This writes metadata about your invocation to a set of monitoring tables in your warehouse - you can view these in a user-friendly UI with `make elementary`.

## Infrastructure as Code (IaC) with Terraform
You can run this pipeline yourself in your own project - just change the project name in `main.tf`, run `terraform init` and `terraform apply`.

See the [infrastructure README](./infra/README.md) for a more thorough breakdown of the required setup.