# @arcanada/output-guard

> Ecosystem-wide LLM structured-output repair pipeline.
>
> **Жизнь одного человека имеет значение / One human life matters**

Validate, repair, and retry LLM responses across **JSON / YAML / TOML / Python-literal** formats. Battle-tested 15-strategy chain ported from [ndcorder/outputguard](https://github.com/ndcorder/outputguard) (MIT) into a stack-neutral TS + Python monorepo with shared golden fixtures.

## Packages

| Package | Registry | Status |
|---|---|---|
| `@arcanada/output-guard` | npm | bootstrap (v0.0.1 placeholder, v0.1.0 in progress per CONN-0087 M2) |
| `arcanada-output-guard` | PyPI | bootstrap (v0.0.1 placeholder, v0.1.0 in progress per CONN-0087 M3) |

## Layout

```
packages/ts/        TypeScript library (ESM + CJS dual)
packages/python/    Python library (3.11+)
fixtures-shared/    Cross-language golden fixtures (byte-equal parity gate)
benchmark/          Arcanada-provider replay corpus
docs/               Diátaxis (tutorials / how-to / reference / explanation)
```

## Design

- **Two-pass orchestrator** (combined-apply → isolating-fallback) per [creative-CONN-0087](https://github.com/Arcanada-one/datarim/blob/main/datarim/creative/creative-CONN-0087-algorithm-strategy-ordering.md).
- **Post-parse schema-validate MANDATORY** — orchestrator never returns success without schema check.
- **`RepairReport.pass: "A" | "B" | "exhausted"`** for observability.
- **AAL: L2 lib / L3 MC integration** — see [`PROJECT_AAL.md`](PROJECT_AAL.md).

## License

MIT — see [LICENSE](LICENSE).

## Provenance

Task: [CONN-0087](https://github.com/Arcanada-one/datarim/blob/main/datarim/tasks/CONN-0087-task-description.md) — Arcanada Ecosystem, Model Connector domain.
