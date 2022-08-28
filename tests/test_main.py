import base64
import hashlib
import hmac
import json
import os
from unittest.mock import patch
from urllib.parse import urlencode

from src.main import post_status

webhook_secret = "abcdefg"


@patch("src.main.requests")
@patch.dict(
    os.environ,
    {"WEBHOOK_SECRET": webhook_secret},
)
def test_post_status(requests):
    job_name = "a736d65652e696f2f70474b4c61447536434a7769426a4a552501"
    message = {
        "resource": {
            "labels": {
                "job_name": job_name,
            },
        },
        "severity": "DEBUG"
    }
    message_bytes = json.dumps(message).encode("utf-8")
    message_encoded = base64.b64encode(message_bytes)
    event = {"data": message_encoded}
    post_status(event, {})

    expected_payload = {
        "action": "complete",
        "recipe_run_id": 1,
        "state": "success",
    }

    expected_payload_bytes = urlencode(expected_payload, doseq=True).encode("utf-8")
    webhook_secret = bytes(os.environ["WEBHOOK_SECRET"], encoding="utf-8")
    h = hmac.new(
        webhook_secret,
        expected_payload_bytes,
        hashlib.sha256,
    )
    requests.post.assert_called_once_with(
        "https://smee.io/pGKLaDu6CJwiBjJU",
        data=expected_payload,
        headers={
            "X-GitHub-Event": "dataflow",
            "X-Hub-Signature-256": f"sha256={h.hexdigest()}",
            "Accept": "application/vnd.github.v3+json",
        },
    )
