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
    job_name: str = message["resource"]["labels"]["job_name"]
    severity = message["severity"]

    # parse job name into repo_id and check_run_id
    # we assume job_names are formatted such as 'repo537721725-checkrun11696408457'
    # 
    # FIXME: eventually the current function will be owned as part of bakery infrastructure,
    # not github app infrastructure. when that happens, we want to make sure that the version
    # of the job name _encoder_ used in the github app does not fall out of sync with this
    # _decoding_ process. various options may exist to solve this problem, including factoring
    # job name encode/decode into a small shared library?
    repo_id, check_run_id = job_name.split("-")
    repo_id = repo_id.split("repo")[-1]
    check_run_id = check_run_id.split("checkrun")[-1]

    # get check run from github api
    check_run = requests.get(
        f"https://api.github.com/repositories/{repo_id}/check-runs/{check_run_id}"
    ).json()

    # determine webhook url based on app name
    gh_app_name = check_run["app"]["name"]
    if gh_app_name == "dev-app-proxy":
        # would there ever be > 1 element in this "pull_requests" array?
        pr_url = check_run["pull_requests"][0]["url"]
        pr = requests.get(pr_url).json()

        # the assumption here is that, if the app is dev-app-proxy, then the pr must have
        # a label of the format `fwd:{WEBHOOK_URL}` where WEBHOOK_URL is the address where
        # the dev app receives webhooks (minus 'https://', for brevity, so we add that belpw).
        label_names: list[str] = [l["name"] for l in pr["labels"]]
        if not any([n.startswith("fwd:") for n in label_names]):
            raise ValueError(f"{pr_url} missing `fwd:` label. Cannot determine webhook url.")
        webhook_url = [
            "https://" + n.split("fwd:")[-1] for n in label_names if n.startswith("fwd")
        ].pop(0)  # TODO: do we care about the case of > 1 forwarding addresses?
    
    # TODO: improve this. ideally we shouldn't be making hardcoded assumptions here.
    elif gh_app_name == "pangeo-forge":
        webhook_url = "https://api.pangeo-forge.org/github/hooks/"
    elif gh_app_name == "pangeo-forge-staging":
        webhook_url = "https://api-staging.pangeo-forge.org/github/hooks/"
    else:
        raise NotImplementedError(f"Unkown webhook url for {gh_app_name = }.")

    print(f"{job_name = }", f"{webhook_url = }")

    # infer conclusion from severity level
    conclusion = "failure"
    if severity == "DEBUG":
        conclusion = "success"

    # The payload and headers for this request mimic the GitHub Events API.
    # This allows us to receive them on the same route as GitHub App webhooks
    # without special-casing in the route handler.
    payload = {
        "action": "completed",
        "job_name": job_name,
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
