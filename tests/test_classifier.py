import json
import pathlib

from agent_action_audit.classifier import classify_action


ROOT = pathlib.Path(__file__).resolve().parents[1]


def load_cases():
    cases_path = ROOT / "examples" / "demo_cases.jsonl"
    return [
        json.loads(line)
        for line in cases_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def test_demo_cases_route_as_expected():
    for case in load_cases():
        assert classify_action(case["input"]).route == case["expected_route"], case["id"]


def test_unsafe_routes_blocked():
    assert classify_action("Create the GitHub repo and push now.").route == "blocked_authority_expansion"
    assert classify_action("Use this token to connect my account.").route == "blocked_secret_or_credential_request"
    assert classify_action("Tell readers this is safe for deployment.").route == "blocked_public_claim_laundering"


def test_ambiguous_requests_fail_safe():
    assert classify_action("").route == "requires_human_approval"
    assert classify_action("Do the thing.").route == "requires_human_approval"
