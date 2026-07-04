# Agent Action Audit Template

A clean-room public template for documenting and testing agent action audit records.

This repository uses synthetic examples only. It does not include private prompts, production logs, customer data, proprietary architecture, real receipts, internal governance labels, credentials, or deployment details.

[![Tests](https://github.com/tombudd/agent-action-audit-template/actions/workflows/test.yml/badge.svg)](https://github.com/tombudd/agent-action-audit-template/actions/workflows/test.yml)

## Purpose

Agent systems can be useful only if their actions can be reviewed, bounded, and reconstructed. This template shows one small public pattern for representing safe and blocked agent actions with fake receipts and human review metadata.

## What This Demonstrates

- audit trail design
- safe versus blocked action records
- human review checkpoints
- schema-backed receipt validation
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

## Repository Structure

```text
agent-action-audit-template/
├── .github/
│   └── workflows/
│       └── test.yml
├── docs/
│   ├── audit_log_design.md
│   └── human_review_flow.md
├── examples/
│   ├── blocked_action_receipt.json
│   └── safe_action_receipt.json
├── schemas/
│   ├── action_receipt.schema.json
│   └── human_review.schema.json
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
