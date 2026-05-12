import { describe, expect, it } from "vitest";
import { fixClosers } from "../../src/strategies/fix-closers.js";

describe("fix-closers", () => {
  it("closes missing }", () => {
    expect(fixClosers('{"a": 1')).toBe('{"a": 1}');
  });

  it("closes missing ]", () => {
    expect(fixClosers("[1, 2, 3")).toBe("[1, 2, 3]");
  });

  it("closes nested missing closers", () => {
    expect(fixClosers('{"a": [1, 2, 3')).toBe('{"a": [1, 2, 3]}');
  });

  it("closes multiple missing closers", () => {
    expect(fixClosers('{"a": {"b": 1')).toBe('{"a": {"b": 1}}');
  });

  it("handles already balanced JSON", () => {
    const s = '{"a": [1, 2, 3]}';
    expect(fixClosers(s)).toBe(s);
  });

  // Idempotent
  it("is idempotent on unbalanced", () => {
    const s = '{"a": 1';
    expect(fixClosers(fixClosers(s))).toBe(fixClosers(s));
  });

  it("is idempotent on balanced", () => {
    const s = '{"a": 1}';
    expect(fixClosers(fixClosers(s))).toBe(s);
  });

  // No-op on clean
  it("no-op on complete JSON", () => {
    const s = '{"a": 1, "b": [1, 2]}';
    expect(fixClosers(s)).toBe(s);
  });

  it("no-op on empty object", () => {
    expect(fixClosers("{}")).toBe("{}");
  });

  it("no-op on empty array", () => {
    expect(fixClosers("[]")).toBe("[]");
  });
});
