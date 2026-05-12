/**
 * Two-pass orchestrator (creative-CONN-0087).
 *
 * Pass A: apply all 15 strategies in CANONICAL_ORDER, then parse once.
 * Pass B: for each strategy individually, apply → parse. First success wins.
 * If both passes fail → pass: "exhausted".
 *
 * MANDATORY (F1): even syntactically-valid output is schema-validated.
 * Throws SchemaValidationError if schema validation fails after parse.
 */
import type { Format, RepairResult, ValidationResult } from "./results.js";
import { SchemaValidationError } from "./errors.js";
import { CANONICAL_ORDER } from "./strategies/index.js";
import { parseJson } from "./formats/json.js";
import { parseYaml } from "./formats/yaml.js";
import { parseToml } from "./formats/toml.js";
import { parsePythonLiteral } from "./formats/python-literal.js";
import { detectFormat } from "./formats/detect.js";

type SchemaValidator<T = unknown> = (data: unknown) => ValidationResult<T>;

/** Resolve format, auto-detecting if needed. */
const resolveFormat = (text: string, format: Format): Exclude<Format, "auto"> =>
  format === "auto" ? detectFormat(text) : format;

/** Attempt to parse text in the given format. Returns parsed value or null on failure. */
const tryParse = (text: string, format: Exclude<Format, "auto">): unknown | null => {
  try {
    switch (format) {
      case "json":   return parseJson(text);
      case "yaml":   return parseYaml(text);
      case "toml":   return parseToml(text);
      case "python": return parsePythonLiteral(text);
    }
  } catch {
    return null;
  }
};

/** Run schema validation if validator is provided. Throws SchemaValidationError on failure. */
const runSchema = <T>(data: unknown, schema?: SchemaValidator<T>): T => {
  if (!schema) return data as T;
  const result = schema(data);
  if (!result.valid) {
    throw new SchemaValidationError(
      `Schema validation failed: ${result.errors?.join("; ") ?? "unknown"}`,
      result.errors ?? [],
    );
  }
  return result.data as T;
};

/** Pass A: apply all strategies in order, then parse once. */
const passA = (
  text: string,
  format: Exclude<Format, "auto">,
): { text: string; applied: string[] } | null => {
  let current = text;
  const applied: string[] = [];
  for (const { name, fn } of CANONICAL_ORDER) {
    const next = fn(current);
    if (next !== current) applied.push(name);
    current = next;
  }
  const parsed = tryParse(current, format);
  if (parsed !== null) return { text: current, applied };
  return null;
};

/** Pass B: try each strategy individually, parse after each. */
const passB = (
  text: string,
  format: Exclude<Format, "auto">,
): { text: string; applied: string[] } | null => {
  for (const { name, fn } of CANONICAL_ORDER) {
    const candidate = fn(text);
    if (candidate === text) continue;
    const parsed = tryParse(candidate, format);
    if (parsed !== null) return { text: candidate, applied: [name] };
  }
  return null;
};

/**
 * Core two-pass repair chain.
 * Returns RepairResult. Throws SchemaValidationError if schema rejects.
 */
export const repair = <T = unknown>(
  text: string,
  format: Format = "auto",
  schema?: SchemaValidator<T>,
): RepairResult<T> => {
  const fmt = resolveFormat(text, format);

  // Try pass A
  const aResult = passA(text, fmt);
  if (aResult !== null) {
    const parsed = tryParse(aResult.text, fmt);
    const validated = runSchema<T>(parsed, schema);
    return {
      repaired: aResult.applied.length > 0,
      data: validated,
      raw: aResult.text,
      strategiesApplied: aResult.applied,
    };
  }

  // Try pass B
  const bResult = passB(text, fmt);
  if (bResult !== null) {
    const parsed = tryParse(bResult.text, fmt);
    const validated = runSchema<T>(parsed, schema);
    return {
      repaired: true,
      data: validated,
      raw: bResult.text,
      strategiesApplied: bResult.applied,
    };
  }

  // Exhausted — try raw parse as last resort
  const rawParsed = tryParse(text, fmt);
  if (rawParsed !== null) {
    const validated = runSchema<T>(rawParsed, schema);
    return {
      repaired: false,
      data: validated,
      raw: text,
      strategiesApplied: [],
    };
  }

  throw new SchemaValidationError("Both passes exhausted: could not parse or repair input", []);
};

/** Validate without repair attempt — just parse + schema. */
export const validate = <T = unknown>(
  text: string,
  format: Format = "auto",
  schema?: SchemaValidator<T>,
): ValidationResult<T> => {
  const fmt = resolveFormat(text, format);
  const parsed = tryParse(text, fmt);
  if (parsed === null) {
    return { valid: false, errors: ["Parse failed"] };
  }
  if (!schema) {
    return { valid: true, data: parsed as T };
  }
  return schema(parsed);
};

/** Validate + repair in one call. Returns validation result with repair info. */
export const validateAndRepair = <T = unknown>(
  text: string,
  format: Format = "auto",
  schema?: SchemaValidator<T>,
): { validation: ValidationResult<T>; repair: RepairResult<T> | null } => {
  const fmt = resolveFormat(text, format);
  const directParse = tryParse(text, fmt);
  if (directParse !== null) {
    const vResult: ValidationResult<T> = schema
      ? schema(directParse)
      : { valid: true as const, data: directParse as T };
    if (vResult.valid) {
      return {
        validation: vResult,
        repair: null,
      };
    }
  }
  // Attempt repair
  try {
    const repairResult = repair<T>(text, format, schema);
    const validation: ValidationResult<T> =
      repairResult.data !== undefined
        ? { valid: true as const, data: repairResult.data }
        : { valid: false as const, errors: ["Repair produced no data"] };
    return {
      validation,
      repair: repairResult,
    };
  } catch (e) {
    return {
      validation: { valid: false, errors: [String(e)] },
      repair: null,
    };
  }
};

/** Parse raw text in given format (throws on failure). */
export const parse = (text: string, format: Format = "auto"): unknown => {
  const fmt = resolveFormat(text, format);
  const result = tryParse(text, fmt);
  if (result === null) {
    throw new SchemaValidationError(`Failed to parse as ${fmt}`, []);
  }
  return result;
};

/** Build a retry prompt embedding previous response and errors. */
export { retryPrompt } from "./retry-prompt.js";
