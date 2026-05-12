/**
 * fix-values: Replace bare non-standard values (NaN, Infinity, -Infinity, undefined)
 * with null. Safe strategy, no ordering constraint.
 */
export const fixValues = (text: string): string => {
  return text
    .replace(/:\s*-Infinity\b/g, ": null")
    .replace(/:\s*Infinity\b/g, ": null")
    .replace(/:\s*NaN\b/g, ": null")
    .replace(/:\s*undefined\b/g, ": null");
};
