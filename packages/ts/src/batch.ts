/**
 * batch: Light array-map wrappers over validate and repair.
 */
import type { Format, RepairResult, ValidationResult } from "./results.js";
import { validate, repair } from "./orchestrator.js";

type SchemaValidator<T = unknown> = (data: unknown) => ValidationResult<T>;

export const validateBatch = <T = unknown>(
  items: string[],
  format: Format = "auto",
  schema?: SchemaValidator<T>,
): ValidationResult<T>[] => items.map((item) => validate<T>(item, format, schema));

export const repairBatch = <T = unknown>(
  items: string[],
  format: Format = "auto",
  schema?: SchemaValidator<T>,
): Array<RepairResult<T> | { error: string }> =>
  items.map((item) => {
    try {
      return repair<T>(item, format, schema);
    } catch (e) {
      return { error: String(e) };
    }
  });
