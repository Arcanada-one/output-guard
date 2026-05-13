"""Bootstrap smoke — constants mirror TS, error hierarchy intact."""

import pytest

from output_guard import (
    FORMAT_DEFAULT,
    MAX_RETRIES,
    ParseError,
    SchemaValidationError,
)


def test_max_retries_is_three() -> None:
    """MAX_RETRIES MUST equal TS-side constant."""
    assert MAX_RETRIES == 3


def test_format_default_is_auto() -> None:
    assert FORMAT_DEFAULT == "auto"


def test_parse_error_chain() -> None:
    cause = RuntimeError("boom")
    err = ParseError("wrap", cause)
    assert err.__cause__ is cause


def test_schema_validation_error_issues() -> None:
    err = SchemaValidationError("nope", ["/x: required"])
    assert err.issues == ["/x: required"]


def test_schema_validation_error_no_issues() -> None:
    err = SchemaValidationError("nope")
    assert err.issues == []


def test_parse_error_raises() -> None:
    with pytest.raises(ParseError):
        raise ParseError("test")
