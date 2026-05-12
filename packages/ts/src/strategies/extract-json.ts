/**
 * extract-json: Extract the first balanced JSON object or array from surrounding text.
 * Runs after strip-fences.
 */
export const extractJson = (text: string): string => {
  const t = text.trim();
  // If it already starts with { or [, skip
  if (t.startsWith("{") || t.startsWith("[")) {
    return text;
  }
  // Find first { or [
  const objIdx = t.indexOf("{");
  const arrIdx = t.indexOf("[");
  let startIdx = -1;
  let openChar: "{" | "[" = "{";
  let closeChar: "}" | "]" = "}";

  if (objIdx === -1 && arrIdx === -1) return text;
  if (objIdx === -1) { startIdx = arrIdx; openChar = "["; closeChar = "]"; }
  else if (arrIdx === -1) { startIdx = objIdx; }
  else if (arrIdx < objIdx) { startIdx = arrIdx; openChar = "["; closeChar = "]"; }
  else { startIdx = objIdx; }

  let depth = 0;
  let inString = false;
  let escaped = false;
  for (let i = startIdx; i < t.length; i++) {
    const ch = t[i];
    if (escaped) { escaped = false; continue; }
    if (ch === "\\") { escaped = true; continue; }
    if (ch === '"') { inString = !inString; continue; }
    if (inString) continue;
    if (ch === openChar) depth++;
    else if (ch === closeChar) {
      depth--;
      if (depth === 0) {
        return t.slice(startIdx, i + 1);
      }
    }
  }
  return text;
};
