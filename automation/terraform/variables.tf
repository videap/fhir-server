############# Terraform Configuration Variables #############
terraform {
  required_version = "~> 1.4"

  backend "gcs" {
    bucket = "fhir-terraform-state"
  }

  required_providers {
    google = {
      source  = "registry.terraform.io/hashicorp/google"
      version = "~> 5"
    }
  }
}

provider "google" {
  project = var.project_id[terraform.workspace]
  region  = var.region
}

############# Google Project Variables #############

variable "region" { type = string }
variable "project_id" { type = map(string) }