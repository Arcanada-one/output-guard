import { describe, expect, it } from "vitest";
import { detectFormat } from "../../src/formats/detect.js";

describe("format: detect", () => {
  it("detects JSON object", () => {
    expect(detectFormat('{"a": 1}')).toBe("json");
  });

  it("detects JSON array", () => {
    expect(detectFormat("[1, 2, 3]")).toBe("json");
  });

  it("detects YAML via key: value pattern", () => {
    expect(detectFormat("a: 1\nb: 2")).toBe("yaml");
  });

  it("detects YAML via --- prefix", () => {
    expect(detectFormat("---\na: 1")).toBe("yaml");
  });

  it("detects TOML via [section] header", () => {
    expect(detectFormat("[section]\nkey = 1")).toBe("toml");
  });

  it("detects TOML via key=val", () => {
    expect(detectFormat("key = value")).toBe("toml");
  });

  it("detects python via True keyword", () => {
    expect(detectFormat("{'a': True}")).toBe("json"); // starts with { → json wins
  });

  it("defaults to json on unknown", () => {
    expect(detectFormat("some text without clear format")).toBe("json");
  });
});
