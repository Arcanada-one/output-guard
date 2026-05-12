from output_guard.strategies.extract_json import extract_json


def test_already_object() -> None:
    assert extract_json('{"a":1}') == '{"a":1}'


def test_already_array() -> None:
    assert extract_json("[1,2,3]") == "[1,2,3]"


def test_extract_from_prose() -> None:
    assert extract_json('Here it is: {"x":1} done') == '{"x":1}'


def test_extract_array_from_prose() -> None:
    assert extract_json("Answer: [1,2] yes") == "[1,2]"


def test_balanced_nested() -> None:
    assert extract_json('text {"a":{"b":[1,2]}} tail') == '{"a":{"b":[1,2]}}'


def test_no_brace_passthrough() -> None:
    assert extract_json("hello") == "hello"


def test_string_with_brace_in_it() -> None:
    assert extract_json('prefix {"a": "}{"} end') == '{"a": "}{"}'


def test_first_open_wins_obj_before_arr() -> None:
    assert extract_json('x {"a":1} [2]') == '{"a":1}'


def test_first_open_wins_arr_before_obj() -> None:
    assert extract_json('x [1] {"a":1}') == "[1]"


def test_unbalanced_passthrough() -> None:
    text = "prefix {unbalanced"
    assert extract_json(text) == text
