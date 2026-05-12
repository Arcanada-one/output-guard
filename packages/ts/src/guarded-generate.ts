/**
 * guardedGenerate: Async wrapper that calls a generate function, validates/repairs
 * output, and retries with a correction prompt on failure.
 *
 * F4 compliance: AbortController per-call timeout (default 30s).
 * MAX_RETRIES=3 hard cap.
 */
import type { ZodType } from "zod";
import type { Format, GuardedGenerateResult, RepairReport } from "./results.js";
import { GuardedGenerationError } from "./errors.js";
import { MAX_RETRIES, DEFAULT_TIMEOUT_MS } from "./constants.js";
import { repair } from "./orchestrator.js";
import { retryPrompt } from "./retry-prompt.js";
import { zodAdapter } from "./adapters/zod.js";

export interface Message {
  role: "user" | "assistant" | "system";
  content: string;
}

export interface GuardedGenerateOptions<T> {
  generate: (prompt: string, history?: Message[]) => Promise<string>;
  prompt: string;
  format?: Format;
  schema?: ZodType<T>;
  maxRetries?: number;
  timeoutMs?: number;
  signal?: AbortSignal;
}

const withTimeout = <T>(
  promise: Promise<T>,
  ms: number,
  signal?: AbortSignal,
): Promise<T> => {
  return new Promise<T>((resolve, reject) => {
    if (signal?.aborted) {
      reject(new Error("AbortSignal already aborted"));
      return;
    }
    const timer = setTimeout(() => reject(new Error(`Timeout after ${ms}ms`)), ms);
    const onAbort = () => {
      clearTimeout(timer);
      reject(new Error("Aborted"));
    };
    signal?.addEventListener("abort", onAbort, { once: true });
    promise.then(
      (val) => { clearTimeout(timer); signal?.removeEventListener("abort", onAbort); resolve(val); },
      (err: unknown) => { clearTimeout(timer); signal?.removeEventListener("abort", onAbort); reject(err); },
    );
  });
};

export const guardedGenerate = async <T = unknown>(
  opts: GuardedGenerateOptions<T>,
): Promise<GuardedGenerateResult<T>> => {
  const {
    generate,
    prompt,
    format = "auto",
    schema,
    maxRetries = MAX_RETRIES,
    timeoutMs = DEFAULT_TIMEOUT_MS,
    signal,
  } = opts;

  const validator = schema ? zodAdapter(schema).validate : undefined;
  const history: Message[] = [];
  let lastError: unknown;
  let lastResponse = "";

  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    if (signal?.aborted) {
      throw new GuardedGenerationError("Aborted by signal", attempt, lastError);
    }

    const currentPrompt =
      attempt === 0
        ? prompt
        : retryPrompt({
            previousResponse: lastResponse,
            errors: lastError instanceof Error ? [lastError.message] : [String(lastError)],
            history,
          }).prompt;

    let raw: string;
    try {
      raw = await withTimeout(generate(currentPrompt, history.length > 0 ? history : undefined), timeoutMs, signal);
    } catch (e) {
      throw new GuardedGenerationError(
        `Generation failed on attempt ${attempt}: ${String(e)}`,
        attempt,
        e,
      );
    }

    lastResponse = raw;
    history.push({ role: "user", content: currentPrompt });
    history.push({ role: "assistant", content: raw });

    try {
      const repairResult = repair<T>(raw, format, validator);
      const report: RepairReport = {
        strategiesApplied: repairResult.strategiesApplied,
        retries: attempt,
        finalValid: true,
        pass: repairResult.repaired ? "B" : "A",
      };
      return { data: repairResult.data as T, report };
    } catch (e) {
      lastError = e;
    }
  }

  throw new GuardedGenerationError(
    `Exhausted ${maxRetries} retries without valid output`,
    maxRetries,
    lastError,
  );
};
