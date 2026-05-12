# arcanada-output-guard

Python sibling of [`@arcanada/output-guard`](https://www.npmjs.com/package/@arcanada/output-guard). Mirror surface, shared golden fixtures, byte-equal parity gate.

See repository root [README](../../README.md) for full design.

## Install

```bash
pip install arcanada-output-guard
# or
uv add arcanada-output-guard
```

## Status

v0.1.0 — 15 strategies, two-pass orchestrator, pydantic + JSON-Schema adapters,
guarded_generate async wrapper, batch + class API, 253 tests (including
parity gate against fixtures-shared and hypothesis property tests).

## Quick start

```python
from output_guard import OutputGuard, pydantic_adapter, repair
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int

# Functional API
result = repair('{"name": "Alice", "age": 30,}', "json", pydantic_adapter(User))
print(result.data)                # User(name='Alice', age=30)
print(result.pass_)               # "A"
print(result.strategies_applied)  # ["fix-commas"]

# Stateful API
guard = OutputGuard(schema=User)
result = guard.repair('```json\n{"name": "Bob", "age": 25}\n```')
```

## License

MIT.
