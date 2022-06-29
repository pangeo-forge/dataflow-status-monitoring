resource "google_secret_manager_secret" "secret-basic" {
  secret_id = "github_repository_dispatch_pat-latest"

  replication {
    automatic = true
  }
}


resource "google_secret_manager_secret_version" "secret-version-basic" {
  secret = google_secret_manager_secret.secret-basic.id

  secret_data = var.pat
}
