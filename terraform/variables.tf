variable "project" {
  type = string
}

variable "credentials_file" {
  type = string
}

variable "pat" {
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

variable "repo_org" {
  type = string
}

variable "repo" {
  type = string
}
