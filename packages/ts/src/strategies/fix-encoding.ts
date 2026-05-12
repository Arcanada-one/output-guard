/**
 * fix-encoding: Replace BOM, token-splitter Unicode surrogates, and
 * the most common GPT tokeniser artefacts (Ċ = Ċ → \n, Ġ = Ġ → space).
 * Runs FIRST — before all other strategies.
 */
export const fixEncoding = (text: string): string => {
  let result = text;
  // BOM
  if (result.charCodeAt(0) === 0xfeff) {
    result = result.slice(1);
  }
  // GPT tokeniser artefacts: Ċ (Ċ) → newline, Ġ (Ġ) → space
  result = result.replace(/Ċ/g, "\n").replace(/Ġ/g, " ");
  // Lone surrogates → replacement character
  result = result.replace(/[\uD800-\uDFFF]/g, "�");
  return result;
};
