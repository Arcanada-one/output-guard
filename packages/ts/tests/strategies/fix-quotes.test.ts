import { describe, expect, it } from "vitest";
import { fixQuotes } from "../../src/strategies/fix-quotes.js";

describe("fix-quotes", () => {
  it("converts single-quoted object to double-quoted", () => {
    expect(fixQuotes("{'a': 'hello'}")).toBe('{"a": "hello"}');
  });

  it("replaces smart open/close double quotes", () => {
    expect(fixQuotes('“”')).toBe('""');
  });

  it("replaces left/right single smart quotes", () => {
    // U+2018 U+2019
    expect(fixQuotes("‘hello’")).toBe('"hello"');
  });

  it("handles single-quoted value containing escaped apostrophe", () => {
    // Input: {'key': 'it\'s'} — escaped apostrophe inside single-quoted string
    // After conversion: {"key": "it's"} — backslash-apostrophe → just apostrophe
    const result = fixQuotes("{'key': 'it\\'s'}");
    // The escape sequence \' in single-quoted string maps to just ' in the double-quoted string
    expect(result).toBe('{"key": "it\'s"}');
  });

  it("converts mixed single-double in nested structure", () => {
    const input = "{'a': {'b': 'c'}}";
    const output = fixQuotes(input);
    expect(JSON.parse(output)).toEqual({ a: { b: "c" } });
  });

  // Idempotent
  it("is idempotent on single-quoted input", () => {
    const s = "{'a': 1}";
    expect(fixQuotes(fixQuotes(s))).toBe(fixQuotes(s));
  });

  it("is idempotent on double-quoted input", () => {
    const s = '{"a": 1}';
    expect(fixQuotes(fixQuotes(s))).toBe(s);
  });

  // No-op on clean
  it("no-op on clean double-quoted JSON", () => {
    const s = '{"a": "hello"}';
    expect(fixQuotes(s)).toBe(s);
  });

  it("no-op on empty string", () => {
    expect(fixQuotes("")).toBe("");
  });

  it("no-op on number values", () => {
    const s = '{"a": 1, "b": 2}';
    expect(fixQuotes(s)).toBe(s);
  });
});
