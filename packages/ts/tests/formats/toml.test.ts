import { describe, expect, it } from "vitest";
import { parseToml } from "../../src/formats/toml.js";

describe("format: toml", () => {
  it("parses simple TOML key=val", () => {
    expect(parseToml('title = "hello"')).toEqual({ title: "hello" });
  });

  it("parses TOML section", () => {
    expect(parseToml("[section]\nkey = 1")).toEqual({ section: { key: 1 } });
  });

  it("parses TOML integers", () => {
    expect(parseToml("count = 42")).toEqual({ count: 42 });
  });

  it("throws ParseError on invalid TOML", () => {
    expect(() => parseToml("{{invalid}}")).toThrow();
  });

  it("parses TOML booleans", () => {
    expect(parseToml("a = true\nb = false")).toEqual({ a: true, b: false });
  });
});
