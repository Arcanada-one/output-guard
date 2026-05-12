/**
 * fix-unicode: Sanitize broken Unicode escape sequences (\uXXXX where XXXX
 * is not a valid 4-hex-digit sequence). Replaces invalid escapes with the
 * Unicode replacement character escape �. Safe strategy.
 *
 * Walks char by char to correctly handle string context and existing valid escapes.
 */
export const fixUnicode = (text: string): string => {
  let result = "";
  let i = 0;

  while (i < text.length) {
    // Look for backslash
    if (text[i] === "\\" && i + 1 < text.length) {
      if (text[i + 1] === "u") {
        // Check if followed by exactly 4 hex digits
        const hexSlice = text.slice(i + 2, i + 6);
        if (/^[0-9a-fA-F]{4}$/.test(hexSlice)) {
          // Valid \uXXXX — pass through
          result += text.slice(i, i + 6);
          i += 6;
        } else {
          // Invalid \u sequence — replace with �
          // Count how many hex digits actually follow before a non-hex char
          let hexCount = 0;
          while (hexCount < 4 && /[0-9a-fA-F]/.test(text[i + 2 + hexCount] ?? "")) {
            hexCount++;
          }
          result += "\\uFFFD";
          i += 2 + hexCount; // skip \u + whatever partial hex digits we consumed
        }
        continue;
      }
      // Other escape: pass through
      result += text[i] ?? "";
      result += text[i + 1] ?? "";
      i += 2;
      continue;
    }
    result += text[i] ?? "";
    i++;
  }
  return result;
};
