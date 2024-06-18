module "scheduler_service_account" {
    source = "github.com/nanoclinic/foundation//terraform/modules/service_accounts?ref=service_accounts-1.2.0"

    service_account_name = "fhir-sa"
    description          = "fhir app service account"
    roles                = []
    project_ids          = [local.project_id]

    workload_identity    = {
        enable = true
        namespace = "foundation"
        cluster_sa = "fhir-sa"
    }

    secrets_with_permissions = [
        "fhir_rabbitmq_user",
        "fhir_rabbitmq_password",
    ]
}