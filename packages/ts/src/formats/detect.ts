/**
 * detect format: heuristic detection of input format.
 * Priority: TOML (key=val pattern), YAML (leading ---), JSON ({ or [), python-literal.
 */
import type { Format } from "../results.js";

export const detectFormat = (text: string): Exclude<Format, "auto"> => {
  const trimmed = text.trimStart();

  // TOML: starts with [section] header or key=val
  if (/^\[[\w.]+\]/.test(trimmed) || /^[\w-]+\s*=\s*/.test(trimmed)) {
    return "toml";
  }

  // YAML: starts with --- or key: value (but not { or [)
  if (
    trimmed.startsWith("---") ||
    (/^[\w-]+\s*:\s*/.test(trimmed) && !trimmed.startsWith("{"))
  ) {
    return "yaml";
  }

  // JSON: starts with { or [
  if (trimmed.startsWith("{") || trimmed.startsWith("[")) {
    return "json";
  }

  // Python literal: starts with { or [ after pythonic keywords
  if (trimmed.startsWith("(") || /\bTrue\b|\bFalse\b|\bNone\b/.test(trimmed)) {
    return "python";
  }

  return "json";
};
