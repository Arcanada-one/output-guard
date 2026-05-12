import { describe, expect, it } from "vitest";
import { fixEncoding } from "../../src/strategies/fix-encoding.js";

describe("fix-encoding", () => {
  // Positive cases
  it("removes BOM from start", () => {
    expect(fixEncoding("﻿{\"a\":1}")).toBe("{\"a\":1}");
  });

  it("replaces GPT tokeniser Ċ artefact with newline", () => {
    expect(fixEncoding("Ċ{ĊĠ\"a\":Ġ1Ċ}")).toBe("\n{\n \"a\": 1\n}");
  });

  it("replaces Ġ artefact with space", () => {
    expect(fixEncoding("Ġhello")).toBe(" hello");
  });

  it("replaces lone surrogate with replacement char", () => {
    expect(fixEncoding("\uD800")).toBe("�");
  });

  it("replaces trailing lone surrogate", () => {
    expect(fixEncoding("hello\uDFFF")).toBe("hello�");
  });

  // Idempotent
  it("is idempotent on normal JSON", () => {
    const s = '{"a": 1, "b": "hello"}';
    expect(fixEncoding(fixEncoding(s))).toBe(fixEncoding(s));
  });

  it("is idempotent on already-clean artefact-free text", () => {
    const s = '{"x": true}';
    expect(fixEncoding(fixEncoding(s))).toBe(s);
  });

  // No-op on clean
  it("no-op on plain JSON", () => {
    const s = '{"a": 1}';
    expect(fixEncoding(s)).toBe(s);
  });

  it("no-op on empty string", () => {
    expect(fixEncoding("")).toBe("");
  });

  it("no-op on ASCII text", () => {
    const s = "hello world";
    expect(fixEncoding(s)).toBe(s);
  });
});
