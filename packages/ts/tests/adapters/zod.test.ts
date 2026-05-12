import { describe, expect, it } from "vitest";
import { z } from "zod";
import { zodAdapter } from "../../src/adapters/zod.js";

describe("adapters/zod", () => {
  it("returns valid=true for matching data", () => {
    const adapter = zodAdapter(z.object({ a: z.number() }));
    expect(adapter.validate({ a: 1 })).toEqual({ valid: true, data: { a: 1 } });
  });

  it("returns valid=false for type mismatch", () => {
    const adapter = zodAdapter(z.object({ a: z.string() }));
    const result = adapter.validate({ a: 1 });
    expect(result.valid).toBe(false);
    expect(result.errors).toBeDefined();
    expect(result.errors?.length).toBeGreaterThan(0);
  });

  it("returns errors with path info for missing required field", () => {
    const adapter = zodAdapter(z.object({ name: z.string() }));
    const result = adapter.validate({});
    expect(result.valid).toBe(false);
    expect(result.errors?.some((e) => e.includes("name"))).toBe(true);
  });

  it("returns valid for nested object match", () => {
    const adapter = zodAdapter(z.object({ user: z.object({ id: z.number() }) }));
    expect(adapter.validate({ user: { id: 42 } })).toMatchObject({ valid: true });
  });

  it("validates array schema", () => {
    const adapter = zodAdapter(z.array(z.string()));
    expect(adapter.validate(["a", "b"])).toMatchObject({ valid: true });
  });

  it("rejects array mismatch", () => {
    const adapter = zodAdapter(z.array(z.string()));
    const result = adapter.validate([1, 2]);
    expect(result.valid).toBe(false);
  });

  it("validates optional fields", () => {
    const adapter = zodAdapter(z.object({ a: z.number(), b: z.string().optional() }));
    expect(adapter.validate({ a: 1 })).toMatchObject({ valid: true });
  });

  it("returns error message from Zod issue", () => {
    const adapter = zodAdapter(z.object({ x: z.number().min(10) }));
    const result = adapter.validate({ x: 1 });
    expect(result.valid).toBe(false);
    expect(result.errors?.join("")).toContain("x");
  });
});
