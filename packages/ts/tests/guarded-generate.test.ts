import { describe, expect, it, vi } from "vitest";
import { z } from "zod";
import { guardedGenerate } from "../src/guarded-generate.js";
import { GuardedGenerationError } from "../src/errors.js";

describe("guardedGenerate", () => {
  it("returns data on first successful attempt", async () => {
    const generate = vi.fn().mockResolvedValue('{"a": 1}');
    const result = await guardedGenerate({ generate, prompt: "give me json" });
    expect(result.data).toEqual({ a: 1 });
    expect(result.report.retries).toBe(0);
    expect(generate).toHaveBeenCalledTimes(1);
  });

  it("retries on schema-invalid output and succeeds", async () => {
    const schema = z.object({ a: z.number() });
    const generate = vi
      .fn()
      .mockResolvedValueOnce('{"a": "wrong type"}') // fails schema
      .mockResolvedValueOnce('{"a": 1}');            // passes schema
    const result = await guardedGenerate({ generate, prompt: "give me json", schema });
    expect(result.data).toEqual({ a: 1 });
    expect(generate).toHaveBeenCalledTimes(2);
  });

  it("throws GuardedGenerationError after MAX_RETRIES exhausted (schema-based)", async () => {
    const schema = z.object({ required: z.string() });
    const generate = vi.fn().mockResolvedValue('{"wrong": "field"}');
    await expect(
      guardedGenerate({ generate, prompt: "give me json", maxRetries: 2, schema }),
    ).rejects.toThrow(GuardedGenerationError);
    expect(generate).toHaveBeenCalledTimes(3); // 1 + 2 retries
  });

  it("throws GuardedGenerationError when AbortSignal is already aborted", async () => {
    const controller = new AbortController();
    controller.abort();
    const generate = vi.fn().mockResolvedValue('{"a": 1}');
    await expect(
      guardedGenerate({ generate, prompt: "test", signal: controller.signal }),
    ).rejects.toThrow(GuardedGenerationError);
    expect(generate).not.toHaveBeenCalled();
  });

  it("validates against Zod schema on success", async () => {
    const schema = z.object({ name: z.string() });
    const generate = vi.fn().mockResolvedValue('{"name": "Alice"}');
    const result = await guardedGenerate({ generate, prompt: "test", schema });
    expect(result.data).toEqual({ name: "Alice" });
  });

  it("retries when schema validation fails", async () => {
    const schema = z.object({ name: z.string() });
    const generate = vi
      .fn()
      .mockResolvedValueOnce('{"name": 42}') // wrong type
      .mockResolvedValueOnce('{"name": "Alice"}');
    const result = await guardedGenerate({ generate, prompt: "test", schema });
    expect(result.data).toEqual({ name: "Alice" });
    expect(generate).toHaveBeenCalledTimes(2);
  });

  it("throws on timeout", async () => {
    const generate = vi.fn().mockImplementation(
      () => new Promise((res) => setTimeout(() => res('{"a":1}'), 1000)),
    );
    await expect(
      guardedGenerate({ generate, prompt: "test", timeoutMs: 10 }),
    ).rejects.toThrow();
  });

  it("report.retries reflects number of retries", async () => {
    const schema = z.object({ x: z.number() });
    const generate = vi
      .fn()
      .mockResolvedValueOnce('{"x": "wrong"}') // fails schema → retry
      .mockResolvedValueOnce('{"x": 1}');       // passes
    const result = await guardedGenerate({ generate, prompt: "t", maxRetries: 3, schema });
    expect(result.report.retries).toBe(1);
  });
});
