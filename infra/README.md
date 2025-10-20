# Terraform Project

This is a pretty simple Terraform project. The core infra for our ELT pipeline is defined in `main.tf` and the state file is stored in Google Cloud Storage (defined in the `backend.tf` file).

## Setup
You can do all of the setup at the command line. You'll need a free Google Cloud project to get going here.

- Change the project name in `main.tf`
- Either update the storage bucket in `backend.tf` or remove it entirely
  - You should only remove it if you only plan on applying from one machine
- Authenticate in the terminal with `gcloud auth application-default login`
- Set the project with `gcloud config set project { YOUR PROJECT NAME }`
- Run `terraform init` to create the local state
- Run `terraform apply` to create the relevant cloud infrastructure