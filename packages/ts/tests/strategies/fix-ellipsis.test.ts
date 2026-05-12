import { describe, expect, it } from "vitest";
import { fixEllipsis } from "../../src/strategies/fix-ellipsis.js";

describe("fix-ellipsis", () => {
  it("removes trailing ... before ]", () => {
    expect(fixEllipsis('{"items": [1, 2, ...]}')).toBe('{"items": [1, 2]}');
  });

  it("removes trailing … before ]", () => {
    expect(fixEllipsis('{"items": [1, 2, …]}')).toBe('{"items": [1, 2]}');
  });

  it("removes trailing ... before }", () => {
    expect(fixEllipsis('{"a": 1, ...}')).toBe('{"a": 1}');
  });

  it("replaces [...] shorthand", () => {
    expect(fixEllipsis("[...]")).toBe("[]");
  });

  it("replaces [… ] shorthand", () => {
    expect(fixEllipsis("[…]")).toBe("[]");
  });

  // Idempotent
  it("is idempotent", () => {
    const s = '{"items": [1, 2, ...]}';
    expect(fixEllipsis(fixEllipsis(s))).toBe(fixEllipsis(s));
  });

  it("is idempotent on clean", () => {
    const s = '{"items": [1, 2]}';
    expect(fixEllipsis(fixEllipsis(s))).toBe(s);
  });

  // No-op on clean
  it("no-op on clean array", () => {
    const s = "[1, 2, 3]";
    expect(fixEllipsis(s)).toBe(s);
  });

  it("no-op on clean object", () => {
    const s = '{"a": 1}';
    expect(fixEllipsis(s)).toBe(s);
  });

  it("no-op on empty array", () => {
    expect(fixEllipsis("[]")).toBe("[]");
  });
});
