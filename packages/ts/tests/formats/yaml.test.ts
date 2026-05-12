import { describe, expect, it } from "vitest";
import { parseYaml } from "../../src/formats/yaml.js";

describe("format: yaml", () => {
  it("parses valid YAML", () => {
    expect(parseYaml("a: 1\nb: hello")).toEqual({ a: 1, b: "hello" });
  });

  it("parses YAML list", () => {
    expect(parseYaml("- 1\n- 2\n- 3")).toEqual([1, 2, 3]);
  });

  it("parses YAML with nested keys", () => {
    expect(parseYaml("outer:\n  inner: value")).toEqual({ outer: { inner: "value" } });
  });

  it("throws ParseError on invalid YAML", () => {
    expect(() => parseYaml("key: [unclosed")).toThrow();
  });

  it("parses YAML boolean values", () => {
    expect(parseYaml("a: true\nb: false")).toEqual({ a: true, b: false });
  });
});
