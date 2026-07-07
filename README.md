# Agent Action Audit Template

A clean-room public template for documenting and testing agent action audit records.

This repository uses synthetic examples only. It does not include private prompts, production logs, customer data, proprietary architecture, real receipts, internal governance labels, credentials, or deployment details.

[![Tests](https://github.com/tombudd/agent-action-audit-template/actions/workflows/test.yml/badge.svg)](https://github.com/tombudd/agent-action-audit-template/actions/workflows/test.yml)

Release: [v1.0.0](https://github.com/tombudd/agent-action-audit-template/releases/tag/v1.0.0)

## Purpose

Agent systems can be useful only if their actions can be reviewed, bounded, and reconstructed. This template shows one small public pattern for representing safe and blocked agent actions with fake receipts and human review metadata.

## Two Layers

This repository now has two complementary layers:

- receipt schema and human review templates
- local request classifier demo

The schema layer shows how to represent allowed and blocked action records. The classifier demo shows how a local request can be routed before any action is taken.

## What This Demonstrates

- audit trail design
- safe versus blocked action records
- human review checkpoints
- JSON Schema-backed receipt validation
- deterministic local request classification
- preview versus execution boundaries
- public-claim and remote-action guard checks
- negative tests for invalid or incomplete receipts
- public-safe synthetic examples
- pytest verification

## Included

- one synthetic allowed-action receipt
- one synthetic blocked-action receipt
- action receipt JSON schema
- human review JSON schema
- pytest validation
- GitHub Actions test workflow
- synthetic examples only
- local classifier demo cases
- generated sample classifier receipts

## Validation Coverage

The test suite checks that:

- valid allowed-action receipts pass schema validation
- valid blocked-action receipts pass schema validation
- missing required fields fail validation
- invalid decision enum values fail validation
- unexpected top-level fields fail validation
- missing nested human-review fields fail validation
- invalid nested human-review status values fail validation
- examples avoid prohibited private-data markers
- classifier demo cases route as expected
- ambiguous requests fail safe to human approval
- generated classifier receipts include boundary flags
- public text avoids assertive overclaim language
- runtime demo code avoids network, deploy, GitHub write, and secret-environment patterns

## Repository Structure

```text
agent-action-audit-template/
├── .github/
│   └── workflows/
│       └── test.yml
├── docs/
│   ├── audit_log_design.md
│   ├── human_review_flow.md
│   ├── EVAL_FACTSHEET.md
│   ├── LIMITATIONS.md
│   └── PUBLIC_CLAIM_BOUNDARY.md
├── examples/
│   ├── blocked_action_receipt.json
│   ├── demo_cases.jsonl
│   └── safe_action_receipt.json
├── schemas/
│   ├── action_receipt.schema.json
│   └── human_review.schema.json
├── src/
│   └── agent_action_audit/
├── tools/
│   └── run_demo.py
├── tests/
│   └── test_receipt_schema.py
├── README.md
└── requirements.txt
```

## Run Locally

```bash
pip install -r requirements.txt
pytest
```

Run the local classifier demo:

```bash
python3 tools/run_demo.py
```

## Limitations

This is a small template, not a production governance system. Passing these tests does not prove agent safety, deployment readiness, compliance, or complete auditability.

## Public Boundary

This repository intentionally excludes:

- private prompts
- private schemas
- production logs
- customer data
- real receipts
- proprietary architecture
- internal governance labels
- deployment details
