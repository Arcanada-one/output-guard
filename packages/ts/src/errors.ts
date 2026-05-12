export class ParseError extends Error {
  override readonly name = "ParseError";
  constructor(message: string, cause?: unknown) {
    super(message);
    if (cause !== undefined) {
      this.cause = cause;
    }
  }
}

export class SchemaValidationError extends Error {
  override readonly name = "SchemaValidationError";
  readonly issues: readonly string[];
  constructor(message: string, issues: readonly string[] = []) {
    super(message);
    this.issues = issues;
  }
}

export class RepairError extends Error {
  override readonly name = "RepairError";
  readonly strategiesApplied: readonly string[];
  constructor(message: string, strategiesApplied: readonly string[] = []) {
    super(message);
    this.strategiesApplied = strategiesApplied;
  }
}

export class GuardedGenerationError extends Error {
  override readonly name = "GuardedGenerationError";
  readonly retries: number;
  readonly lastError?: unknown;
  constructor(message: string, retries: number, lastError?: unknown) {
    super(message);
    this.retries = retries;
    if (lastError !== undefined) {
      this.lastError = lastError;
    }
  }
}
