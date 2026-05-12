/**
 * toml format: parse TOML via `smol-toml`.
 */
import { parse as tomlParse } from "smol-toml";
import { ParseError } from "../errors.js";

export const parseToml = (text: string): unknown => {
  try {
    return tomlParse(text) as unknown;
  } catch (e) {
    throw new ParseError(`TOML parse failed: ${String(e)}`, e);
  }
};
