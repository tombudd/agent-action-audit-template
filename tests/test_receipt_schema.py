from __future__ import annotations

import json
from pathlib import Path


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


def test_safe_action_receipt_matches_schema() -> None:
    receipt = _load_json(SAFE_RECEIPT)
    action_schema = _load_json(ACTION_SCHEMA)
    human_review_schema = _load_json(HUMAN_REVIEW_SCHEMA)

    assert _validate_action_receipt(receipt, action_schema, human_review_schema) == []
    assert receipt["decision"] == "allowed"
    assert receipt["human_review"]["required"] is False


def test_blocked_action_receipt_matches_schema() -> None:
    receipt = _load_json(BLOCKED_RECEIPT)
    action_schema = _load_json(ACTION_SCHEMA)
    human_review_schema = _load_json(HUMAN_REVIEW_SCHEMA)

    assert _validate_action_receipt(receipt, action_schema, human_review_schema) == []
    assert receipt["decision"] == "blocked"
    assert receipt["human_review"]["required"] is True
    assert receipt["human_review"]["status"] == "pending"


def test_examples_preserve_public_boundary() -> None:
    for path in [SAFE_RECEIPT, BLOCKED_RECEIPT]:
        text = path.read_text(encoding="utf-8").lower()
        for marker in PROHIBITED_MARKERS:
            assert marker not in text


def test_missing_required_field_fails_validation() -> None:
    receipt = _load_json(SAFE_RECEIPT)
    action_schema = _load_json(ACTION_SCHEMA)
    human_review_schema = _load_json(HUMAN_REVIEW_SCHEMA)
    receipt.pop("decision")

    errors = _validate_action_receipt(receipt, action_schema, human_review_schema)

    assert "missing required field: decision" in errors


def _validate_action_receipt(
    receipt: dict,
    action_schema: dict,
    human_review_schema: dict,
) -> list[str]:
    errors: list[str] = []

    errors.extend(_validate_object(receipt, action_schema))
    if isinstance(receipt.get("human_review"), dict):
        errors.extend(
            f"human_review.{error}"
            for error in _validate_object(receipt["human_review"], human_review_schema)
        )

    return errors


def _validate_object(data: dict, schema: dict) -> list[str]:
    errors: list[str] = []

    for field in schema.get("required", []):
        if field not in data:
            errors.append(f"missing required field: {field}")

    allowed_properties = set(schema.get("properties", {}))
    for field, value in data.items():
        if field not in allowed_properties:
            errors.append(f"unexpected field: {field}")
            continue

        property_schema = schema["properties"][field]
        if "enum" in property_schema and value not in property_schema["enum"]:
            errors.append(f"invalid enum value for {field}: {value}")
        if property_schema.get("type") == "boolean" and not isinstance(value, bool):
            errors.append(f"invalid boolean field: {field}")
        if property_schema.get("type") == "string" and not isinstance(value, str):
            errors.append(f"invalid string field: {field}")

    return errors


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))
