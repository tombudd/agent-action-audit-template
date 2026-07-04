from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, RefResolver


ROOT = Path(__file__).resolve().parents[1]
ACTION_SCHEMA = ROOT / "schemas" / "action_receipt.schema.json"
HUMAN_REVIEW_SCHEMA = ROOT / "schemas" / "human_review.schema.json"
SAFE_RECEIPT = ROOT / "examples" / "safe_action_receipt.json"
BLOCKED_RECEIPT = ROOT / "examples" / "blocked_action_receipt.json"

PROHIBITED_MARKERS = [
    "private_prompt",
    "hidden_prompt",
    "private_schema",
    "production_log",
    "customer_data",
    "secret_key",
    "api_key",
]


@pytest.fixture()
def action_validator() -> Draft202012Validator:
    action_schema = _load_json(ACTION_SCHEMA)
    human_review_schema = _load_json(HUMAN_REVIEW_SCHEMA)
    resolver = RefResolver.from_schema(
        action_schema,
        store={"human_review.schema.json": human_review_schema},
    )
    return Draft202012Validator(action_schema, resolver=resolver)


def test_safe_action_receipt_matches_schema(action_validator: Draft202012Validator) -> None:
    receipt = _load_json(SAFE_RECEIPT)

    assert _validation_errors(action_validator, receipt) == []
    assert receipt["decision"] == "allowed"
    assert receipt["human_review"]["required"] is False


def test_blocked_action_receipt_matches_schema(action_validator: Draft202012Validator) -> None:
    receipt = _load_json(BLOCKED_RECEIPT)

    assert _validation_errors(action_validator, receipt) == []
    assert receipt["decision"] == "blocked"
    assert receipt["human_review"]["required"] is True
    assert receipt["human_review"]["status"] == "pending"


def test_examples_preserve_public_boundary() -> None:
    for path in [SAFE_RECEIPT, BLOCKED_RECEIPT]:
        text = path.read_text(encoding="utf-8").lower()
        for marker in PROHIBITED_MARKERS:
            assert marker not in text


def test_missing_required_field_fails_validation(
    action_validator: Draft202012Validator,
) -> None:
    receipt = _load_json(SAFE_RECEIPT)
    receipt.pop("decision")

    errors = _validation_errors(action_validator, receipt)

    assert any("'decision' is a required property" in error for error in errors)


def test_invalid_decision_enum_fails_validation(
    action_validator: Draft202012Validator,
) -> None:
    receipt = _load_json(SAFE_RECEIPT)
    receipt["decision"] = "auto_executed"

    errors = _validation_errors(action_validator, receipt)

    assert any("auto_executed" in error for error in errors)


def test_unexpected_top_level_field_fails_validation(
    action_validator: Draft202012Validator,
) -> None:
    receipt = _load_json(SAFE_RECEIPT)
    receipt["private_prompt"] = "synthetic placeholder that should still be rejected"

    errors = _validation_errors(action_validator, receipt)

    assert any("Additional properties are not allowed" in error for error in errors)


def test_missing_nested_human_review_field_fails_validation(
    action_validator: Draft202012Validator,
) -> None:
    receipt = _load_json(BLOCKED_RECEIPT)
    receipt["human_review"] = copy.deepcopy(receipt["human_review"])
    receipt["human_review"].pop("status")

    errors = _validation_errors(action_validator, receipt)

    assert any("'status' is a required property" in error for error in errors)


def test_invalid_nested_human_review_enum_fails_validation(
    action_validator: Draft202012Validator,
) -> None:
    receipt = _load_json(BLOCKED_RECEIPT)
    receipt["human_review"] = copy.deepcopy(receipt["human_review"])
    receipt["human_review"]["status"] = "silently_approved"

    errors = _validation_errors(action_validator, receipt)

    assert any("silently_approved" in error for error in errors)


def _validation_errors(
    validator: Draft202012Validator,
    receipt: dict,
) -> list[str]:
    return sorted(error.message for error in validator.iter_errors(receipt))


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))
