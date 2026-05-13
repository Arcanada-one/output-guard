# Repair order — two-pass orchestrator

## Problem

Strategies (`fix-quotes`, `fix-commas`, `fix-keys`, …) are non-commutative. Applying them in the wrong order, or in a single-pass sequence, can amplify damage. Reference: Corder's `fix-quotes × fix-commas` interaction bug.

## Decision

**Two-pass orchestrator.**

1. **Pass A — combined apply.** Run the full strategy chain in declared order, single pass. Most production failures (markdown fences, trailing commas, Python booleans) are independent and clean up in one shot. Fast path: ~250µs median.
2. **Pass B — isolating fallback.** If Pass A output fails schema validation, replay each strategy in isolation against the original input, picking the first repair that schema-validates. Slower (~3ms worst case) but interaction-safe.
3. **Exhausted.** Both passes failed → `RepairReport.pass = "exhausted"` + `final_valid = false`.

## Mandatory post-parse schema validate

The orchestrator **never** returns success without a schema check, even on syntactically-valid output. This closes failure mode F1 (semantically-wrong JSON that parses fine but breaks downstream).

## Observability

`RepairReport.pass: "A" | "B" | "exhausted"` surfaces which path produced the result. Prometheus counter `mc_repair_retries_total{provider, format, outcome}` aggregates this in Model Connector.

## Rejected alternatives

- **O1 fixed sequential single-pass** — brittle on strategy interactions (Corder bug).
- **O3 DAG with pre/post invariants** — breaks TS↔Python byte-equal parity tractability.
- **O4 property-based fuzzer** — deferred to M5 hardening.

See full tradeoff matrix in the linked creative document.
