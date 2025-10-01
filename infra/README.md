# Terraform Project

This is a pretty simple Terraform project. The core infra for our ELT pipeline is defined in `main.tf` and the state file is stored in Google Cloud Storage (defined in the `backend.tf` file).

As long as you're authenticated and have editor access on your target project (e.g., `gcloud auth application-default login` and `gcloud config set project { TARGET PROJECT }`), you can spin up all the relevant infrastructure with `terraform apply`.