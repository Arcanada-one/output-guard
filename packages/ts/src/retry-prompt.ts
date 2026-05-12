/**
 * retry-prompt: Build a correction prompt that embeds the previous LLM response,
 * detected schema errors, and JSON-pointer-localised error locations.
 */

export interface RetryPromptOptions {
  previousResponse: string;
  schema?: string;
  errors?: string[];
  history?: Array<{ role: string; content: string }>;
}

export interface RetryPromptResult {
  prompt: string;
  detectedErrors: string[];
  pointerPaths: string[];
}

const extractPointers = (errors: string[]): string[] => {
  const pointers: string[] = [];
  for (const e of errors) {
    // Extract JSON pointer paths like /field/subfield
    const matches = e.match(/\/[\w/[\]]+/g);
    if (matches) pointers.push(...matches);
  }
  return [...new Set(pointers)];
};

export const retryPrompt = (opts: RetryPromptOptions): RetryPromptResult => {
  const { previousResponse, schema, errors = [], history = [] } = opts;
  const pointerPaths = extractPointers(errors);

  const errorBlock =
    errors.length > 0
      ? `\n\nErrors detected:\n${errors.map((e, i) => `${i + 1}. ${e}`).join("\n")}`
      : "";

  const pointerBlock =
    pointerPaths.length > 0
      ? `\n\nAffected fields: ${pointerPaths.join(", ")}`
      : "";

  const schemaBlock = schema
    ? `\n\nExpected schema:\n\`\`\`\n${schema}\n\`\`\``
    : "";

  const historyBlock =
    history.length > 0
      ? `\n\nConversation history:\n${history
          .map((m) => `${m.role}: ${m.content}`)
          .join("\n")}`
      : "";

  const prompt = [
    "Your previous response could not be parsed or did not match the expected schema.",
    `\n\nPrevious response:\n\`\`\`\n${previousResponse}\n\`\`\``,
    errorBlock,
    pointerBlock,
    schemaBlock,
    historyBlock,
    "\n\nPlease provide a corrected response that is valid JSON (or the requested format) and matches the schema exactly.",
  ].join("");

  return {
    prompt,
    detectedErrors: errors,
    pointerPaths,
  };
};
