# Human Review Flow

This template separates an action decision from human review metadata.

## Review States

- `not_required`: the action is low risk and does not require review in this synthetic example
- `pending`: the action is held until a human reviews it
- `approved`: a human has approved the action in a synthetic review scenario
- `blocked`: a human has blocked the action in a synthetic review scenario

## Example Flow

```text
requested action -> risk check -> allow or block -> record receipt -> review if needed
```

## Public Boundary

The examples are fake public fixtures. They do not represent production systems, private approvals, real users, private logs, deployment events, or proprietary architecture.
