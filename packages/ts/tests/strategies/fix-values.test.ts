import { describe, expect, it } from "vitest";
import { fixValues } from "../../src/strategies/fix-values.js";

describe("fix-values", () => {
  it("replaces NaN with null", () => {
    expect(fixValues('{"a": NaN}')).toBe('{"a": null}');
  });

  it("replaces Infinity with null", () => {
    expect(fixValues('{"a": Infinity}')).toBe('{"a": null}');
  });

  it("replaces -Infinity with null", () => {
    expect(fixValues('{"a": -Infinity}')).toBe('{"a": null}');
  });

  it("replaces undefined with null", () => {
    expect(fixValues('{"a": undefined}')).toBe('{"a": null}');
  });

  it("replaces multiple bad values", () => {
    expect(fixValues('{"a": NaN, "b": Infinity, "c": undefined}')).toBe(
      '{"a": null, "b": null, "c": null}',
    );
  });

  // Idempotent
  it("is idempotent", () => {
    const s = '{"a": NaN}';
    expect(fixValues(fixValues(s))).toBe(fixValues(s));
  });

  it("is idempotent on clean", () => {
    const s = '{"a": null}';
    expect(fixValues(fixValues(s))).toBe(s);
  });

  // No-op on clean
  it("no-op on clean JSON", () => {
    const s = '{"a": 1, "b": null}';
    expect(fixValues(s)).toBe(s);
  });

  it("no-op on string containing NaN", () => {
    // NaN inside a string value should NOT be replaced (word boundary helps but regex is after colon)
    const s = '{"msg": "NaN value"}';
    // Note: our regex requires colon before NaN, so this should pass
    expect(fixValues(s)).toBe(s);
  });

  it("no-op on empty object", () => {
    expect(fixValues("{}")).toBe("{}");
  });
});
