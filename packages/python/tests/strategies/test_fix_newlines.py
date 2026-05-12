from output_guard.strategies.fix_newlines import fix_newlines


def test_newline_inside_string() -> None:
    assert fix_newlines('{"a": "hello\nworld"}') == '{"a": "hello\\nworld"}'


def test_cr_inside_string() -> None:
    assert fix_newlines('{"a": "hello\rworld"}') == '{"a": "hello\\rworld"}'


def test_newline_outside_string_preserved() -> None:
    assert fix_newlines('{\n"a": 1\n}') == '{\n"a": 1\n}'


def test_clean_passthrough() -> None:
    assert fix_newlines('{"a":1}') == '{"a":1}'


def test_escape_pair_preserved() -> None:
    assert fix_newlines('{"a": "x\\ny"}') == '{"a": "x\\ny"}'


def test_multiple_newlines_in_string() -> None:
    assert fix_newlines('"a\nb\nc"') == '"a\\nb\\nc"'


def test_string_with_escaped_quote() -> None:
    assert fix_newlines('"x\\"\ny"') == '"x\\"\\ny"'


def test_empty_string() -> None:
    assert fix_newlines("") == ""


def test_only_newlines() -> None:
    assert fix_newlines("\n\n\n") == "\n\n\n"


def test_newline_between_keys() -> None:
    assert fix_newlines('{"a": "x",\n"b": "y"}') == '{"a": "x",\n"b": "y"}'
