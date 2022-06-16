# dataflow-status-monitoring

GCP Resources to report the status of completed Dataflow jobs to a repository dispatch endpoint.

## Requirements
- Terraform
- A GCP project with the necessary services activated.

## Environment Settings
The Terraform environment variables can be configured with the us of a [.tfvars file](https://www.terraform.io/language/values/variables#variable-definitions-tfvars-files) with the following variables.
```
credentials_file = "<Your project service account credentials key file path>" 
project          = "<Your GCP project id>"
pat              = "<Your Github PAT with permissions for repository dispatch>"
repo_org         = "pangeo-forge"
repo             = "staged-recipes"
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
