/**
 * fix-quotes: Replace single-quoted keys/values and Unicode smart quotes with ASCII double quotes.
 * Must-isolate: runs before fix-keys and fix-inner-quotes.
 */

const SMART_OPEN = /[‘‛‹]/g;   // ' ‛ ‹
const SMART_CLOSE = /[’›]/g;         // ' ›
const SMART_DQUOTE = /[“”„‟«»]/g; // " " „ ‟ « »

export const fixQuotes = (text: string): string => {
  let result = text;
  // Replace smart quotes
  result = result
    .replace(SMART_OPEN, "'")
    .replace(SMART_CLOSE, "'")
    .replace(SMART_DQUOTE, '"');

  // Convert single-quoted strings to double-quoted.
  // Walk char by char to handle escapes correctly.
  let out = "";
  let i = 0;
  while (i < result.length) {
    const ch = result[i];
    if (ch === "'") {
      // Collect single-quoted token
      out += '"';
      i++;
      while (i < result.length) {
        const c = result[i];
        if (c === "\\") {
          const next = result[i + 1];
          if (next === "'") {
            // \' inside single-quoted string → plain ' (no backslash needed in double-quoted)
            out += "'";
            i += 2;
            continue;
          }
          // Other escape sequences: pass through
          out += result[i] ?? "";
          i++;
          out += result[i] ?? "";
          i++;
          continue;
        }
        if (c === "'") { out += '"'; i++; break; }
        if (c === '"') { out += '\\"'; i++; continue; }
        out += c;
        i++;
      }
    } else {
      out += ch;
      i++;
    }
  }
  return out;
};
