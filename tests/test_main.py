import base64
import hashlib
import hmac
import json
import os
from unittest.mock import patch

from src.main import post_status

webhook_secret = "abcdefg"


@patch("src.main.requests")
@patch.dict(
    os.environ,
    {"WEBHOOK_SECRET": webhook_secret},
)
def test_post_status(requests):
    job_name = "test"
    hook_url = "api__pangeo-forge__org--github--hooks--"
    message = {
        "resource": {
            "labels": {
                "job_name": job_name,
                "hook_url": hook_url,
            },
        },
        "severity": "DEBUG"
    }
    message_bytes = json.dumps(message).encode("utf-8")
    message_encoded = base64.b64encode(message_bytes)
    event = {"data": message_encoded}
    post_status(event, {})

    webhook_secret = bytes(os.environ["WEBHOOK_SECRET"], encoding="utf-8")
    h = hmac.new(webhook_secret, message_bytes, hashlib.sha256)
    requests.post.assert_called_once_with(
        "https://api.pangeo-forge.org/github/hooks/",
        data=json.dumps(
            {
                "action": "complete",
                "job_name": job_name,
                "state": "success",
            }
        ),
        headers={
            "X-GitHub-Event": "dataflow",
            "X-Hub-Signature-256": f"sha256={h.hexdigest()}",
            "Accept": "application/vnd.github.v3+json",
        },
    )
