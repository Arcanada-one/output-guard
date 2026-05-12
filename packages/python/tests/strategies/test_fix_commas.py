from output_guard.strategies.fix_commas import fix_commas


def test_trailing_in_object() -> None:
    assert fix_commas('{"a":1,}') == '{"a":1}'


def test_trailing_in_array() -> None:
    assert fix_commas("[1,2,3,]") == "[1,2,3]"


def test_trailing_with_whitespace() -> None:
    assert fix_commas("[1, 2, 3, ]") == "[1, 2, 3 ]"


def test_trailing_with_newline() -> None:
    assert fix_commas("[1,\n]") == "[1\n]"


def test_clean_passthrough() -> None:
    assert fix_commas("[1,2]") == "[1,2]"


def test_nested() -> None:
    assert fix_commas('{"a":[1,],"b":2,}') == '{"a":[1],"b":2}'


def test_empty_object() -> None:
    assert fix_commas("{}") == "{}"


def test_no_trailing() -> None:
    assert fix_commas('{"a":1}') == '{"a":1}'


def test_multiple_levels() -> None:
    assert fix_commas("[[1,],[2,],]") == "[[1],[2]]"


def test_string_with_comma() -> None:
    # comma inside string not before bracket — should still be safe
    assert fix_commas('["a,b"]') == '["a,b"]'
