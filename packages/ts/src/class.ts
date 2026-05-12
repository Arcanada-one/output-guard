/**
 * OutputGuard: Stateful class wrapper around the functional API.
 * Stores format, schema, maxRetries defaults.
 */
import type { ZodType } from "zod";
import type { Format, GuardedGenerateResult, RepairResult, ValidationResult } from "./results.js";
import { validate, repair } from "./orchestrator.js";
import { guardedGenerate } from "./guarded-generate.js";
import type { GuardedGenerateOptions, Message } from "./guarded-generate.js";
import { zodAdapter } from "./adapters/zod.js";

export interface OutputGuardOptions<T = unknown> {
  format?: Format;
  schema?: ZodType<T>;
  maxRetries?: number;
  timeoutMs?: number;
}

export class OutputGuard<T = unknown> {
  private readonly format: Format;
  private readonly schema: ZodType<T> | undefined;
  private readonly maxRetries: number;
  private readonly timeoutMs: number;

  constructor(opts: OutputGuardOptions<T> = {}) {
    this.format = opts.format ?? "auto";
    this.schema = opts.schema !== undefined ? opts.schema : undefined;
    this.maxRetries = opts.maxRetries ?? 3;
    this.timeoutMs = opts.timeoutMs ?? 30_000;
  }

  validate(text: string): ValidationResult<T> {
    const validator = this.schema ? zodAdapter(this.schema).validate : undefined;
    return validate<T>(text, this.format, validator);
  }

  repair(text: string): RepairResult<T> {
    const validator = this.schema ? zodAdapter(this.schema).validate : undefined;
    return repair<T>(text, this.format, validator);
  }

  async guarded(
    generate: (prompt: string, history?: Message[]) => Promise<string>,
    prompt: string,
    opts?: Partial<Omit<GuardedGenerateOptions<T>, "generate" | "prompt">>,
  ): Promise<GuardedGenerateResult<T>> {
    const resolvedSchema = opts?.schema !== undefined ? opts.schema : this.schema;
    const base: GuardedGenerateOptions<T> = {
      generate,
      prompt,
      format: opts?.format ?? this.format,
      maxRetries: opts?.maxRetries ?? this.maxRetries,
      timeoutMs: opts?.timeoutMs ?? this.timeoutMs,
    };
    if (resolvedSchema !== undefined) base.schema = resolvedSchema;
    if (opts?.signal !== undefined) base.signal = opts.signal;
    return guardedGenerate<T>(base);
  }
}
