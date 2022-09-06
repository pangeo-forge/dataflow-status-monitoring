resource "google_logging_project_sink" "logsink" {
  name                   = "${var.env}-logsink"
  destination            = "pubsub.googleapis.com/projects/${var.project}/topics/${resource.google_pubsub_topic.topic.name}"
  filter                 = "resource.type = dataflow_step AND logName=(\"projects/${var.project}/logs/dataflow.googleapis.com%2Fjob-message\") AND ((severity=ERROR AND textPayload=~\"^Workflow failed.*\") OR (severity=DEBUG AND textPayload=~\"^Executing success step success.*$\"))"
  unique_writer_identity = true
}
