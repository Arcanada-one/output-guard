/**
 * remove-comments: Strip // line comments, /* block comments *\/, and # line comments
 * from JSON-like text. String-aware: does not strip inside quoted strings.
 * Runs before structural strategies.
 */
export const removeComments = (text: string): string => {
  let result = "";
  let i = 0;
  let inString = false;
  let escaped = false;

  while (i < text.length) {
    const ch = text[i];
    if (escaped) {
      result += ch;
      escaped = false;
      i++;
      continue;
    }
    if (inString) {
      if (ch === "\\") { escaped = true; result += ch; i++; continue; }
      if (ch === '"') inString = false;
      result += ch;
      i++;
      continue;
    }
    // Not in string
    if (ch === '"') { inString = true; result += ch; i++; continue; }
    // // comment
    if (ch === "/" && text[i + 1] === "/") {
      while (i < text.length && text[i] !== "\n") i++;
      continue;
    }
    // /* comment */
    if (ch === "/" && text[i + 1] === "*") {
      i += 2;
      while (i < text.length && !(text[i] === "*" && text[i + 1] === "/")) i++;
      i += 2;
      continue;
    }
    // # comment (only at start of token, not inside strings)
    if (ch === "#") {
      while (i < text.length && text[i] !== "\n") i++;
      continue;
    }
    result += ch;
    i++;
  }
  return result;
};
