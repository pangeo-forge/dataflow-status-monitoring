resource "google_secret_manager_secret" "secret-basic" {
  secret_id = "github_app_webook_secret-${var.app_name}"

  replication {
    user_managed {
      replicas {
        location = var.region
      }
    }
  }
}

resource "google_secret_manager_secret_version" "secret-version-basic" {
  secret = google_secret_manager_secret.secret-basic.id

  secret_data = var.webhook_secret
}

resource "google_secret_manager_secret_iam_binding" "binding" {
  secret_id = google_secret_manager_secret.secret-basic.secret_id
  role      = "roles/secretmanager.secretAccessor"
  members = [
    "serviceAccount:${var.project}@appspot.gserviceaccount.com",
  ]
}
