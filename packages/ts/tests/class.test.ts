import { describe, expect, it, vi } from "vitest";
import { z } from "zod";
import { OutputGuard } from "../src/class.js";

describe("OutputGuard class", () => {
  it("validate() returns valid for clean JSON", () => {
    const guard = new OutputGuard({ format: "json" });
    const result = guard.validate('{"a": 1}');
    expect(result.valid).toBe(true);
  });

  it("validate() returns invalid for bad JSON", () => {
    const guard = new OutputGuard({ format: "json" });
    const result = guard.validate("}");
    expect(result.valid).toBe(false);
  });

  it("repair() repairs trailing comma", () => {
    const guard = new OutputGuard({ format: "json" });
    const result = guard.repair('{"a": 1,}');
    expect(result.data).toEqual({ a: 1 });
  });

  it("validate() applies Zod schema", () => {
    const schema = z.object({ name: z.string() });
    const guard = new OutputGuard({ format: "json", schema });
    expect(guard.validate('{"name": "Alice"}').valid).toBe(true);
    expect(guard.validate('{"name": 42}').valid).toBe(false);
  });

  it("guarded() resolves with data on first attempt", async () => {
    const schema = z.object({ x: z.number() });
    const guard = new OutputGuard({ format: "json", schema });
    const generate = vi.fn().mockResolvedValue('{"x": 42}');
    const result = await guard.guarded(generate, "give me x");
    expect(result.data).toEqual({ x: 42 });
  });

  it("guarded() retries on schema failure", async () => {
    const schema = z.object({ x: z.number() });
    const guard = new OutputGuard({ format: "json", schema, maxRetries: 3 });
    const generate = vi
      .fn()
      .mockResolvedValueOnce('{"x": "wrong"}')
      .mockResolvedValueOnce('{"x": 1}');
    const result = await guard.guarded(generate, "test");
    expect(result.data).toEqual({ x: 1 });
  });

  it("default format is auto", () => {
    const guard = new OutputGuard();
    const result = guard.validate('{"a": 1}');
    expect(result.valid).toBe(true);
  });

  it("repair() with schema throws on schema mismatch", () => {
    const schema = z.object({ a: z.string() });
    const guard = new OutputGuard({ format: "json", schema });
    expect(() => guard.repair('{"a": 1}')).toThrow();
  });
});
