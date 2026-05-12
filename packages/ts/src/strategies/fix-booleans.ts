/**
 * fix-booleans: Replace Python-style booleans (True, False, None) with
 * JSON equivalents (true, false, null). Safe strategy.
 * Uses word boundaries to avoid replacing inside string values.
 */
export const fixBooleans = (text: string): string => {
  return text
    .replace(/\bTrue\b/g, "true")
    .replace(/\bFalse\b/g, "false")
    .replace(/\bNone\b/g, "null");
};
