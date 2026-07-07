# Release Notes v1.1.0 Draft

This draft adds a local classifier demo layer while preserving the existing v1.0.0 receipt schema and human review template layer.

## Added

- Deterministic local request classifier.
- JSONL demo cases for preview, approval-required, blocked authority, blocked claim, blocked secret, and ambiguous requests.
- Demo runner that emits local machine-readable receipts.
- Evaluation factsheet, limitations, and public claim boundary docs.
- Tests for classifier routes, generated receipt shape, public-claim language, and remote-action absence.

## Preserved

- Existing action receipt and human review schemas.
- Existing synthetic JSON receipt examples.
- Existing GitHub Actions workflow, issue templates, PR template, and devcontainer.
- Existing v1.0.0 release notes and citation metadata.

## Not Included

- No tag creation.
- No GitHub release creation.
- No deployment.
- No package publishing.
