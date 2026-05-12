export type Format = "json" | "yaml" | "toml" | "python" | "auto";

export type Strategy = (text: string) => string;

export interface ValidationResult<T = unknown> {
  valid: boolean;
  data?: T;
  errors?: string[];
}

export interface RepairResult<T = unknown> {
  repaired: boolean;
  data?: T;
  raw: string;
  strategiesApplied: string[];
}

/**
 * Two-pass orchestrator outcome (creative-CONN-0087):
 *   "A"         — Pass A combined-apply succeeded (fast path, ~250µs).
 *   "B"         — Pass B isolating single-step fallback succeeded.
 *   "exhausted" — both passes failed; schema validation rejected the output.
 */
export type OrchestratorPass = "A" | "B" | "exhausted";

export interface RepairReport {
  strategiesApplied: string[];
  retries: number;
  finalValid: boolean;
  pass: OrchestratorPass;
  error?: string;
}

export interface GuardedGenerateResult<T = unknown> {
  data: T;
  report: RepairReport;
}
