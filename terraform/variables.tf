variable "project" {
  type = string
}

variable "credentials_file" {
  type = string
}

variable "apps_with_secrets" {
  type = map
  sensitive = true
}

variable "function_src_dir" {
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
