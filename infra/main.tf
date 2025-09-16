terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "6.9.0"
    }
  }
}

provider "google" {
  project = "tmc-changemakers-2025"
}


// Main dataset in the project
resource "google_bigquery_dataset" "csc_main" {
  dataset_id    = "csc_main"
  friendly_name = "CSC Main Dataset"
  description   = "Raw layer in our mock dbt project"
  location      = "US"
}

resource "google_bigquery_dataset" "csc_scratch" {
  dataset_id                  = "csc_scratch"
  friendly_name               = "CSC Scratch Dataset"
  description                 = "Scratch layer in our mock dbt project"
  location                    = "US"
  default_table_expiration_ms = 86400000 // 1 day
}

resource "google_storage_bucket" "csc_gcs_bucket" {
  name     = "csc-scratch"
  location = "US"

  uniform_bucket_level_access = true

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 60
    }
  }
}


// Service account for development purposes
resource "google_service_account" "csc_service_account" {
  account_id   = "csc-dev"
  display_name = "CSC 2025 Development Service Account"
  description  = "Service account for CSC 2025 development"
  project      = "tmc-changemakers-2025"
}


resource "google_project_iam_member" "csc_service_account_roles" {
  for_each = toset([
    "roles/bigquery.dataEditor",
    "roles/bigquery.jobUser",
    "roles/storage.admin",
  ])
  project = "tmc-changemakers-2025"
  role    = each.value
  member  = "serviceAccount:${google_service_account.csc_service_account.email}"
}

