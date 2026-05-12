import pytest

from output_guard.errors import ParseError
from output_guard.formats.yaml_ import parse_yaml


def test_parse_simple() -> None:
    assert parse_yaml("a: 1\nb: 2") == {"a": 1, "b": 2}


def test_parse_list() -> None:
    assert parse_yaml("- 1\n- 2\n- 3") == [1, 2, 3]


def test_parse_nested() -> None:
    assert parse_yaml("a:\n  b: 1") == {"a": {"b": 1}}


def test_parse_doc_separator() -> None:
    assert parse_yaml("---\na: 1") == {"a": 1}


def test_parse_invalid_raises() -> None:
    with pytest.raises(ParseError):
        parse_yaml("a: [\n  - unclosed")


def test_parse_empty_returns_none() -> None:
    assert parse_yaml("") is None
