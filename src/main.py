import base64
import hashlib
import hmac
import json
import os

import requests


def post_status(event, context):
    pubsub_message = base64.b64decode(event["data"]).decode("utf-8")
    message = json.loads(pubsub_message)
    job_name = message["resource"]["labels"]["job_name"]
    hook_url = message["resource"]["labels"]["hook_url"]
    severity = message["severity"]
    print(job_name, hook_url)
    state = "failure"
    if severity == "DEBUG":
        state = "success"
    # The payload and headers for this request mimic the GitHub Events API.
    # This allows us to receive them on the same route as GitHub App webhooks
    # without special-casing in the route handler.
    payload = {
        "action": "complete",
        "job_name": job_name,
        "state": state,
    }
    payload_bytes = json.dumps(message).encode("utf-8")
    webhook_secret = bytes(os.environ["WEBHOOK_SECRET"], encoding="utf-8")
    h = hmac.new(webhook_secret, payload_bytes, hashlib.sha256)
    headers = {
        "X-GitHub-Event": "dataflow",
        "X-Hub-Signature-256": f"sha256={h.hexdigest()}",
        "Accept": "application/vnd.github.v3+json",
    }
    requests.post(
        hook_url,
        data=json.dumps(payload),
        headers=headers,
    )
