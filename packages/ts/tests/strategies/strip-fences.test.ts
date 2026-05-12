import { describe, expect, it } from "vitest";
import { stripFences } from "../../src/strategies/strip-fences.js";

describe("strip-fences", () => {
  it("strips ```json fences", () => {
    expect(stripFences('```json\n{"a": 1}\n```')).toBe('{"a": 1}');
  });

  it("strips ``` unlabelled fences", () => {
    expect(stripFences('```\n{"a": 1}\n```')).toBe('{"a": 1}');
  });

  it("strips ```yaml fences", () => {
    expect(stripFences("```yaml\na: 1\n```")).toBe("a: 1");
  });

  it("strips ```toml fences", () => {
    expect(stripFences("```toml\n[t]\nk=1\n```")).toBe("[t]\nk=1");
  });

  it("handles whitespace after closing fence", () => {
    expect(stripFences("```json\n{\"a\":1}\n```  ")).toBe('{"a":1}');
  });

  // Idempotent
  it("is idempotent when already stripped", () => {
    const s = '{"a": 1}';
    expect(stripFences(stripFences(s))).toBe(stripFences(s));
  });

  it("is idempotent on already-stripped JSON", () => {
    const s = "{}";
    expect(stripFences(stripFences(s))).toBe(s);
  });

  // No-op on clean
  it("no-op on plain JSON", () => {
    const s = '{"a": 1}';
    expect(stripFences(s)).toBe(s);
  });

  it("no-op on empty string", () => {
    expect(stripFences("")).toBe("");
  });

  it("no-op on plain YAML without fences", () => {
    const s = "a: 1\nb: 2";
    expect(stripFences(s)).toBe(s);
  });
});
