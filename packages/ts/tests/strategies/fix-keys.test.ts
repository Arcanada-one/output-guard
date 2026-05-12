import { describe, expect, it } from "vitest";
import { fixKeys } from "../../src/strategies/fix-keys.js";

describe("fix-keys", () => {
  it("quotes bare keys in object", () => {
    expect(fixKeys("{a: 1, b: 2}")).toBe('{"a": 1, "b": 2}');
  });

  it("quotes underscore-prefixed keys", () => {
    expect(fixKeys("{_id: 123}")).toBe('{"_id": 123}');
  });

  it("quotes camelCase keys", () => {
    const result = fixKeys("{myKey: 'value'}");
    expect(result).toBe('{"myKey": \'value\'}');
  });

  it("handles multiple unquoted keys on same line", () => {
    const r = fixKeys("{a: 1, b: 2, c: 3}");
    expect(r).toBe('{"a": 1, "b": 2, "c": 3}');
  });

  it("does not double-quote already quoted keys", () => {
    const s = '{"a": 1}';
    expect(fixKeys(s)).toBe(s);
  });

  // Idempotent
  it("is idempotent", () => {
    const s = "{a: 1}";
    expect(fixKeys(fixKeys(s))).toBe(fixKeys(s));
  });

  it("is idempotent on already-quoted", () => {
    const s = '{"a": 1}';
    expect(fixKeys(fixKeys(s))).toBe(s);
  });

  // No-op on clean
  it("no-op on clean JSON", () => {
    const s = '{"a": 1, "b": "hello"}';
    expect(fixKeys(s)).toBe(s);
  });

  it("no-op on empty object", () => {
    expect(fixKeys("{}")).toBe("{}");
  });

  it("no-op on array", () => {
    const s = "[1, 2, 3]";
    expect(fixKeys(s)).toBe(s);
  });
});
