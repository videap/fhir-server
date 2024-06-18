locals {
  env        = terraform.workspace
  project_id = var.project_id[terraform.workspace]
}