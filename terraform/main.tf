terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.15.0"
    }
  }
  backend "local" { path = var.tfstate_path }
}

provider "google" {
  credentials = file(var.credentials_file)
  project     = var.project
  region      = var.region
  zone        = var.zone
}
