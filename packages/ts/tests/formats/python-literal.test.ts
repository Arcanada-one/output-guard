import { describe, expect, it } from "vitest";
import { parsePythonLiteral } from "../../src/formats/python-literal.js";

describe("format: python-literal", () => {
  it("parses Python dict with True/False/None", () => {
    expect(parsePythonLiteral("{'a': True, 'b': False, 'c': None}")).toEqual({
      a: true,
      b: false,
      c: null,
    });
  });

  it("parses single-quoted strings", () => {
    expect(parsePythonLiteral("{'key': 'value'}")).toEqual({ key: "value" });
  });

  it("removes trailing commas", () => {
    expect(parsePythonLiteral("{'a': 1,}")).toEqual({ a: 1 });
  });

  it("parses nested dicts", () => {
    expect(parsePythonLiteral("{'a': {'b': 2}}")).toEqual({ a: { b: 2 } });
  });

  it("throws ParseError on unrecoverable input", () => {
    expect(() => parsePythonLiteral("not a dict at all!!!")).toThrow();
  });
});
