# Contributing

> Internal Arcanada repository. External PRs welcome — please open an issue first.

## Dev setup

```bash
# TS
cd packages/ts
pnpm install
pnpm test

# Python
cd packages/python
uv venv && source .venv/bin/activate
uv pip install -e ".[dev]"
pytest
```

## Parity rule

Every deterministic strategy in `packages/ts/src/strategies/` MUST have a byte-equal twin in `packages/python/src/output_guard/strategies/`. Golden fixtures in `fixtures-shared/strategies/<name>/{in,out}.txt` are loaded by **both** test suites — `pnpm test:parity` and `pytest tests/parity/` are required CI gates.

## Strategy ordering

See [`docs/explanation/repair-order.md`](docs/explanation/repair-order.md) for the two-pass orchestrator design (combined → isolating fallback). Adding a new strategy:

1. Document positioning rationale in `docs/reference/strategies.md`.
2. Add golden fixtures to `fixtures-shared/strategies/<name>/`.
3. Implement in both TS and Python; run parity tests.
4. Update orchestrator strategy registry in BOTH languages atomically (same PR).

## License

MIT. By contributing you agree your work is published under MIT.

## Provenance

Part of the Arcanada ecosystem. See `PROJECT_AAL.md` for autonomy level.
