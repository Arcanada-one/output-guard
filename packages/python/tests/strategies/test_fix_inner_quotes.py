from output_guard.strategies.fix_inner_quotes import fix_inner_quotes


def test_inner_quote_escaped() -> None:
    assert fix_inner_quotes('{"a": "he said "hi""}') == '{"a": "he said \\"hi\\""}'


def test_no_inner_quote() -> None:
    assert fix_inner_quotes('{"a": "x"}') == '{"a": "x"}'


def test_escaped_quote_preserved() -> None:
    assert fix_inner_quotes('{"a": "x\\"y"}') == '{"a": "x\\"y"}'


def test_clean_passthrough() -> None:
    assert fix_inner_quotes('{"a":1}') == '{"a":1}'


def test_quote_before_colon_closes() -> None:
    assert fix_inner_quotes('{"key": "val"}') == '{"key": "val"}'


def test_quote_before_comma_closes() -> None:
    assert fix_inner_quotes('{"a": "x", "b": "y"}') == '{"a": "x", "b": "y"}'


def test_quote_before_close_brace() -> None:
    assert fix_inner_quotes('{"a": "x"}') == '{"a": "x"}'


def test_quote_before_close_bracket() -> None:
    assert fix_inner_quotes('["a"]') == '["a"]'


def test_quote_at_end() -> None:
    assert fix_inner_quotes('{"a": "x"') == '{"a": "x"'


def test_multiple_inner_quotes() -> None:
    assert fix_inner_quotes('{"q": "a "b" c"}') == '{"q": "a \\"b\\" c"}'
