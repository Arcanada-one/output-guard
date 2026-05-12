import { describe, expect, it } from "vitest";
import { fixUnicode } from "../../src/strategies/fix-unicode.js";

describe("fix-unicode", () => {
  it("replaces \\u with fewer than 4 hex digits with \\uFFFD", () => {
    const result = fixUnicode('{"a": "\\u00"}');
    expect(result).toBe('{"a": "\\uFFFD"}');
  });

  it("replaces short \\u0 escape with \\uFFFD", () => {
    const result = fixUnicode('{"a": "\\u0"}');
    expect(result).toBe('{"a": "\\uFFFD"}');
  });

  it("leaves valid \\uXXXX intact", () => {
    const s = '{"a": "\\u0041"}'; // A = A
    expect(fixUnicode(s)).toBe(s);
  });

  it("leaves \\u4e2d (CJK) intact", () => {
    const s = '{"a": "\\u4e2d"}';
    expect(fixUnicode(s)).toBe(s);
  });

  it("handles empty string", () => {
    expect(fixUnicode("")).toBe("");
  });

  // Idempotent
  it("is idempotent on broken escape", () => {
    const s = '{"a": "\\u00"}';
    expect(fixUnicode(fixUnicode(s))).toBe(fixUnicode(s));
  });

  it("is idempotent on valid escape", () => {
    const s = '{"a": "\\u0041"}';
    expect(fixUnicode(fixUnicode(s))).toBe(s);
  });

  // No-op on clean
  it("no-op on clean JSON without unicode escapes", () => {
    const s = '{"a": "hello"}';
    expect(fixUnicode(s)).toBe(s);
  });

  it("no-op on complete valid unicode escape \\uFFFF", () => {
    const s = '{"a": "\\uFFFF"}';
    expect(fixUnicode(s)).toBe(s);
  });

  it("no-op on numbers", () => {
    const s = '{"a": 42}';
    expect(fixUnicode(s)).toBe(s);
  });
});
