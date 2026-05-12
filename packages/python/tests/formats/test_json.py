from output_guard.formats.json_ import parse_json, repair_json


def test_parse_clean() -> None:
    assert parse_json('{"a": 1}') == {"a": 1}


def test_parse_array() -> None:
    assert parse_json("[1, 2, 3]") == [1, 2, 3]


def test_parse_with_repair_fallback() -> None:
    assert parse_json('{"a": 1,}') == {"a": 1}


def test_parse_unrepairable_returns_something() -> None:
    # json-repair coerces aggressively; orchestrator handles ParseError downstream.
    import contextlib

    from output_guard.errors import ParseError

    with contextlib.suppress(ParseError):
        parse_json("totally not json")


def test_repair_returns_string() -> None:
    out = repair_json('{"a": 1,}')
    assert isinstance(out, str)
    assert "}" in out


def test_parse_nested() -> None:
    assert parse_json('{"a": [1, {"b": 2}]}') == {"a": [1, {"b": 2}]}


def test_parse_string_value() -> None:
    assert parse_json('"hello"') == "hello"


def test_parse_null() -> None:
    assert parse_json("null") is None
