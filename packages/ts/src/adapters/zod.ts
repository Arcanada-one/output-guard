/**
 * Zod adapter: wraps a ZodType schema into the library's SchemaValidator interface.
 */
import type { ZodType } from "zod";
import type { ValidationResult } from "../results.js";

export interface SchemaAdapter<T = unknown> {
  validate: (data: unknown) => ValidationResult<T>;
}

export const zodAdapter = <T>(schema: ZodType<T>): SchemaAdapter<T> => ({
  validate: (data: unknown): ValidationResult<T> => {
    const result = schema.safeParse(data);
    if (result.success) {
      return { valid: true, data: result.data };
    }
    const errors = result.error.issues.map(
      (issue) => `${issue.path.join("/") || "root"}: ${issue.message}`,
    );
    return { valid: false, errors };
  },
});
