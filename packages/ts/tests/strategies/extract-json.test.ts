import { describe, expect, it } from "vitest";
import { extractJson } from "../../src/strategies/extract-json.js";

describe("extract-json", () => {
  it("extracts JSON object from surrounding text", () => {
    expect(extractJson('Sure! Here\'s: {"a": 1} Let me know!')).toBe('{"a": 1}');
  });

  it("extracts JSON array from surrounding text", () => {
    expect(extractJson("Result: [1, 2, 3] done.")).toBe("[1, 2, 3]");
  });

  it("extracts nested object", () => {
    expect(extractJson('prefix {"a": {"b": 2}} suffix')).toBe('{"a": {"b": 2}}');
  });

  it("no-op when text already starts with {", () => {
    const s = '{"a": 1}';
    expect(extractJson(s)).toBe(s);
  });

  it("no-op when text already starts with [", () => {
    const s = "[1, 2]";
    expect(extractJson(s)).toBe(s);
  });

  // Idempotent
  it("is idempotent", () => {
    const s = 'prefix {"x": 1} suffix';
    expect(extractJson(extractJson(s))).toBe(extractJson(s));
  });

  it("is idempotent when no JSON found", () => {
    const s = "no json here";
    expect(extractJson(extractJson(s))).toBe(s);
  });

  // No-op on clean
  it("no-op on pure JSON object", () => {
    const s = '{"key": "value"}';
    expect(extractJson(s)).toBe(s);
  });

  it("no-op on pure JSON array", () => {
    const s = '["a", "b"]';
    expect(extractJson(s)).toBe(s);
  });

  it("returns original when no JSON found", () => {
    const s = "plain text without braces";
    expect(extractJson(s)).toBe(s);
  });
});
