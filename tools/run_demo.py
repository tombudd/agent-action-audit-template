#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from agent_action_audit.classifier import make_receipt  # noqa: E402
from agent_action_audit.schema import validate_receipt  # noqa: E402


CLASSIFICATION = "PASS_AGENT_ACTION_AUDIT_LOCAL_DEMO"


def read_cases() -> list[dict[str, str]]:
    cases_path = ROOT / "examples" / "demo_cases.jsonl"
    return [
        json.loads(line)
        for line in cases_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def main() -> int:
    out_dir = ROOT / "state" / "sample_receipts"
    out_dir.mkdir(parents=True, exist_ok=True)

    receipts: list[dict[str, object]] = []
    failures: list[str] = []
    for case in read_cases():
        receipt = make_receipt(case["input"])
        receipt["case_id"] = case["id"]
        receipt["expected_route"] = case["expected_route"]
        receipt["route_matches_expected"] = receipt["route"] == case["expected_route"]
        schema_errors = validate_receipt(receipt)
        receipt["schema_valid"] = not schema_errors
        receipt["schema_errors"] = schema_errors
        receipts.append(receipt)
        if not receipt["route_matches_expected"]:
            failures.append(f"{case['id']}: expected {case['expected_route']}, got {receipt['route']}")
        if schema_errors:
            failures.append(f"{case['id']}: schema errors {schema_errors}")

    receipts_path = out_dir / "demo_receipts.jsonl"
    receipts_path.write_text(
        "\n".join(json.dumps(receipt, sort_keys=True) for receipt in receipts) + "\n",
        encoding="utf-8",
    )

    score = 100 if not failures else 80
    report = {
        "classification": CLASSIFICATION if score >= 95 else "HOLD_FOR_HUMAN_RELEASE_APPROVAL",
        "score": score,
        "receipt_count": len(receipts),
        "receipts_path": str(receipts_path.relative_to(ROOT)),
        "tests_expected": [
            "tests/test_classifier.py",
            "tests/test_public_claim_language_guard.py",
            "tests/test_receipt_schema.py",
            "tests/test_network_and_remote_action_absence.py",
        ],
        "boundary_flags": {
            "external_network_call_allowed": False,
            "github_write_allowed": False,
            "deployment_allowed": False,
            "secret_access_allowed": False,
            "memory_promotion_allowed": False,
            "runtime_authority_mutation_allowed": False,
            "public_claim_allowed": False,
        },
        "known_limitations": [
            "Keyword routing is intentionally small.",
            "Receipts describe local classifier behavior only.",
            "Public release requires separate human approval.",
        ],
        "human_approval_step_required_before_public_release": (
            "Founder review of local report, public language, repository history, and release target."
        ),
        "failures": failures,
    }

    report_path = out_dir / "z4_grading_report.json"
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
