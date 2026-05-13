// Public API barrel for @arcanada/output-guard

export { MAX_RETRIES, RETRY_BACKOFF_MS, FORMAT_DEFAULT, DEFAULT_TIMEOUT_MS } from "./constants.js";

export type {
  Format,
  Strategy,
  ValidationResult,
  RepairResult,
  RepairReport,
  GuardedGenerateResult,
  OrchestratorPass,
} from "./results.js";

export {
  ParseError,
  SchemaValidationError,
  GuardedGenerationError,
  RepairError,
} from "./errors.js";

// Orchestrator functional API
export { validate, repair, validateAndRepair, parse, retryPrompt } from "./orchestrator.js";

// Generate
export { guardedGenerate } from "./guarded-generate.js";
export type { GuardedGenerateOptions, Message } from "./guarded-generate.js";

// Batch
export { validateBatch, repairBatch } from "./batch.js";

// Class API
export { OutputGuard } from "./class.js";
export type { OutputGuardOptions } from "./class.js";

// Formats
export { detectFormat } from "./formats/detect.js";
export { parseJson, repairJson } from "./formats/json.js";
export { parseYaml } from "./formats/yaml.js";
export { parseToml } from "./formats/toml.js";
export { parsePythonLiteral } from "./formats/python-literal.js";

// Adapters
export { zodAdapter } from "./adapters/zod.js";
export type { SchemaAdapter } from "./adapters/zod.js";

// Strategies
export {
  CANONICAL_ORDER,
  STRATEGY_NAMES,
  fixEncoding,
  stripFences,
  extractJson,
  removeComments,
  fixCommas,
  fixQuotes,
  fixKeys,
  fixValues,
  fixBooleans,
  fixTruncated,
  fixEllipsis,
  fixUnicode,
  fixInnerQuotes,
  fixClosers,
  fixNewlines,
} from "./strategies/index.js";

// Retry prompt types
export type { RetryPromptOptions, RetryPromptResult } from "./retry-prompt.js";
