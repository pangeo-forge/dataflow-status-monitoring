import base64
import json
import os
from unittest.mock import patch

from src.main import post_status

pat = "pat"
org = "org"
repo = "repo"


@patch("src.main.requests")
@patch.dict(
    os.environ,
    {"PAT": pat, "REPO_ORG": org, "REPO": repo},
)
def test_post_status(requests):
    job_name = "test"
    message = {
        "resource": {"labels": {"job_name": job_name}},
        "severity": "DEBUG"
    }
    message_bytes = json.dumps(message).encode("utf-8")
    message_encoded = base64.b64encode(message_bytes)
    event = {"data": message_encoded}
    post_status(event, {})
    requests.post.assert_called_once_with(
        f"https://api.github.com/repos/{org}/{repo}/dispatches",
        data=f'{{"event_type": "prefect_webhook", "client_payload": {{"flow_run_name": "{job_name}", "state": "Success"}}}}',
        headers={
            "Authorization": f"token {pat}",
            "Accept": "application/vnd.github.v3+json",
        },
    )
