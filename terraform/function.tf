resource "google_storage_bucket" "function_bucket" {
  name     = "${var.project}-github-app-post-dataflow-status-function"
  location = var.region
}

data "archive_file" "source" {
  type        = "zip"
  source_dir  = "../src"
  output_path = "/tmp/function.zip"
}

resource "google_storage_bucket_object" "zip" {
  source       = data.archive_file.source.output_path
  content_type = "application/zip"
  name         = "src-${data.archive_file.source.output_md5}.zip"
  bucket       = google_storage_bucket.function_bucket.name
}

locals {
  app_names = [var.app_name]
}

resource "google_cloudfunctions_function" "function" {
  for_each = {
    for app in local.app_names : "github-app-post-dataflow-status-${app}" => "github_app_webook_secret-${app}"
  }
  name = each.key
  runtime = "python39"

  source_archive_bucket = google_storage_bucket.function_bucket.name
  source_archive_object = google_storage_bucket_object.zip.name

  # Must match the function name in the cloud function `main.py` source code
  entry_point = "post_status"

  event_trigger {
    event_type = "google.pubsub.topic.publish"
    resource   = resource.google_pubsub_topic.topic.id
  }
  labels                = {}
  environment_variables = {}
  secret_environment_variables {
    key     = "WEBHOOK_SECRET"
    secret  = each.value
    version = 1
  }
}
