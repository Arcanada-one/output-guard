# PROJECT_AAL — output-guard

> AAL = Autonomous Agents Levels. Spec: `Areas/Architecture/AAL-Classification.md`.

## Components

| Component | current_aal | target_aal | last_validated |
|---|---|---|---|
| `@arcanada/output-guard` library (TS) | L2 | L2 | 2026-05-12 |
| `arcanada-output-guard` library (Python) | L2 | L2 | 2026-05-12 |
| Model Connector `/execute` integration | L1 | L3 | 2026-05-12 |

## Rationale

### Library (L2 deterministic)

- Pure functional surface: strategy chain operates on string-in / string-out, no side effects, no env reads, no fs writes.
- Schema-validate MANDATORY gate post-repair → fail-closed.
- No model invocation inside library; `guardedGenerate` accepts caller-provided LLM callable.
- No autonomous decision: caller controls retry budget (`MAX_RETRIES=3` constant, overridable).

### MC integration (current L1 → target L3)

- L1 (bootstrap): opt-in via `output_format` DTO field; backward-compat null bypass.
- L2 (M4 ship): bounded auto-retry with circuit breaker (`MAX_RETRIES=3` + `AbortController` per-call timeout — adversarial-latency mitigation).
- L3 (post-M5 hardening): provider-native-first dispatch, Prometheus `mc_repair_retries_total` counter, replay-corpus regression gate, RepairReport observability surface.

## Weakest Links

1. Strategy ordering correctness — covered by golden-fixture parity gate (TS↔Python byte-equal) + Pass A/B/exhausted RepairReport instrumentation.
2. Upstream dep CVE (`jsonrepair`, `yaml`, `smol-toml`, `pyyaml`) — Dependabot weekly + `pnpm audit` / `pip-audit` CI gate.
3. Retry-loop cost runaway — hard `MAX_RETRIES=3` + AbortController timeout.

## L5 decision

**deferred** — grammar-constrained decoding (outlines/lm-format-enforcer) is L5-research, out of scope. Reason: vendor lock-in + no CLI-connector coverage.
