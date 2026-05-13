# @arcanada/output-guard

![npm version](https://img.shields.io/npm/v/@arcanada/output-guard) ![License: MIT](https://img.shields.io/badge/license-MIT-green) [![CI](https://github.com/Arcanada-one/output-guard/actions/workflows/ci.yml/badge.svg)](https://github.com/Arcanada-one/output-guard/actions) ![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-blue)

Validate, repair, and retry LLM structured output (JSON / YAML / TOML / Python literal) — battle-tested 15-strategy repair chain with two-pass orchestrator.

## Install

```bash
pnpm add @arcanada/output-guard

# or
npm install @arcanada/output-guard

# or
yarn add @arcanada/output-guard
```

## Quick start

```typescript
import { repair, OutputGuard } from '@arcanada/output-guard';
import { z } from 'zod';

const User = z.object({
  name: z.string(),
  age: z.number(),
});

// Functional API — format-only repair, no schema
const result = repair('{"name":"Alice","age":30,}', 'json');

console.log(result.data);              // { name: 'Alice', age: 30 }
console.log(result.repaired);          // true
console.log(result.pass);              // "A"
console.log(result.strategiesApplied); // ["fix-commas"]
```

## Stateful API (with schema validation)

```typescript
import { OutputGuard } from '@arcanada/output-guard';

const guard = new OutputGuard({ format: 'json', schema: User });
const result = guard.repair('```json\n{"name":"Bob","age":25}\n```');
// throws if schema mismatch; returns RepairResult<User> on success
```

## Output format support

- **JSON** — strict and relaxed parsing with common error recovery
- **YAML** — with structural repair for indentation and missing keys
- **TOML** — fixing malformed tables and value assignments
- **Python literal** — parsing `dict`/`list` literals with safe eval
- **Auto-detect** — set `format: 'auto'` to infer format from content

## `RepairResult` semantics

```typescript
interface RepairResult<T> {
  repaired: boolean;          // false when raw was already valid
  data?: T;                   // parsed + (optionally) schema-validated payload
  raw: string;                // original input as supplied
  strategiesApplied: string[]; // ordered list of repair strategies invoked
  pass: "A" | "B";            // "A" = combined-apply; "B" = isolating fallback
}
```

`MAX_RETRIES` exhaustion signals via thrown `ParseError`, not via a `pass` value.

## Async wrapper for LLM calls

```typescript
import { guardedGenerate } from '@arcanada/output-guard';
import { z } from 'zod';

const result = await guardedGenerate({
  generate: async (prompt) => callYourLLM(prompt),  // your LLM client
  prompt: 'Return JSON {"result": <integer>}',
  schema: z.object({ result: z.number() }),
  format: 'json',
  maxRetries: 3,
});

console.log(result.data);              // { result: 42 }
console.log(result.pass);              // "A" | "B"
console.log(result.strategiesApplied); // [] when raw was already valid
```

## Error handling

- **`ValidationError`** — schema validation failure
- **`RepairExhaustedError`** — all repair strategies exhausted
- **`FormatError`** — unsupported or unparseable format

## Requirements

Node >= 18 (recommended 20+)

## Documentation

Full API reference and guides: [docs/](https://github.com/Arcanada-one/output-guard/tree/main/packages/ts/docs) (Diataxis structure).  
Source: [packages/ts](https://github.com/Arcanada-one/output-guard/tree/main/packages/ts)

## License

MIT — see [LICENSE](https://github.com/Arcanada-one/output-guard/tree/main/LICENSE)

---

Жизнь одного человека имеет значение / One human life matters