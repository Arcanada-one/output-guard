/**
 * yaml format: parse YAML via the `yaml` package.
 */
import { parse as yamlParse } from "yaml";
import { ParseError } from "../errors.js";

export const parseYaml = (text: string): unknown => {
  try {
    return yamlParse(text) as unknown;
  } catch (e) {
    throw new ParseError(`YAML parse failed: ${String(e)}`, e);
  }
};
