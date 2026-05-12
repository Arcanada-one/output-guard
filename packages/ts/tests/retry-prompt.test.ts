import { describe, expect, it } from "vitest";
import { retryPrompt } from "../src/retry-prompt.js";

describe("retryPrompt", () => {
  it("includes previous response in prompt", () => {
    const result = retryPrompt({ previousResponse: '{"a": bad}' });
    expect(result.prompt).toContain('{"a": bad}');
  });

  it("includes errors in prompt", () => {
    const result = retryPrompt({
      previousResponse: "...",
      errors: ["Unexpected token", "/field: required"],
    });
    expect(result.prompt).toContain("Unexpected token");
    expect(result.detectedErrors).toHaveLength(2);
  });

  it("extracts JSON pointer paths from errors", () => {
    const result = retryPrompt({
      previousResponse: "...",
      errors: ["/name: required", "/age: Expected number"],
    });
    expect(result.pointerPaths).toContain("/name");
    expect(result.pointerPaths).toContain("/age");
  });

  it("includes schema when provided", () => {
    const result = retryPrompt({
      previousResponse: "...",
      schema: '{ "type": "object" }',
    });
    expect(result.prompt).toContain("Expected schema");
  });

  it("includes history when provided", () => {
    const result = retryPrompt({
      previousResponse: "...",
      history: [{ role: "user", content: "first message" }],
    });
    expect(result.prompt).toContain("first message");
  });

  it("returns empty pointerPaths when no errors", () => {
    const result = retryPrompt({ previousResponse: "ok" });
    expect(result.pointerPaths).toEqual([]);
    expect(result.detectedErrors).toEqual([]);
  });
});
