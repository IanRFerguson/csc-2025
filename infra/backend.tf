terraform {
  backend "gcs" {
    bucket = "ian-dev"
    prefix = "terraform/state/csc-2025/admin"
  }
}
