# fixtures-shared

Language-agnostic golden fixtures consumed by **both** TS and Python test suites. Byte-equal parity gate per CONTRIBUTING.md.

## Layout

```
strategies/<name>/in.txt    raw input
strategies/<name>/out.txt   expected output after applying strategy <name> in isolation
formats/<format>/...        per-format integration samples
parity/...                  deterministic full-chain in/out
```

## Discipline

- Encoding: UTF-8 without BOM.
- Trailing newline: present.
- One fixture set per strategy/format; do NOT branch by language.
- Adding a fixture: open PR touching both `packages/ts/tests/parity/` and `packages/python/tests/parity/` to load it; CI parity job must stay green.
