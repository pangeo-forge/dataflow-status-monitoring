import base64
import json
import os

import requests


def post_status(event, context):
    pubsub_message = base64.b64decode(event["data"]).decode("utf-8")
    message = json.loads(pubsub_message)
    job_name = message["incident"]["resource"]["labels"]["job_name"]
    print(job_name)
    policy_name = message["incident"]["policy_name"]
    state = "Failure"
    if policy_name == "Dataflow Succeeded Alert":
        state = "Success"
    payload = {"client_payload": {"flow_run_name": job_name, "state": state}}
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
