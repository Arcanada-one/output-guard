/**
 * Strategy barrel + CANONICAL_ORDER definition.
 * The order matches the two-pass orchestrator spec:
 * 1 fix-encoding → 2 strip-fences → 3 extract-json → 4 remove-comments →
 * 5 fix-commas → 6 fix-quotes → 7 fix-keys → 8 fix-values → 9 fix-booleans →
 * 10 fix-truncated → 11 fix-ellipsis → 12 fix-unicode → 13 fix-inner-quotes →
 * 14 fix-closers → 15 fix-newlines
 */
import type { Strategy } from "../results.js";

export { fixEncoding } from "./fix-encoding.js";
export { stripFences } from "./strip-fences.js";
export { extractJson } from "./extract-json.js";
export { removeComments } from "./remove-comments.js";
export { fixCommas } from "./fix-commas.js";
export { fixQuotes } from "./fix-quotes.js";
export { fixKeys } from "./fix-keys.js";
export { fixValues } from "./fix-values.js";
export { fixBooleans } from "./fix-booleans.js";
export { fixTruncated } from "./fix-truncated.js";
export { fixEllipsis } from "./fix-ellipsis.js";
export { fixUnicode } from "./fix-unicode.js";
export { fixInnerQuotes } from "./fix-inner-quotes.js";
export { fixClosers } from "./fix-closers.js";
export { fixNewlines } from "./fix-newlines.js";

import { fixEncoding } from "./fix-encoding.js";
import { stripFences } from "./strip-fences.js";
import { extractJson } from "./extract-json.js";
import { removeComments } from "./remove-comments.js";
import { fixCommas } from "./fix-commas.js";
import { fixQuotes } from "./fix-quotes.js";
import { fixKeys } from "./fix-keys.js";
import { fixValues } from "./fix-values.js";
import { fixBooleans } from "./fix-booleans.js";
import { fixTruncated } from "./fix-truncated.js";
import { fixEllipsis } from "./fix-ellipsis.js";
import { fixUnicode } from "./fix-unicode.js";
import { fixInnerQuotes } from "./fix-inner-quotes.js";
import { fixClosers } from "./fix-closers.js";
import { fixNewlines } from "./fix-newlines.js";

/** Strategy names for reporting (index-aligned with CANONICAL_ORDER). */
export const STRATEGY_NAMES = [
  "fix-encoding",
  "strip-fences",
  "extract-json",
  "remove-comments",
  "fix-commas",
  "fix-quotes",
  "fix-keys",
  "fix-values",
  "fix-booleans",
  "fix-truncated",
  "fix-ellipsis",
  "fix-unicode",
  "fix-inner-quotes",
  "fix-closers",
  "fix-newlines",
] as const;

export type StrategyName = (typeof STRATEGY_NAMES)[number];

export const CANONICAL_ORDER: ReadonlyArray<{ name: StrategyName; fn: Strategy }> = [
  { name: "fix-encoding",     fn: fixEncoding },
  { name: "strip-fences",     fn: stripFences },
  { name: "extract-json",     fn: extractJson },
  { name: "remove-comments",  fn: removeComments },
  { name: "fix-commas",       fn: fixCommas },
  { name: "fix-quotes",       fn: fixQuotes },
  { name: "fix-keys",         fn: fixKeys },
  { name: "fix-values",       fn: fixValues },
  { name: "fix-booleans",     fn: fixBooleans },
  { name: "fix-truncated",    fn: fixTruncated },
  { name: "fix-ellipsis",     fn: fixEllipsis },
  { name: "fix-unicode",      fn: fixUnicode },
  { name: "fix-inner-quotes", fn: fixInnerQuotes },
  { name: "fix-closers",      fn: fixClosers },
  { name: "fix-newlines",     fn: fixNewlines },
] as const;
