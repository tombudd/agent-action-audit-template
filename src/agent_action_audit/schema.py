from __future__ import annotations

from typing import Any


VERSION = "0.1.0"

ROUTES = {
    "allowed_local_preview",
    "requires_human_approval",
    "blocked_authority_expansion",
    "blocked_public_claim_laundering",
    "blocked_secret_or_credential_request",
}

RECEIPT_REQUIRED_KEYS = {
    "receipt_version",
    "timestamp_utc",
    "input_hash_sha256",
    "route",
    "reason",
    "boundary_flags",
    "classifier_version",
}

BOUNDARY_FLAG_KEYS = {
    "external_network_call_allowed",
    "github_write_allowed",
    "deployment_allowed",
    "secret_access_allowed",
    "memory_promotion_allowed",
    "runtime_authority_mutation_allowed",
    "public_claim_allowed",
}


def validate_receipt(receipt: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    missing = RECEIPT_REQUIRED_KEYS - set(receipt)
    if missing:
        errors.append(f"missing receipt keys: {sorted(missing)}")

    route = receipt.get("route")
    if route not in ROUTES:
        errors.append(f"unknown route: {route}")

    flags = receipt.get("boundary_flags")
    if not isinstance(flags, dict):
        errors.append("boundary_flags must be an object")
    else:
        missing_flags = BOUNDARY_FLAG_KEYS - set(flags)
        if missing_flags:
            errors.append(f"missing boundary flags: {sorted(missing_flags)}")
        for key in BOUNDARY_FLAG_KEYS & set(flags):
            if flags[key] is not False:
                errors.append(f"boundary flag must be false: {key}")

    if not isinstance(receipt.get("input_hash_sha256"), str) or len(receipt.get("input_hash_sha256", "")) != 64:
        errors.append("input_hash_sha256 must be a 64 character hex string")

    return errors
