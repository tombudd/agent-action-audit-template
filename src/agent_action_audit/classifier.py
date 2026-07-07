from __future__ import annotations

import datetime as dt
import hashlib
from dataclasses import dataclass
from typing import Any

from .schema import VERSION


AUTHORITY_TERMS = (
    "deploy",
    "publish",
    "push",
    "create github repo",
    "github repo",
    "connect account",
    "send email",
    "external api",
    "remote service",
    "expand authority",
    "runtime authority",
    "autonomous action",
)

SECRET_TERMS = (
    "api key",
    "secret",
    "token",
    "credential",
    "private key",
    "hidden account",
    "password",
)

PUBLIC_CLAIM_TERMS = (
    "certify safety",
    "certified safe",
    "prove alignment",
    "proves alignment",
    "prove agentic ai is safe",
    "safe for deployment",
    "deployment-ready",
    "external validation",
    "guarantee",
)

APPROVAL_TERMS = (
    "for my approval",
    "approval first",
    "approve before",
    "release checklist",
    "human approval",
)

LOCAL_PREVIEW_TERMS = (
    "review",
    "suggest",
    "preview",
    "local",
    "draft",
    "summarize",
)


@dataclass(frozen=True)
class Classification:
    route: str
    reason: str


def _contains_any(text: str, terms: tuple[str, ...]) -> str | None:
    normalized = " ".join(text.lower().split())
    for term in terms:
        if term in normalized:
            return term
    return None


def classify_action(request_text: str) -> Classification:
    if not request_text or not request_text.strip():
        return Classification(
            route="requires_human_approval",
            reason="Empty or ambiguous request requires human approval.",
        )

    secret_term = _contains_any(request_text, SECRET_TERMS)
    if secret_term:
        return Classification(
            route="blocked_secret_or_credential_request",
            reason=f"Request mentions credential handling: {secret_term}.",
        )

    claim_term = _contains_any(request_text, PUBLIC_CLAIM_TERMS)
    if claim_term:
        return Classification(
            route="blocked_public_claim_laundering",
            reason=f"Request attempts to overstate evidence: {claim_term}.",
        )

    authority_term = _contains_any(request_text, AUTHORITY_TERMS)
    if authority_term:
        return Classification(
            route="blocked_authority_expansion",
            reason=f"Request asks for external action or authority expansion: {authority_term}.",
        )

    approval_term = _contains_any(request_text, APPROVAL_TERMS)
    if approval_term:
        return Classification(
            route="requires_human_approval",
            reason=f"Request explicitly depends on human approval: {approval_term}.",
        )

    preview_term = _contains_any(request_text, LOCAL_PREVIEW_TERMS)
    if preview_term:
        return Classification(
            route="allowed_local_preview",
            reason=f"Request is bounded to local preview work: {preview_term}.",
        )

    return Classification(
        route="requires_human_approval",
        reason="Ambiguous request fails safe to human approval.",
    )


def boundary_flags() -> dict[str, bool]:
    return {
        "external_network_call_allowed": False,
        "github_write_allowed": False,
        "deployment_allowed": False,
        "secret_access_allowed": False,
        "memory_promotion_allowed": False,
        "runtime_authority_mutation_allowed": False,
        "public_claim_allowed": False,
    }


def make_receipt(request_text: str) -> dict[str, Any]:
    classification = classify_action(request_text)
    return {
        "receipt_version": "agent-action-audit-receipt-v1",
        "timestamp_utc": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(),
        "input_hash_sha256": hashlib.sha256(request_text.encode("utf-8")).hexdigest(),
        "route": classification.route,
        "reason": classification.reason,
        "boundary_flags": boundary_flags(),
        "classifier_version": VERSION,
    }
