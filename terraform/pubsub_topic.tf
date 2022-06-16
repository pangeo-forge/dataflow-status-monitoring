resource "google_pubsub_topic" "topic" {
  name = "dataflow-status-topic"
}
data "google_project" "project" {}
data "google_iam_policy" "publisher" {
  binding {
    role = "roles/pubsub.publisher"
    members = [
      "serviceAccount:service-${data.google_project.project.number}@gcp-sa-monitoring-notification.iam.gserviceaccount.com",
    ]
  }
}

resource "google_pubsub_topic_iam_policy" "policy" {
  project     = var.project
  topic       = resource.google_pubsub_topic.topic.name
  policy_data = data.google_iam_policy.publisher.policy_data
}

