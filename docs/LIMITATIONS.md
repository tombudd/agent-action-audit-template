# Limitations

This repository is intentionally small and deterministic.

It can demonstrate route discipline for example requests, but it cannot establish that every future agent action is safe. It does not inspect live accounts, execute remote actions, connect services, or validate a production deployment.

Known limits:

- Keyword routing can miss unusual phrasing.
- Ambiguous requests are routed to human approval instead of being executed.
- Receipts record local classifier decisions only.
- The public-language checks cover this repository surface, not every future downstream copy.
- The remote-action absence test is a static local check, not a sandbox monitor.

Any public release requires a separate human approval step.
