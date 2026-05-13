# @arcanada/output-guard

> Ecosystem-wide LLM structured-output repair pipeline.
>
> **Жизнь одного человека имеет значение / One human life matters**

Validate, repair, and retry LLM responses across **JSON / YAML / TOML / Python-literal** formats. Battle-tested 15-strategy chain ported from [ndcorder/outputguard](https://github.com/ndcorder/outputguard) (MIT) into a stack-neutral TS + Python monorepo with shared golden fixtures.

## Packages

| Package | Registry | Status |
|---|---|---|
| `@arcanada/output-guard` | npm | v0.1.x |
| `arcanada-output-guard` | PyPI | v0.1.x |

## Layout

```
packages/ts/        TypeScript library (ESM + CJS dual)
packages/python/    Python library (3.11+)
fixtures-shared/    Cross-language golden fixtures (byte-equal parity gate)
benchmark/          Arcanada-provider replay corpus
docs/               Diátaxis (tutorials / how-to / reference / explanation)
```

## Design

- **Two-pass orchestrator** (combined-apply → isolating-fallback) — see [`docs/explanation/repair-order.md`](docs/explanation/repair-order.md).
- **Post-parse schema-validate MANDATORY** — orchestrator never returns success without schema check.
- **`RepairReport.pass: "A" | "B" | "exhausted"`** for observability.
- **AAL: L2 lib / L3 MC integration** — see [`PROJECT_AAL.md`](PROJECT_AAL.md).

## License

MIT — see [LICENSE](LICENSE).

## Provenance

Part of the Arcanada Ecosystem — Model Connector domain.
