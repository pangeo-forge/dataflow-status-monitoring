variable "project" {
  type = string
}

variable "credentials_file" {
  type = string
}

variable "app_name" {
  type = string
}

variable "webhook_secret" {
  type = string
}

variable "region" {
  type    = string
  default = "us-central1"
}

variable "zone" {
  type    = string
  default = "us-central1-c"
}
