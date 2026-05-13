"""Result and report dataclasses. Mirror of packages/ts/src/results.ts."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any, Literal

Format = Literal["json", "yaml", "toml", "python", "auto"]
Strategy = Callable[[str], str]

OrchestratorPass = Literal["A", "B", "exhausted"]
"""Two-pass orchestrator outcome:
``A``         — Pass A combined-apply succeeded (fast path).
``B``         — Pass B isolating single-step fallback succeeded.
``exhausted`` — both passes failed; schema validation rejected the output.
"""


@dataclass(frozen=True, slots=True)
class ValidationResult:
    valid: bool
    data: Any = None
    errors: list[str] = field(default_factory=list)


RepairPass = Literal["A", "B"]
"""Authoritative pass label of the two-pass orchestrator.

``A`` — Pass A combined-apply parse path (also covers raw-parse fast path).
``B`` — Pass B isolating single-step fallback.

Exhaustion is signalled by ``ParseError`` raise, not by this field — see
orchestrator docstring + consumer catch contract.
"""


@dataclass(frozen=True, slots=True)
class RepairResult:
    repaired: bool
    raw: str
    pass_: RepairPass
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
