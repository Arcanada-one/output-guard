/**
 * json format: parse JSON, falling back to jsonrepair on syntax error.
 */
import { jsonrepair } from "jsonrepair";
import { ParseError } from "../errors.js";

export const parseJson = (text: string): unknown => {
  try {
    return JSON.parse(text);
  } catch {
    // fallback: try jsonrepair
    try {
      const repaired = jsonrepair(text);
      return JSON.parse(repaired);
    } catch (e) {
      throw new ParseError(`JSON parse failed: ${String(e)}`, e);
    }
  }
};

export const repairJson = (text: string): string => {
  try {
    return jsonrepair(text);
  } catch (e) {
    throw new ParseError(`jsonrepair failed: ${String(e)}`, e);
  }
};
