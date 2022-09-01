variable "project" {
  type = string
}

variable "credentials_file" {
  type = string
}

variable "apps_with_secrets" {
  type = map
}

variable "region" {
  type    = string
  default = "us-central1"
}

variable "zone" {
  type    = string
  default = "us-central1-c"
}
