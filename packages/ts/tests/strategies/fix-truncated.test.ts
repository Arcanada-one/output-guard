import { describe, expect, it } from "vitest";
import { fixTruncated } from "../../src/strategies/fix-truncated.js";

describe("fix-truncated", () => {
  it("removes trailing ellipsis ...", () => {
    expect(fixTruncated('{"a": 1, "b": "hel...')).toBe('{"a": 1, "b": "hel"');
  });

  it("removes trailing Unicode ellipsis …", () => {
    expect(fixTruncated('{"items": [1, 2…')).toBe('{"items": [1, 2');
  });

  it("removes trailing dangling comma", () => {
    expect(fixTruncated('{"a": 1,')).toBe('{"a": 1');
  });

  it("closes unterminated string", () => {
    expect(fixTruncated('{"a": "hello')).toBe('{"a": "hello"');
  });

  it("does not add quote when string already closed", () => {
    expect(fixTruncated('{"a": "hello"')).toBe('{"a": "hello"');
  });

  // Idempotent
  it("is idempotent on truncated", () => {
    const s = '{"a": 1, "b": "hel...';
    expect(fixTruncated(fixTruncated(s))).toBe(fixTruncated(s));
  });

  it("is idempotent on clean", () => {
    const s = '{"a": 1}';
    expect(fixTruncated(fixTruncated(s))).toBe(s);
  });

  // No-op on clean
  it("no-op on complete JSON", () => {
    const s = '{"a": 1, "b": "hello"}';
    expect(fixTruncated(s)).toBe(s);
  });

  it("no-op on empty object", () => {
    expect(fixTruncated("{}")).toBe("{}");
  });

  it("no-op on array", () => {
    const s = "[1, 2, 3]";
    expect(fixTruncated(s)).toBe(s);
  });
});
