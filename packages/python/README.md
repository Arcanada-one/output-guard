# arcanada-output-guard

[![PyPI](https://img.shields.io/pypi/v/arcanada-output-guard.svg)](https://pypi.org/project/arcanada-output-guard/)
[![Python](https://img.shields.io/pypi/pyversions/arcanada-output-guard.svg)](https://pypi.org/project/arcanada-output-guard/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)

Validate, repair, and retry LLM structured output (JSON / YAML / TOML / Python literal) — battle-tested 15-strategy repair chain with two-pass orchestrator. Python sibling of [`@arcanada/output-guard`](https://www.npmjs.com/package/@arcanada/output-guard) with shared golden fixtures and byte-equal parity gate.

## Install

```bash
pip install arcanada-output-guard
# or
uv add arcanada-output-guard
# or
poetry add arcanada-output-guard
```

Requires Python **≥ 3.11**. Runtime deps: `pyyaml`, `tomli-w`, `pydantic`, `jsonschema`, `json-repair`.

## Quick start

```python
from output_guard import repair

# Functional API — format-only repair, no schema
result = repair('{"name": "Alice", "age": 30,}', "json")

print(result.data)                  # {'name': 'Alice', 'age': 30}
print(result.repaired)              # True
print(result.pass_)                 # 'A'
print(result.strategies_applied)    # ['fix-commas']
```

## Stateful API with pydantic schema

```python
from pydantic import BaseModel
from output_guard import OutputGuard

class User(BaseModel):
    name: str
    age: int

guard = OutputGuard(format="json", schema=User)
result = guard.repair('```json\n{"name": "Bob", "age": 25}\n```')

print(result.data)               # User(name='Bob', age=25)
print(result.pass_)              # 'A' or 'B'
```

## Output format support

- **JSON** — strict + relaxed parsing with common error recovery (trailing commas, unquoted keys, single→double quote, true/false casing, fenced blocks).
- **YAML** — structural repair for indentation + missing keys.
- **TOML** — fixing malformed tables and value assignments.
- **Python literal** — `dict` / `list` literals via safe `ast.literal_eval`.
- **Auto-detect** — pass `format="auto"` to infer from content.

## `RepairResult` semantics

```python
@dataclass(frozen=True, slots=True)
class RepairResult:
    repaired: bool                       # False when raw was already valid
    raw: str                             # original input as supplied
    pass_: Literal["A", "B"]             # "A" = combined-apply; "B" = isolating fallback
    data: Any = None                     # parsed + (optionally) schema-validated payload
    strategies_applied: list[str] = []   # ordered list of repair strategies invoked
```

`MAX_RETRIES` exhaustion signals via `ParseError` raise, not via a `pass_` value.

## Async wrapper for LLM calls

```python
import asyncio
from pydantic import BaseModel
from output_guard import guarded_generate, GuardedGenerateOptions

class Answer(BaseModel):
    result: int

async def my_llm(prompt: str, history=None) -> str:
    # call your LLM client here (OpenAI / Anthropic / OpenRouter / MC / etc.)
    return '{"result": 42}'

async def main():
    out = await guarded_generate(GuardedGenerateOptions(
        generate=my_llm,
        prompt='Return JSON {"result": <integer>}',
        schema=Answer,
        fmt="json",
        max_retries=3,
    ))
    print(out.data)                  # Answer(result=42)
    print(out.pass_)                 # 'A' | 'B'
    print(out.strategies_applied)

asyncio.run(main())
```

## Error handling

```python
from output_guard import (
    ParseError,
    SchemaValidationError,
    RepairError,
    GuardedGenerationError,
)

try:
    result = guard.repair(bad_input)
except SchemaValidationError:
    ...  # input parsed but doesn't satisfy schema
except ParseError:
    ...  # MAX_RETRIES exhausted — all strategies failed
except RepairError:
    ...  # a repair strategy itself raised
except GuardedGenerationError:
    ...  # guarded_generate gave up after max_retries LLM round-trips
```

## Schema adapters

```python
from output_guard import pydantic_adapter, jsonschema_adapter
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int

# pydantic v2
adapter = pydantic_adapter(User)

# JSON Schema (dict)
adapter = jsonschema_adapter({
    "type": "object",
    "properties": {"name": {"type": "string"}, "age": {"type": "integer"}},
    "required": ["name", "age"],
})
```

## Batch API

```python
from output_guard import repair_batch

results = repair_batch(
    ['{"a": 1,}', '{"b": 2,}', '{"c": 3,}'],
    fmt="json",
)
# returns list[RepairResult]; per-item failure surfaces as RepairResult with repaired=False
```

## Documentation

- Source: https://github.com/Arcanada-one/output-guard/tree/main/packages/python
- Design (two-pass orchestrator, strategy ordering): see [repository docs](https://github.com/Arcanada-one/output-guard/blob/main/docs/explanation/repair-order.md)
- TypeScript sibling: https://www.npmjs.com/package/@arcanada/output-guard

## License

MIT — see [LICENSE](https://github.com/Arcanada-one/output-guard/blob/main/LICENSE).

---

**Жизнь одного человека имеет значение / One human life matters**
