from output_guard.strategies.fix_closers import fix_closers


def test_missing_brace() -> None:
    assert fix_closers('{"a":1') == '{"a":1}'


def test_missing_bracket() -> None:
    assert fix_closers("[1,2") == "[1,2]"


def test_missing_both() -> None:
    assert fix_closers('{"a":[1,2') == '{"a":[1,2]}'


def test_balanced_passthrough() -> None:
    assert fix_closers('{"a":1}') == '{"a":1}'


def test_array_with_nested_object_unclosed() -> None:
    assert fix_closers('[{"a":1') == '[{"a":1}]'


def test_string_brace_ignored() -> None:
    assert fix_closers('{"a":"}"') == '{"a":"}"}'


def test_empty_string() -> None:
    assert fix_closers("") == ""


def test_only_opens() -> None:
    assert fix_closers("{{{") == "{{{}}}"


def test_already_balanced_array_in_obj() -> None:
    assert fix_closers('{"x":[1,2]}') == '{"x":[1,2]}'


def test_escaped_quote_inside() -> None:
    assert fix_closers('{"a":"x\\"y"') == '{"a":"x\\"y"}'
