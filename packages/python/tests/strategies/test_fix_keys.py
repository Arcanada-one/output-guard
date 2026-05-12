from output_guard.strategies.fix_keys import fix_keys


def test_bare_key() -> None:
    assert fix_keys("{a: 1}") == '{"a": 1}'


def test_multiple_bare_keys() -> None:
    assert fix_keys("{a: 1, b: 2}") == '{"a": 1, "b": 2}'


def test_already_quoted() -> None:
    assert fix_keys('{"a": 1}') == '{"a": 1}'


def test_underscore_key() -> None:
    assert fix_keys("{a_b: 1}") == '{"a_b": 1}'


def test_dollar_key() -> None:
    assert fix_keys("{$x: 1}") == '{"$x": 1}'


def test_after_newline() -> None:
    assert fix_keys("{\nkey: 1\n}") == '{\n"key": 1\n}'


def test_alphanumeric_key() -> None:
    assert fix_keys("{a1: 1}") == '{"a1": 1}'


def test_passthrough_no_keys() -> None:
    assert fix_keys("[1,2]") == "[1,2]"


def test_no_replace_in_value() -> None:
    assert fix_keys('{"x": "y:z"}') == '{"x": "y:z"}'


def test_key_with_whitespace_before_colon() -> None:
    assert fix_keys("{key  : 1}") == '{"key"  : 1}'
