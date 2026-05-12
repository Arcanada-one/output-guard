/**
 * fix-newlines: Replace literal newlines inside JSON string values with escaped \n.
 * Must run LAST (after all other structural repairs).
 */
export const fixNewlines = (text: string): string => {
  let result = "";
  let inString = false;
  let i = 0;

  while (i < text.length) {
    const ch = text[i];
    if (!inString) {
      if (ch === '"') inString = true;
      result += ch;
      i++;
      continue;
    }
    // Inside string
    if (ch === "\\") {
      // Consume escape pair
      result += ch;
      i++;
      if (i < text.length) { result += text[i]; i++; }
      continue;
    }
    if (ch === '"') {
      inString = false;
      result += ch;
      i++;
      continue;
    }
    if (ch === "\n") {
      result += "\\n";
      i++;
      continue;
    }
    if (ch === "\r") {
      result += "\\r";
      i++;
      continue;
    }
    result += ch;
    i++;
  }
  return result;
};
