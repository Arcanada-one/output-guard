/**
 * fix-inner-quotes: Escape unescaped double-quote characters inside JSON string values.
 * Must-isolate: runs after fix-quotes.
 * Scans the text char-by-char tracking string context.
 */
export const fixInnerQuotes = (text: string): string => {
  let result = "";
  let inString = false;
  let i = 0;

  while (i < text.length) {
    const ch = text[i];
    if (!inString) {
      if (ch === '"') {
        inString = true;
        result += ch;
        i++;
        continue;
      }
      result += ch;
      i++;
      continue;
    }
    // Inside a string
    if (ch === "\\") {
      // Consume escape sequence as-is
      result += ch;
      i++;
      if (i < text.length) {
        result += text[i];
        i++;
      }
      continue;
    }
    if (ch === '"') {
      // Check if this quote closes the string or is embedded
      // Heuristic: if next non-whitespace char is : , } ] then it closes
      let j = i + 1;
      while (j < text.length && (text[j] === " " || text[j] === "\t")) j++;
      const next = text[j];
      const isCloser =
        next === ":" ||
        next === "," ||
        next === "}" ||
        next === "]" ||
        next === undefined ||
        j >= text.length;
      if (isCloser) {
        inString = false;
        result += ch;
      } else {
        result += '\\"';
      }
      i++;
      continue;
    }
    result += ch;
    i++;
  }
  return result;
};
