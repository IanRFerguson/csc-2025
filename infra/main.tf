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


// Key for the development service account
resource "google_service_account_key" "csc_service_account_key" {
  service_account_id = google_service_account.csc_service_account.name
  public_key_type    = "TYPE_X509_PEM_FILE"
  private_key_type   = "TYPE_GOOGLE_CREDENTIALS_FILE"
}


// Grant jobUser and dataEditor roles to the service account on the dataset
resource "google_project_iam_member" "csc_service_account_roles" {
  for_each = toset([
    "roles/bigquery.dataEditor",
    "roles/bigquery.jobUser",
    "roles/storage.objectAdmin",
  ])
  project = "tmc-changemakers-2025"
  role    = each.value
  member  = "serviceAccount:${google_service_account.csc_service_account.email}"
}

output "service_account_key_json" {
  value     = google_service_account_key.csc_service_account_key.private_key
  sensitive = true
}

resource "local_file" "service_account_key" {
  content = jsonencode({
    type                        = "service_account"
    project_id                  = google_service_account.csc_service_account.project
    private_key_id              = google_service_account_key.csc_service_account_key.id
    private_key                 = google_service_account_key.csc_service_account_key.private_key
    client_email                = google_service_account.csc_service_account.email
    client_id                   = google_service_account.csc_service_account.unique_id
    auth_uri                    = "https://accounts.google.com/o/oauth2/auth"
    token_uri                   = "https://oauth2.googleapis.com/token"
    auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
    client_x509_cert_url        = "https://www.googleapis.com/robot/v1/metadata/x509/${google_service_account.csc_service_account.email}"
  })
  filename = "${path.module}/../service_accounts/csc_service_account_key.json"
}
