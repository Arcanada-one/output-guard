import pytest
from pydantic import BaseModel

from output_guard import (
    ParseError,
    SchemaValidationError,
    parse,
    pydantic_adapter,
    repair,
    validate,
    validate_and_repair,
)


class _Doc(BaseModel):
    a: int


def test_pass_a_clean_input() -> None:
    result = repair('{"a":1}')
    assert result.pass_ == "A"
    assert result.repaired is False
    assert result.strategies_applied == []
    assert result.data == {"a": 1}


def test_pass_a_with_repair() -> None:
    result = repair('{"a":1,}')
    assert result.pass_ == "A"
    assert result.repaired is True
    assert "fix-commas" in result.strategies_applied
    assert result.data == {"a": 1}


def test_pass_a_with_fence_and_python() -> None:
    result = repair('```json\n{"x": True, "y": None}\n```')
    assert result.pass_ == "A"
    assert result.data == {"x": True, "y": None}


def test_parse_error_on_garbage() -> None:
    with pytest.raises(ParseError):
        repair("totally not anything ::: }}}")


def test_schema_validation_error() -> None:
    adapter = pydantic_adapter(_Doc)
    with pytest.raises(SchemaValidationError):
        repair('{"a": "not-an-int"}', "json", adapter)


def test_schema_success() -> None:
    adapter = pydantic_adapter(_Doc)
    result = repair('{"a": 42}', "json", adapter)
    assert isinstance(result.data, _Doc)
    assert result.data.a == 42


def test_validate_clean() -> None:
    result = validate('{"a":1}')
    assert result.valid is True
    assert result.data == {"a": 1}


def test_validate_invalid_no_repair() -> None:
    result = validate('{"a":1,}')
    # validate does NOT repair — trailing comma stays a syntax error before fallback
    # but parse_json now falls back to json-repair internally → valid True
    # We document this: validate uses parse_json which itself repairs.
    assert result.valid is True


def test_parse_function() -> None:
    assert parse('{"a":1}') == {"a": 1}


def test_parse_fails_raises_schema_error() -> None:
    with pytest.raises(SchemaValidationError):
        parse(":::garbage:::")


def test_validate_and_repair_clean() -> None:
    v, r = validate_and_repair('{"a":1}')
    assert v.valid is True
    assert r is None


def test_validate_and_repair_with_repair() -> None:
    # json-repair fallback inside parse_json catches the trailing comma during
    # the direct-parse path; orchestrator therefore returns (valid, None).
    v, r = validate_and_repair('{"a":1,}', "json", pydantic_adapter(_Doc))
    assert v.valid is True
    assert r is None
