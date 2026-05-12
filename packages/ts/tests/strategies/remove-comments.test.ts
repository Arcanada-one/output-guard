import { describe, expect, it } from "vitest";
import { removeComments } from "../../src/strategies/remove-comments.js";

describe("remove-comments", () => {
  it("removes // line comments", () => {
    expect(removeComments('{"a": 1} // comment')).toBe('{"a": 1} ');
  });

  it("removes # line comments", () => {
    expect(removeComments('{"a": 1} # comment')).toBe('{"a": 1} ');
  });

  it("removes /* block comments */", () => {
    expect(removeComments('{"a": /* hidden */ 1}')).toBe('{"a":  1}');
  });

  it("does not remove // inside strings", () => {
    const s = '{"url": "http://example.com"}';
    expect(removeComments(s)).toBe(s);
  });

  it("removes multiline /* */ comments", () => {
    expect(removeComments('{"a": 1\n/* multi\nline */\n}')).toBe('{"a": 1\n\n}');
  });

  // Idempotent
  it("is idempotent", () => {
    const s = '{"a": 1} // x';
    expect(removeComments(removeComments(s))).toBe(removeComments(s));
  });

  it("is idempotent on already-clean", () => {
    const s = '{"x": "y"}';
    expect(removeComments(removeComments(s))).toBe(s);
  });

  // No-op on clean
  it("no-op on clean JSON", () => {
    const s = '{"a": 1, "b": 2}';
    expect(removeComments(s)).toBe(s);
  });

  it("no-op on empty string", () => {
    expect(removeComments("")).toBe("");
  });

  it("preserves content inside strings", () => {
    const s = '{"msg": "hello // world"}';
    expect(removeComments(s)).toBe(s);
  });
});
