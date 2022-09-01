resource "google_secret_manager_secret" "secret-basic" {
  for_each = [
    for app in keys(var.apps_with_secrets) : "webook-secret-${app}"
  ]
  secret_id = each.key
  labels    = {}
  replication {
    user_managed {
      replicas {
        location = var.region
      }
    }
  }
}

resource "google_secret_manager_secret_version" "secret-version-basic" {
  for_each = {
    for app, secret in var.apps_with_secrets : "webook-secret-${app}" => secret
  }
  secret = each.key
  secret_data = each.value
}

resource "google_secret_manager_secret_iam_binding" "binding" {
  secret_id = google_secret_manager_secret.secret-basic.secret_id
  role      = "roles/secretmanager.secretAccessor"
  members = [
    "serviceAccount:${var.project}@appspot.gserviceaccount.com",
  ]
}
