import base64
import json
import os

import requests


def post_status(event, context):
    pubsub_message = base64.b64decode(event["data"]).decode("utf-8")
    message = json.loads(pubsub_message)
    job_name = message["resource"]["labels"]["job_name"]
    severity = message["severity"]
    print(job_name)
    state = "Failure"
    if severity == "DEBUG":
        state = "Success"
    payload = {
        # NOTE: These webhooks originate from Dataflow, but we're using
        # Prefectisms ("prefect_webhook", "flow_run_name") for backwards
        # compatibility during the transition from Prefect -> Dataflow.
        # These can be changed once all systems switch to Dataflow.
        "event_type": "prefect_webhook",
        "client_payload": {"flow_run_name": job_name, "state": state},
    }
    headers = {
        "Authorization": f"token {os.environ['PAT']}",
        "Accept": "application/vnd.github.v3+json",
    }
    org = os.environ['REPO_ORG']
    repo = os.environ['REPO']
    requests.post(
        f"https://api.github.com/repos/{org}/{repo}/dispatches",
        data=json.dumps(payload),
        headers=headers,
    )
