# Evaluation Factsheet

## Scope

The evaluator checks whether a text request should remain a local preview, require human approval, or be blocked.

## Routes

- `allowed_local_preview`: local review or suggestion only
- `requires_human_approval`: a bounded request that needs explicit approval first
- `blocked_authority_expansion`: remote action, account connection, release, or authority expansion request
- `blocked_public_claim_laundering`: language that turns limited evidence into broad public assurance
- `blocked_secret_or_credential_request`: credential, token, key, or hidden-access request

## Evidence

Evidence consists of local unit tests and JSON receipts generated from demo cases. This evidence supports the local demo behavior only.

## Non-Goals

The evaluator does not perform remote actions, connect services, process secrets, or approve release.
