from agent_action_audit.classifier import make_receipt
from agent_action_audit.schema import BOUNDARY_FLAG_KEYS, validate_receipt


def test_demo_receipt_schema_valid_for_preview_case():
    receipt = make_receipt("Review this README locally.")
    assert validate_receipt(receipt) == []


def test_demo_receipt_contains_boundary_flags():
    receipt = make_receipt("Review this README locally.")
    assert set(receipt["boundary_flags"]) == BOUNDARY_FLAG_KEYS
    assert all(value is False for value in receipt["boundary_flags"].values())


def test_demo_receipt_schema_rejects_unknown_route():
    receipt = make_receipt("Review this README locally.")
    receipt["route"] = "unknown"
    assert validate_receipt(receipt)
