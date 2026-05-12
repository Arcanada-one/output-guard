/**
 * fix-truncated: Repair truncated JSON by removing trailing incomplete tokens
 * (partial strings, dangling commas, partial keys).
 * Must-isolate: runs before fix-closers.
 */
export const fixTruncated = (text: string): string => {
  let result = text.trimEnd();

  // Remove trailing ellipsis (... or …) that indicate truncation
  result = result.replace(/[…]{1}$/, "").trimEnd();
  result = result.replace(/\.{3}$/, "").trimEnd();

  // Remove trailing comma at end
  result = result.replace(/,\s*$/, "").trimEnd();

  // If last char is inside an unterminated string, try to close it
  // Detect: text ends without matching closing " after last "
  const lastQuoteIdx = result.lastIndexOf('"');
  if (lastQuoteIdx !== -1) {
    // Count non-escaped quotes
    let quoteCount = 0;
    let i = 0;
    while (i < result.length) {
      if (result[i] === "\\") { i += 2; continue; }
      if (result[i] === '"') quoteCount++;
      i++;
    }
    // Odd number of quotes → last string is unterminated
    if (quoteCount % 2 === 1) {
      result = result + '"';
    }
  }

  return result;
};
