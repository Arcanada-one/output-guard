"""Result and report dataclasses. Mirror of packages/ts/src/results.ts."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any, Literal

Format = Literal["json", "yaml", "toml", "python", "auto"]
Strategy = Callable[[str], str]

OrchestratorPass = Literal["A", "B", "exhausted"]
"""Two-pass orchestrator outcome (creative-CONN-0087):
``A``         — Pass A combined-apply succeeded (fast path).
``B``         — Pass B isolating single-step fallback succeeded.
``exhausted`` — both passes failed; schema validation rejected the output.
"""


@dataclass(frozen=True, slots=True)
class ValidationResult:
    valid: bool
    data: Any = None
    errors: list[str] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class RepairResult:
    repaired: bool
    raw: str
    data: Any = None
    strategies_applied: list[str] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class RepairReport:
    strategies_applied: list[str]
    retries: int
    final_valid: bool
    pass_: OrchestratorPass
    error: str | None = None


@dataclass(frozen=True, slots=True)
class GuardedGenerateResult:
    data: Any
    report: RepairReport
