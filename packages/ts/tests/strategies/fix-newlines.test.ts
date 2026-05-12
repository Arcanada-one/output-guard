import { describe, expect, it } from "vitest";
import { fixNewlines } from "../../src/strategies/fix-newlines.js";

describe("fix-newlines", () => {
  it("escapes literal newline inside string value", () => {
    expect(fixNewlines('{"a": "line1\nline2"}')).toBe('{"a": "line1\\nline2"}');
  });

  it("escapes literal carriage return inside string", () => {
    expect(fixNewlines('{"a": "line1\rline2"}')).toBe('{"a": "line1\\rline2"}');
  });

  it("escapes newline in multi-key object", () => {
    expect(fixNewlines('{"a": "x\ny", "b": 1}')).toBe('{"a": "x\\ny", "b": 1}');
  });

  it("does not escape newlines outside strings", () => {
    const s = '{\n"a": 1\n}';
    expect(fixNewlines(s)).toBe(s);
  });

  it("preserves already-escaped newlines", () => {
    const s = '{"a": "line1\\nline2"}';
    expect(fixNewlines(s)).toBe(s);
  });

  // Idempotent
  it("is idempotent on string with literal newline", () => {
    const s = '{"a": "line1\nline2"}';
    expect(fixNewlines(fixNewlines(s))).toBe(fixNewlines(s));
  });

  it("is idempotent on clean JSON", () => {
    const s = '{"a": "hello"}';
    expect(fixNewlines(fixNewlines(s))).toBe(s);
  });

  // No-op on clean
  it("no-op on clean JSON", () => {
    const s = '{"a": "hello world"}';
    expect(fixNewlines(s)).toBe(s);
  });

  it("no-op on JSON with structural newlines only", () => {
    const s = '{\n"a": 1,\n"b": 2\n}';
    expect(fixNewlines(s)).toBe(s);
  });

  it("no-op on empty string", () => {
    expect(fixNewlines("")).toBe("");
  });
});
