import pytest

from output_guard.errors import ParseError
from output_guard.formats.toml_ import parse_toml


def test_parse_kv() -> None:
    assert parse_toml('a = 1\nb = "two"') == {"a": 1, "b": "two"}


def test_parse_section() -> None:
    assert parse_toml("[s]\nx = 1") == {"s": {"x": 1}}


def test_parse_array() -> None:
    assert parse_toml("xs = [1, 2, 3]") == {"xs": [1, 2, 3]}


def test_parse_invalid_raises() -> None:
    with pytest.raises(ParseError):
        parse_toml("not = valid = toml")
