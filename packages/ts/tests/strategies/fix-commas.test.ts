import { describe, expect, it } from "vitest";
import { fixCommas } from "../../src/strategies/fix-commas.js";

describe("fix-commas", () => {
  it("removes trailing comma before }", () => {
    expect(fixCommas('{"a": 1, "b": 2,}')).toBe('{"a": 1, "b": 2}');
  });

  it("removes trailing comma before ]", () => {
    expect(fixCommas("[1, 2, 3,]")).toBe("[1, 2, 3]");
  });

  it("removes trailing comma with whitespace", () => {
    expect(fixCommas('{"a": 1,  }')).toBe('{"a": 1  }');
  });

  it("removes trailing comma with newline", () => {
    expect(fixCommas('{"a": 1,\n}')).toBe('{"a": 1\n}');
  });

  it("removes multiple trailing commas in nested", () => {
    expect(fixCommas('{"a": [1, 2,], "b": 3,}')).toBe('{"a": [1, 2], "b": 3}');
  });

  // Idempotent
  it("is idempotent", () => {
    const s = '{"a": 1,}';
    expect(fixCommas(fixCommas(s))).toBe(fixCommas(s));
  });

  it("is idempotent on clean", () => {
    const s = '{"a": 1}';
    expect(fixCommas(fixCommas(s))).toBe(s);
  });

  // No-op on clean
  it("no-op on clean JSON", () => {
    const s = '{"a": 1, "b": 2}';
    expect(fixCommas(s)).toBe(s);
  });

  it("no-op on array without trailing comma", () => {
    const s = "[1, 2, 3]";
    expect(fixCommas(s)).toBe(s);
  });

  it("no-op on empty object", () => {
    expect(fixCommas("{}")).toBe("{}");
  });
});
