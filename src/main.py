import base64
import hashlib
import hmac
import json
import os
from urllib.parse import urlencode

import requests


def post_status(event, context):
    pubsub_message = base64.b64decode(event["data"]).decode("utf-8")
    message = json.loads(pubsub_message)
    job_name = message["resource"]["labels"]["job_name"]
    severity = message["severity"]

    # reconstruct webhook_url and recipe_run_id from encoded job_name
    job_name = job_name[1:]  # drop leading 'a' from job_name
    as_pairs = [a + b for a, b in zip(job_name[::2], job_name[1::2])]
    control_character_idx = [
        i for i, val in enumerate(as_pairs) if chr(int(val, 16)) == "%"
    ].pop(0)
    recipe_run_id = int("".join(as_pairs[control_character_idx + 1:]))
    webhook_url = "".join(
        [chr(int(val, 16)) for val in as_pairs[:control_character_idx]]
    )
    # if "smee" in url, this is a proxy service, which doesn't take the "/github/hooks/"
    # route. otherwise, this is a named deployment, and we need to append this route.
    # currently, local proxy services other than smee are not supported.
    if "smee" not in webhook_url:
        webhook_url += "/github/hooks/"
    print(f"{job_name = }", f"{recipe_run_id = }", f"{webhook_url = }")

    # infer conclusion from severity level
    conclusion = "failure"
    if severity == "DEBUG":
        conclusion = "success"

    # The payload and headers for this request mimic the GitHub Events API.
    # This allows us to receive them on the same route as GitHub App webhooks
    # without special-casing in the route handler.
    payload = {
        "action": "completed",
        "recipe_run_id": recipe_run_id,
        "conclusion": conclusion,
    }
    payload_bytes = urlencode(payload, doseq=True).encode("utf-8")
    webhook_secret = bytes(os.environ["WEBHOOK_SECRET"], encoding="utf-8")
    h = hmac.new(webhook_secret, payload_bytes, hashlib.sha256)
    headers = {
        "X-GitHub-Event": "dataflow",
        "X-Hub-Signature-256": f"sha256={h.hexdigest()}",
        "Accept": "application/vnd.github.v3+json",
    }
    response = requests.post(
        f"https://{webhook_url}",
        data=payload,
        headers=headers,
    )
    print(f"{response.status_code = }", f"{response.text = }")
