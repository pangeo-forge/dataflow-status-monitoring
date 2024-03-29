# dataflow-status-monitoring

GCP Resources to report the status of completed Dataflow jobs to a repository dispatch endpoint.

## Requirements
- Terraform
- A GCP Service Account with project OWNER role + a key file generated for this service account.
- A GCP project with the necessary services activated. These include:
  - Cloud Function API
  - Cloud Build API
  - Cloud Pub/Sub API
  - Cloud Logging API
  - Secret Manager API


## Environment Settings
The Terraform environment variables can be configured with the us of a [.tfvars file](https://www.terraform.io/language/values/variables#variable-definitions-tfvars-files) with the following variables.
```
credentials_file  = "<Your service account credentials key file path>"
project           = "<Your GCP project id>"
apps_with_secrets = "<JSON mapping of app instance names to their corresponding webhook secrets>"
```

## Deploying the resources
```
$ cd terraform
$ terraform init
$ terraform plan -out tfplan -var-file=your.tfvars
$ terraform apply tfplan
```

## Development

### Requirements
- Python>=3.9
- tox

### Tests and Linting
```
$ tox
```
