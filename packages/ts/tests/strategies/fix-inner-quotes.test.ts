import { describe, expect, it } from "vitest";
import { fixInnerQuotes } from "../../src/strategies/fix-inner-quotes.js";

describe("fix-inner-quotes", () => {
  it("escapes unescaped quote inside string value", () => {
    // {"a": " "hello" "} → {"a": " \"hello\" "}
    expect(fixInnerQuotes('{"a": " "hello" "}')).toBe('{"a": " \\"hello\\" "}');
  });

  it("leaves already-escaped quotes intact", () => {
    const s = '{"a": "say \\"hi\\""}';
    expect(fixInnerQuotes(s)).toBe(s);
  });

  it("handles empty string value", () => {
    const s = '{"a": ""}';
    expect(fixInnerQuotes(s)).toBe(s);
  });

  it("preserves structural quotes", () => {
    const s = '{"a": 1, "b": "text"}';
    expect(fixInnerQuotes(s)).toBe(s);
  });

  it("handles nested structure without inner quotes", () => {
    const s = '{"a": {"b": "c"}}';
    expect(fixInnerQuotes(s)).toBe(s);
  });

  // Idempotent
  it("is idempotent on inner-quote input", () => {
    const s = '{"a": " "hello" "}';
    expect(fixInnerQuotes(fixInnerQuotes(s))).toBe(fixInnerQuotes(s));
  });

  it("is idempotent on clean JSON", () => {
    const s = '{"a": "hello world"}';
    expect(fixInnerQuotes(fixInnerQuotes(s))).toBe(s);
  });

  // No-op on clean
  it("no-op on clean JSON", () => {
    const s = '{"a": "hello", "b": 1}';
    expect(fixInnerQuotes(s)).toBe(s);
  });

  it("no-op on empty object", () => {
    expect(fixInnerQuotes("{}")).toBe("{}");
  });

  it("no-op on array of strings", () => {
    const s = '["a", "b", "c"]';
    expect(fixInnerQuotes(s)).toBe(s);
  });
});
