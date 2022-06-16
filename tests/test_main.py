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
    alert = {
        "incident": {
            "resource": {"labels": {"job_name": job_name}},
            "policy_name": "Dataflow Succeeded Alert",
        }
    }
    alert_bytes = json.dumps(alert).encode("utf-8")
    alert_encoded = base64.b64encode(alert_bytes)
    event = {"data": alert_encoded}
    post_status(event, {})
    requests.post.assert_called_once_with(
        f"https://api.github.com/repos/{org}/{repo}/dispatches",
        data=f'{{"client_payload": {{"flow_run_name": "{job_name}", "state": "Success"}}}}',
        headers={
            "Authorization": f"token {pat}",
            "Accept": "application/vnd.github.v3+json",
        },
    )
