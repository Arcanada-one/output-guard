"""batch: Light list-comp wrappers over ``validate`` and ``repair``.

Mirror of packages/ts/src/batch.ts.
"""

from __future__ import annotations

from typing import Any

from .adapters.pydantic_ import SchemaAdapter
from .errors import ParseError, SchemaValidationError
from .orchestrator import SchemaValidator, repair, validate
from .results import Format, RepairResult, ValidationResult


def validate_batch(
    items: list[str],
    fmt: Format = "auto",
    schema: SchemaValidator | SchemaAdapter[Any] | None = None,
) -> list[ValidationResult]:
    return [validate(item, fmt, schema) for item in items]


def repair_batch(
    items: list[str],
    fmt: Format = "auto",
    schema: SchemaValidator | SchemaAdapter[Any] | None = None,
) -> list[RepairResult | dict[str, str]]:
    results: list[RepairResult | dict[str, str]] = []
    for item in items:
        try:
            results.append(repair(item, fmt, schema))
        except (ParseError, SchemaValidationError) as e:
            results.append({"error": str(e)})
    return results
