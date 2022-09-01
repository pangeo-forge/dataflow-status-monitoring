resource "google_secret_manager_secret" "secret-basic" {
  for_each = nonsensitive(toset(keys(var.apps_with_secrets)))
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
  for_each = nonsensitive(toset(keys(var.apps_with_secrets)))
  secret = each.key
  secret_data = var.apps_with_secrets[each.key]
}

resource "google_secret_manager_secret_iam_binding" "binding" {
  for_each = nonsensitive(toset(keys(var.apps_with_secrets)))
  secret_id = each.key
  role      = "roles/secretmanager.secretAccessor"
  members = [
    "serviceAccount:${var.project}@appspot.gserviceaccount.com",
  ]
}
