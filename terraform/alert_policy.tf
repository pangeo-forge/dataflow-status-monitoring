resource "google_monitoring_notification_channel" "notification_channel" {
  display_name = "Pubsub Notification Channel"
  type         = "pubsub"
  labels = {
    topic = resource.google_pubsub_topic.topic.id
  }
}

resource "google_monitoring_alert_policy" "alert_policy" {
  display_name = "Dataflow Succeeded Alert"
  combiner     = "OR"
  conditions {
    display_name = "Dataflow Succeeded"
    condition_monitoring_query_language {
      query    = "fetch dataflow_job | metric 'dataflow.googleapis.com/job/status' | align next_older(1m) | condition eq(val(),'SUCCEEDED')"
      duration = "60s"
    }
  }
  notification_channels = [resource.google_monitoring_notification_channel.notification_channel.id]
}

resource "google_monitoring_alert_policy" "alert_failed_policy" {
  display_name = "Dataflow Failed Alert"
  combiner     = "OR"
  conditions {
    display_name = "Dataflow Failed"
    condition_monitoring_query_language {
      query    = "fetch dataflow_job | metric 'dataflow.googleapis.com/job/status' | align next_older(1m) | condition eq(val(),'FAILED')"
      duration = "60s"
    }
  }
  notification_channels = [resource.google_monitoring_notification_channel.notification_channel.id]
}
