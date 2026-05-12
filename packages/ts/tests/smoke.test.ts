import { describe, expect, it } from "vitest";
import { MAX_RETRIES, FORMAT_DEFAULT } from "../src/index.js";
import { ParseError, SchemaValidationError } from "../src/index.js";

describe("M1 bootstrap smoke", () => {
  it("MAX_RETRIES is 3 (mirrored in Python constants.py)", () => {
    expect(MAX_RETRIES).toBe(3);
  });

  it("FORMAT_DEFAULT is auto", () => {
    expect(FORMAT_DEFAULT).toBe("auto");
  });

  it("ParseError carries cause", () => {
    const cause = new Error("boom");
    const err = new ParseError("wrap", cause);
    expect(err.name).toBe("ParseError");
    expect(err.cause).toBe(cause);
  });

  it("SchemaValidationError carries issues", () => {
    const err = new SchemaValidationError("nope", ["/x: required"]);
    expect(err.issues).toEqual(["/x: required"]);
  });
});
