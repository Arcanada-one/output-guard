import { describe, expect, it } from "vitest";
import { z } from "zod";
import { validateBatch, repairBatch } from "../src/batch.js";
import { zodAdapter } from "../src/adapters/zod.js";

describe("batch", () => {
  it("validateBatch returns valid results for clean inputs", () => {
    const results = validateBatch(['{"a": 1}', '{"b": 2}'], "json");
    expect(results.every((r) => r.valid)).toBe(true);
  });

  it("validateBatch returns invalid for bad input", () => {
    const results = validateBatch(["}"], "json");
    expect(results[0]?.valid).toBe(false);
  });

  it("validateBatch applies schema", () => {
    const schema = z.object({ a: z.number() });
    const adapter = zodAdapter(schema).validate;
    const results = validateBatch(['{"a": 1}', '{"a": "wrong"}'], "json", adapter);
    expect(results[0]?.valid).toBe(true);
    expect(results[1]?.valid).toBe(false);
  });

  it("repairBatch repairs all inputs", () => {
    const results = repairBatch(['{"a": 1,}', '{"b": 2,}'], "json");
    expect(results).toHaveLength(2);
    const r0 = results[0];
    if (r0 && "data" in r0) {
      expect(r0.data).toEqual({ a: 1 });
    }
  });

  it("repairBatch returns error object for unrecoverable input", () => {
    const results = repairBatch(["}"], "json");
    const r0 = results[0];
    expect(r0).toHaveProperty("error");
  });

  it("repairBatch handles empty array", () => {
    expect(repairBatch([], "json")).toEqual([]);
  });

  it("validateBatch handles empty array", () => {
    expect(validateBatch([], "json")).toEqual([]);
  });
});
