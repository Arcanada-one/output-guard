"""Tunable constants. Mirrored in packages/ts/src/constants.ts — keep in sync."""

from typing import Final

MAX_RETRIES: Final[int] = 3
"""Hard cap on retry attempts in ``guarded_generate``.

Rationale: bounded cost — adversarial-latency mitigation.
"""

RETRY_BACKOFF_MS: Final[int] = 250

FORMAT_DEFAULT: Final[str] = "auto"

DEFAULT_TIMEOUT_MS: Final[int] = 30_000
"""Default per-call timeout for guard execution (asyncio.timeout-wrapped)."""
