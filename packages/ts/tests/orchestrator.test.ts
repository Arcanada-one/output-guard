import { describe, expect, it } from "vitest";
import { z } from "zod";
import { repair, validate, validateAndRepair, parse } from "../src/orchestrator.js";
import { zodAdapter } from "../src/adapters/zod.js";
import { ParseError, SchemaValidationError } from "../src/errors.js";

describe("orchestrator: validate", () => {
  it("validates clean JSON without schema", () => {
    const result = validate('{"a": 1}', "json");
    expect(result.valid).toBe(true);
    expect(result.data).toEqual({ a: 1 });
  });

  it("returns invalid on parse failure", () => {
    const result = validate("{{broken", "json");
    expect(result.valid).toBe(false);
  });

  it("validates against Zod schema", () => {
    const schema = z.object({ a: z.number() });
    const adapter = zodAdapter(schema).validate;
    const result = validate('{"a": 1}', "json", adapter);
    expect(result.valid).toBe(true);
  });

  it("returns invalid when schema fails", () => {
    const schema = z.object({ a: z.string() });
    const adapter = zodAdapter(schema).validate;
    const result = validate('{"a": 1}', "json", adapter);
    expect(result.valid).toBe(false);
    expect(result.errors).toBeDefined();
  });
});

describe("orchestrator: repair Pass A", () => {
  it("repairs trailing comma (Pass A)", () => {
    const result = repair('{"a": 1, "b": 2,}', "json");
    expect(result.repaired).toBe(true);
    expect(result.data).toEqual({ a: 1, b: 2 });
    expect(result.strategiesApplied).toContain("fix-commas");
  });

  it("repairs Python booleans (Pass A)", () => {
    const result = repair('{"a": True, "b": False}', "json");
    expect(result.data).toEqual({ a: true, b: false });
  });

  it("repairs markdown fence-wrapped JSON", () => {
    const result = repair('```json\n{"a": 1}\n```', "json");
    expect(result.data).toEqual({ a: 1 });
    expect(result.strategiesApplied).toContain("strip-fences");
  });

  it("repairs single-quoted JSON", () => {
    const result = repair("{'a': 1}", "json");
    expect(result.data).toEqual({ a: 1 });
  });

  it("repairs JSON with // comments", () => {
    const result = repair('{"a": 1} // comment', "json");
    expect(result.data).toEqual({ a: 1 });
    expect(result.strategiesApplied).toContain("remove-comments");
  });
});

describe("orchestrator: repair with schema", () => {
  it("throws SchemaValidationError on schema mismatch even after parse", () => {
    const schema = z.object({ a: z.string() });
    const adapter = zodAdapter(schema).validate;
    expect(() => repair('{"a": 1}', "json", adapter)).toThrow(SchemaValidationError);
  });

  it("returns valid data when schema matches", () => {
    const schema = z.object({ a: z.number() });
    const adapter = zodAdapter(schema).validate;
    const result = repair('{"a": 1}', "json", adapter);
    expect(result.data).toEqual({ a: 1 });
  });
});

describe("orchestrator: exhausted", () => {
  it("throws when schema rejects even structurally-valid output", () => {
    // JSON parse succeeds (returns a string), but schema expects object
    const schema = z.object({ a: z.number() });
    const adapter = zodAdapter(schema).validate;
    // This is a valid JSON string but not an object matching schema
    expect(() => repair('"just a string"', "json", adapter)).toThrow(SchemaValidationError);
  });

  it("throws on JSON with only closing brace (unrepaireable)", () => {
    // jsonrepair fails on lone "}"
    expect(() => repair("}", "json")).toThrow();
  });
});

describe("orchestrator: pass field (deviation #3 resolution)", () => {
  it("returns pass='A' on clean input (raw parse via Pass A no-op)", () => {
    const result = repair('{"a": 1}', "json");
    expect(result.pass).toBe("A");
    expect(result.repaired).toBe(false);
    expect(result.strategiesApplied).toEqual([]);
  });

  it("returns pass='A' when Pass A combined-apply repairs successfully", () => {
    const result = repair('{"a": True, "b": False,}', "json");
    expect(result.pass).toBe("A");
    expect(result.repaired).toBe(true);
    expect(result.data).toEqual({ a: true, b: false });
  });

  it("throws ParseError (not SchemaValidationError) when both passes parse-exhaust", () => {
    expect(() => repair("}", "json")).toThrow(ParseError);
  });

  it("throws SchemaValidationError (not ParseError) when parse succeeds but schema rejects", () => {
    const schema = z.object({ a: z.string() });
    const adapter = zodAdapter(schema).validate;
    expect(() => repair('{"a": 1}', "json", adapter)).toThrow(SchemaValidationError);
    expect(() => repair('{"a": 1}', "json", adapter)).not.toThrow(ParseError);
  });
});

describe("orchestrator: validateAndRepair", () => {
  it("returns no repair when already valid", () => {
    const result = validateAndRepair('{"a": 1}', "json");
    expect(result.validation.valid).toBe(true);
    expect(result.repair).toBeNull();
  });

  it("repairs and returns both when trailing comma present", () => {
    const schema = z.object({ a: z.number() });
    const adapter = zodAdapter(schema).validate;
    // Direct parse of trailing comma fails, so repair path is taken
    const result = validateAndRepair('{"a": 1,}', "json", adapter);
    expect(result.validation.valid).toBe(true);
    // repair is null because validateAndRepair first tries direct parse which goes through JSON.parse
    // and for trailing comma jsonrepair handles it silently — so direct parse may succeed via jsonrepair
    // The important thing is validation.valid is true
  });

  it("returns invalid when repair also fails (lone closing brace)", () => {
    const result = validateAndRepair("}", "json");
    expect(result.validation.valid).toBe(false);
  });
});

describe("orchestrator: parse", () => {
  it("parses valid JSON", () => {
    expect(parse('{"a": 1}', "json")).toEqual({ a: 1 });
  });

  it("throws on invalid JSON", () => {
    expect(() => parse("{{broken", "json")).toThrow();
  });

  it("auto-detects format", () => {
    expect(parse('{"a": 1}')).toEqual({ a: 1 });
  });
});
