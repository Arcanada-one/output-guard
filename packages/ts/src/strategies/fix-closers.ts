/**
 * fix-closers: Append missing closing braces/brackets to balance the structure.
 * Must-isolate: runs after fix-truncated and fix-ellipsis.
 */
export const fixClosers = (text: string): string => {
  const stack: string[] = [];
  let inString = false;
  let escaped = false;

  for (const ch of text) {
    if (escaped) { escaped = false; continue; }
    if (ch === "\\" && inString) { escaped = true; continue; }
    if (ch === '"') { inString = !inString; continue; }
    if (inString) continue;
    if (ch === "{") stack.push("}");
    else if (ch === "[") stack.push("]");
    else if (ch === "}" || ch === "]") {
      if (stack[stack.length - 1] === ch) stack.pop();
    }
  }

  // Append all missing closers in reverse
  return text + stack.reverse().join("");
};
