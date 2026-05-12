/**
 * fix-commas: Remove trailing commas before } and ].
 * Must-isolate: applied before fix-keys. Runs before fix-keys.
 */
export const fixCommas = (text: string): string => {
  // Remove trailing comma before } or ] accounting for optional whitespace/newlines
  return text.replace(/,(\s*[}\]])/g, "$1");
};
