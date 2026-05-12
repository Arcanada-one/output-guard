/**
 * strip-fences: Remove markdown code fences wrapping JSON/YAML/TOML/etc.
 * Handles ```json, ```yaml, ```toml, ``` (unlabelled).
 * Runs before extract-json.
 */
export const stripFences = (text: string): string => {
  const trimmed = text.trim();
  const match = /^```[\w-]*\r?\n([\s\S]*?)\r?\n```\s*$/i.exec(trimmed);
  if (match?.[1] !== undefined) {
    return match[1].trim();
  }
  // Inline fence without trailing newline before closing ```
  const inlineMatch = /^```[\w-]*\r?\n([\s\S]*?)```\s*$/i.exec(trimmed);
  if (inlineMatch?.[1] !== undefined) {
    return inlineMatch[1].trim();
  }
  return text;
};
