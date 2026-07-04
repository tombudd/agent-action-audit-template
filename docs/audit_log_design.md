# Audit Log Design

This template models a small public-safe action receipt. The receipt is meant to answer four questions:

1. What action was requested?
2. Was it allowed or blocked?
3. Why was that decision made?
4. Was human review required?

## Design Principles

- Use synthetic examples only.
- Record the action decision explicitly.
- Preserve a short human-readable reason.
- Represent human review status separately from the action decision.
- Keep redaction status visible.
- Avoid private prompts, production logs, customer data, proprietary architecture, and real operational traces.

## Receipt Fields

- `receipt_id`: synthetic identifier for the audit record
- `action_id`: synthetic identifier for the requested action
- `action_type`: public action category
- `requested_by`: synthetic requester
- `decision`: `allowed` or `blocked`
- `reason`: short explanation
- `risk_level`: `low`, `medium`, or `high`
- `human_review`: review metadata
- `timestamp`: synthetic timestamp
- `redaction_status`: public synthetic boundary marker

## Limitations

This template does not prove agent safety or deployment readiness. It is a small public pattern for thinking about auditability and review checkpoints.
