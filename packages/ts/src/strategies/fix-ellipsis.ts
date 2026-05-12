/**
 * fix-ellipsis: Remove placeholder ellipsis (...) from arrays and objects.
 * e.g. [1, 2, ...] → [1, 2]
 * Safe strategy; runs before fix-closers.
 */
export const fixEllipsis = (text: string): string => {
  // Remove , ... or , … inside arrays/objects
  return text
    .replace(/,\s*\.\.\.\s*(?=[}\]])/g, "")
    .replace(/,\s*…\s*(?=[}\]])/g, "")
    // Also handle [..., ...] where ... is the only element
    .replace(/\[\s*\.\.\.\s*\]/g, "[]")
    .replace(/\[\s*…\s*\]/g, "[]");
};
