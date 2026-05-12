"""Integration: realistic broken-LLM-output samples through the full chain."""
from __future__ import annotations

import pytest
from pydantic import BaseModel

from output_guard import SchemaValidationError, pydantic_adapter, repair


class _User(BaseModel):
    name: str
    age: int


def test_fenced_python_dict() -> None:
    raw = "```python\n{'name': 'Alice', 'age': 30}\n```"
    result = repair(raw, "auto", pydantic_adapter(_User))
    assert isinstance(result.data, _User)
    assert result.data.name == "Alice"


def test_truncated_with_trailing_comma() -> None:
    raw = '{"name": "Bob", "age": 25,'
    result = repair(raw, "json", pydantic_adapter(_User))
    assert isinstance(result.data, _User)
    assert result.data.age == 25


def test_comments_and_smart_quotes() -> None:
    raw = '{ /* user */ "name": “Eve”, "age": 99 }'
    result = repair(raw, "json", pydantic_adapter(_User))
    assert isinstance(result.data, _User)


def test_prose_wrapped_json() -> None:
    raw = 'Sure, here you go: {"name": "Tom", "age": 1} done.'
    result = repair(raw, "json", pydantic_adapter(_User))
    assert isinstance(result.data, _User)


def test_schema_rejected_after_repair() -> None:
    raw = '{"name": "Pat", "age": "not-a-number"}'
    with pytest.raises(SchemaValidationError):
        repair(raw, "json", pydantic_adapter(_User))


def test_unbalanced_object_closed() -> None:
    raw = '{"name": "Zoe", "age": 40'
    result = repair(raw, "json", pydantic_adapter(_User))
    assert isinstance(result.data, _User)
