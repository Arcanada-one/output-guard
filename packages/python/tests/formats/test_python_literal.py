import pytest

from output_guard.errors import ParseError
from output_guard.formats.python_literal import parse_python_literal


def test_python_true() -> None:
    assert parse_python_literal("{'a': True}") == {"a": True}


def test_python_false() -> None:
    assert parse_python_literal("{'a': False}") == {"a": False}


def test_python_none() -> None:
    assert parse_python_literal("{'a': None}") == {"a": None}


def test_python_list() -> None:
    assert parse_python_literal("[1, 2, None]") == [1, 2, None]


def test_python_nested() -> None:
    assert parse_python_literal("{'a': [True, None]}") == {"a": [True, None]}


def test_invalid_raises() -> None:
    with pytest.raises(ParseError):
        parse_python_literal("{not valid")
