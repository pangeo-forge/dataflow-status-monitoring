resource "google_storage_bucket" "function_bucket" {
  name     = "${var.project}-post-dataflow-status-function"
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

resource "google_cloudfunctions_function" "function" {
  name    = "post-dataflow-status"
  runtime = "python39"

  source_archive_bucket = google_storage_bucket.function_bucket.name
  source_archive_object = google_storage_bucket_object.zip.name

  # Must match the function name in the cloud function `main.py` source code
  entry_point = "post_status"

  event_trigger {
    event_type = "google.pubsub.topic.publish"
    resource   = resource.google_pubsub_topic.topic.id
  }
  environment_variables = {
    REPO_ORG = "${var.repo_org}"
    REPO     = "${var.repo}"
  }
  secret_environment_variables {
    key     = "PAT"
    secret  = "github_repository_dispatch_pat"
    version = "latest"
  }
}



