from pydantic import BaseModel

from output_guard.adapters import pydantic_adapter


class _Item(BaseModel):
    a: int
    b: str


def test_valid_data() -> None:
    adapter = pydantic_adapter(_Item)
    result = adapter.validate({"a": 1, "b": "hello"})
    assert result.valid is True
    assert isinstance(result.data, _Item)
    assert result.data.a == 1


def test_invalid_missing_field() -> None:
    adapter = pydantic_adapter(_Item)
    result = adapter.validate({"a": 1})
    assert result.valid is False
    assert any("b" in e for e in result.errors)


def test_invalid_wrong_type() -> None:
    adapter = pydantic_adapter(_Item)
    result = adapter.validate({"a": "x", "b": "y"})
    assert result.valid is False
    assert any("a" in e for e in result.errors)


def test_extra_field_ignored() -> None:
    adapter = pydantic_adapter(_Item)
    result = adapter.validate({"a": 1, "b": "ok", "extra": 99})
    assert result.valid is True


def test_root_level_error() -> None:
    adapter = pydantic_adapter(_Item)
    result = adapter.validate("not a dict")
    assert result.valid is False
