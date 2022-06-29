resource "google_secret_manager_secret" "secret-basic" {
  secret_id = "github_repository_dispatch_pat"

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

  secret_data = var.pat
}
