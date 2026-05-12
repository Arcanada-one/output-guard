import { describe, expect, it } from "vitest";
import { parseJson, repairJson } from "../../src/formats/json.js";

describe("format: json", () => {
  it("parses valid JSON", () => {
    expect(parseJson('{"a": 1}')).toEqual({ a: 1 });
  });

  it("parses JSON array", () => {
    expect(parseJson("[1, 2, 3]")).toEqual([1, 2, 3]);
  });

  it("uses jsonrepair on trailing comma", () => {
    expect(parseJson('{"a": 1,}')).toEqual({ a: 1 });
  });

  it("uses jsonrepair on single-quoted keys", () => {
    expect(parseJson("{'a': 1}")).toEqual({ a: 1 });
  });

  it("throws ParseError on lone closing brace (truly unrepaireable)", () => {
    // jsonrepair cannot repair a lone closing brace
    expect(() => parseJson("}")).toThrow();
  });

  it("repairJson returns repaired string", () => {
    expect(JSON.parse(repairJson('{"a": 1,}'))).toEqual({ a: 1 });
  });

  it("repairJson handles single-quoted", () => {
    expect(JSON.parse(repairJson("{'a': 1}"))).toEqual({ a: 1 });
  });
});
