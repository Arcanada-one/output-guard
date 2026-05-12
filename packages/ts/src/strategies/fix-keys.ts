/**
 * fix-keys: Quote bare (unquoted) object keys.
 * Must-isolate: runs after fix-quotes.
 * Handles simple identifiers only — does not attempt to re-parse.
 */
export const fixKeys = (text: string): string => {
  // Match: start of object value — a bare identifier followed by colon
  // Negative lookbehind: not already in a string context (simplified heuristic)
  // Pattern: word chars at start of key position (after { , or newline)
  return text.replace(
    /([{,\n\r]\s*)([A-Za-z_$][\w$]*)(\s*):/g,
    (_, prefix: string, key: string, space: string) =>
      `${prefix}"${key}"${space}:`,
  );
};
