/**
 * Hard cap on retry attempts in `guardedGenerate`.
 * Mirrored in `packages/python/src/output_guard/constants.py` — keep in sync.
 * Rationale: bounded cost (creative-CONN-0087 F4 adversarial-latency mitigation).
 */
export const MAX_RETRIES = 3 as const;

export const RETRY_BACKOFF_MS = 250 as const;

export const FORMAT_DEFAULT = "auto" as const;

/** Default per-call timeout for AbortController-wrapped guard execution (ms). */
export const DEFAULT_TIMEOUT_MS = 30_000 as const;
