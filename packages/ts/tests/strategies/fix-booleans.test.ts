import { describe, expect, it } from "vitest";
import { fixBooleans } from "../../src/strategies/fix-booleans.js";

describe("fix-booleans", () => {
  it("replaces True with true", () => {
    expect(fixBooleans('{"a": True}')).toBe('{"a": true}');
  });

  it("replaces False with false", () => {
    expect(fixBooleans('{"a": False}')).toBe('{"a": false}');
  });

  it("replaces None with null", () => {
    expect(fixBooleans('{"a": None}')).toBe('{"a": null}');
  });

  it("replaces all Python booleans in one pass", () => {
    expect(fixBooleans('{"a": True, "b": False, "c": None}')).toBe(
      '{"a": true, "b": false, "c": null}',
    );
  });

  it("uses word boundaries — does not replace partial words", () => {
    // 'Truecolor' should not become 'truecolor'
    expect(fixBooleans('{"color": "Truecolor"}')).toBe('{"color": "Truecolor"}');
  });

  // Idempotent
  it("is idempotent", () => {
    const s = '{"a": True}';
    expect(fixBooleans(fixBooleans(s))).toBe(fixBooleans(s));
  });

  it("is idempotent on clean", () => {
    const s = '{"a": true}';
    expect(fixBooleans(fixBooleans(s))).toBe(s);
  });

  // No-op on clean
  it("no-op on valid JSON booleans", () => {
    const s = '{"a": true, "b": false, "c": null}';
    expect(fixBooleans(s)).toBe(s);
  });

  it("no-op on empty object", () => {
    expect(fixBooleans("{}")).toBe("{}");
  });

  it("no-op on numbers and strings", () => {
    const s = '{"a": 1, "b": "hello"}';
    expect(fixBooleans(s)).toBe(s);
  });
});
