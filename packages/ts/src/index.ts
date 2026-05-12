// Public API barrel for @arcanada/output-guard
// M1 bootstrap: types + constants only. Implementation lands in M2 (CONN-0087).

export { MAX_RETRIES, RETRY_BACKOFF_MS, FORMAT_DEFAULT } from "./constants.js";
export type {
  Format,
  Strategy,
  ValidationResult,
  RepairResult,
  RepairReport,
  GuardedGenerateResult,
} from "./results.js";
export {
  ParseError,
  SchemaValidationError,
  GuardedGenerationError,
  RepairError,
} from "./errors.js";
