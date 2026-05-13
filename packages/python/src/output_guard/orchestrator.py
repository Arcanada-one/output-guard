"""Two-pass orchestrator.

Mirror of packages/ts/src/orchestrator.ts.

Pass A: apply all 15 strategies in CANONICAL_ORDER, then parse once.
Pass B: for each strategy individually, apply → parse. First success wins.

Outcome contract (caller-side catch is canonical):
- Success → ``RepairResult`` with authoritative ``pass_: "A" | "B"``.
- Schema rejects parsed data → raise ``SchemaValidationError``.
- Both passes parse-exhausted → raise ``ParseError``. Consumers MUST
  catch ``ParseError`` to construct ``repair_report.pass_: "exhausted"``.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any, Literal

from .adapters.pydantic_ import SchemaAdapter
from .errors import ParseError, SchemaValidationError
from .formats.detect import detect_format
from .formats.json_ import parse_json
from .formats.python_literal import parse_python_literal
from .formats.toml_ import parse_toml
from .formats.yaml_ import parse_yaml
from .results import Format, RepairResult, ValidationResult
from .retry_prompt import retry_prompt
from .strategies import CANONICAL_ORDER

__all__ = ["parse", "repair", "retry_prompt", "validate", "validate_and_repair"]

SchemaValidator = Callable[[Any], ValidationResult]
ConcreteFormat = Literal["json", "yaml", "toml", "python"]


def _resolve_format(text: str, fmt: Format) -> ConcreteFormat:
    if fmt == "auto":
        return detect_format(text)
    return fmt


def _try_parse(text: str, fmt: ConcreteFormat) -> Any:
    """Return parsed value or _SENTINEL_FAILURE on failure (None is a valid JSON value)."""
    try:
        if fmt == "json":
            return parse_json(text)
        if fmt == "yaml":
            return parse_yaml(text)
        if fmt == "toml":
            return parse_toml(text)
        if fmt == "python":
            return parse_python_literal(text)
    except ParseError:
        return _SENTINEL_FAILURE
    return _SENTINEL_FAILURE


class _SentinelFailure:
    __slots__ = ()


_SENTINEL_FAILURE: Any = _SentinelFailure()


def _coerce_validator(
    schema: SchemaValidator | SchemaAdapter[Any] | None,
) -> SchemaValidator | None:
    if schema is None:
        return None
    if isinstance(schema, SchemaAdapter):
        return schema.validate
    return schema


def _run_schema(data: Any, schema: SchemaValidator | None) -> Any:
    if schema is None:
        return data
    result = schema(data)
    if not result.valid:
        raise SchemaValidationError(
            f"Schema validation failed: {'; '.join(result.errors) or 'unknown'}",
            list(result.errors),
        )
    return result.data


def _pass_a(text: str, fmt: ConcreteFormat) -> tuple[str, list[str]] | None:
    current = text
    applied: list[str] = []
    for name, fn in CANONICAL_ORDER:
        nxt = fn(current)
        if nxt != current:
            applied.append(name)
        current = nxt
    parsed = _try_parse(current, fmt)
    if parsed is not _SENTINEL_FAILURE:
        return current, applied
    return None


def _pass_b(text: str, fmt: ConcreteFormat) -> tuple[str, list[str]] | None:
    for name, fn in CANONICAL_ORDER:
        candidate = fn(text)
        if candidate == text:
            continue
        parsed = _try_parse(candidate, fmt)
        if parsed is not _SENTINEL_FAILURE:
            return candidate, [name]
    return None


def repair(
    text: str,
    fmt: Format = "auto",
    schema: SchemaValidator | SchemaAdapter[Any] | None = None,
) -> RepairResult:
    """Core two-pass repair chain.

    Returns ``RepairResult`` on success. Raises ``SchemaValidationError`` when
    schema rejects. Raises ``ParseError`` when both passes fail to parse.
    """

    validator = _coerce_validator(schema)
    concrete = _resolve_format(text, fmt)

    a_result = _pass_a(text, concrete)
    if a_result is not None:
        repaired_text, applied = a_result
        parsed = _try_parse(repaired_text, concrete)
        validated = _run_schema(parsed, validator)
        return RepairResult(
            repaired=len(applied) > 0,
            raw=repaired_text,
            pass_="A",
            data=validated,
            strategies_applied=applied,
        )

    b_result = _pass_b(text, concrete)
    if b_result is not None:
        repaired_text, applied = b_result
        parsed = _try_parse(repaired_text, concrete)
        validated = _run_schema(parsed, validator)
        return RepairResult(
            repaired=True,
            raw=repaired_text,
            pass_="B",
            data=validated,
            strategies_applied=applied,
        )

    raise ParseError("Both passes exhausted: could not parse or repair input")


def validate(
    text: str,
    fmt: Format = "auto",
    schema: SchemaValidator | SchemaAdapter[Any] | None = None,
) -> ValidationResult:
    """Validate without repair — parse + optional schema check."""
    validator = _coerce_validator(schema)
    concrete = _resolve_format(text, fmt)
    parsed = _try_parse(text, concrete)
    if parsed is _SENTINEL_FAILURE:
        return ValidationResult(valid=False, errors=["Parse failed"])
    if validator is None:
        return ValidationResult(valid=True, data=parsed)
    return validator(parsed)


def validate_and_repair(
    text: str,
    fmt: Format = "auto",
    schema: SchemaValidator | SchemaAdapter[Any] | None = None,
) -> tuple[ValidationResult, RepairResult | None]:
    """Validate then repair if needed. Returns ``(validation, repair_or_None)``."""
    validator = _coerce_validator(schema)
    concrete = _resolve_format(text, fmt)
    direct = _try_parse(text, concrete)
    if direct is not _SENTINEL_FAILURE:
        v_result = validator(direct) if validator else ValidationResult(valid=True, data=direct)
        if v_result.valid:
            return v_result, None

    try:
        repair_result = repair(text, fmt, schema)
        if repair_result.data is not None:
            return ValidationResult(valid=True, data=repair_result.data), repair_result
        return ValidationResult(valid=False, errors=["Repair produced no data"]), repair_result
    except (ParseError, SchemaValidationError) as e:
        return ValidationResult(valid=False, errors=[str(e)]), None


def parse(text: str, fmt: Format = "auto") -> Any:
    """Parse raw text in given format. Raises ``SchemaValidationError`` on failure."""
    concrete = _resolve_format(text, fmt)
    result = _try_parse(text, concrete)
    if result is _SENTINEL_FAILURE:
        raise SchemaValidationError(f"Failed to parse as {concrete}", [])
    return result
