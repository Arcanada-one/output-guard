/**
 * python-literal format: mini-chain to parse Python dict/list literals.
 * Pipeline: None→null, True→true, False→false, single→double quotes, then JSON.parse.
 */
import { ParseError } from "../errors.js";

const toPythonJson = (text: string): string => {
  return text
    .replace(/\bNone\b/g, "null")
    .replace(/\bTrue\b/g, "true")
    .replace(/\bFalse\b/g, "false")
    // single-quoted keys/values → double
    .replace(/'([^'\\]*(\\.[^'\\]*)*)'/g, '"$1"')
    // trailing commas
    .replace(/,(\s*[}\]])/g, "$1");
};

export const parsePythonLiteral = (text: string): unknown => {
  const converted = toPythonJson(text.trim());
  try {
    return JSON.parse(converted);
  } catch (e) {
    throw new ParseError(`python-literal parse failed: ${String(e)}`, e);
  }
};
