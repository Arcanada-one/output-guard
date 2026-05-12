from output_guard.strategies.fix_quotes import fix_quotes


def test_single_quoted_value() -> None:
    assert fix_quotes("{'a': 'b'}") == '{"a": "b"}'


def test_smart_double_quotes() -> None:
    assert fix_quotes("“a”") == '"a"'


def test_smart_single_open_close() -> None:
    assert fix_quotes("‘a’") == '"a"'


def test_french_guillemets() -> None:
    assert fix_quotes("«x»") == '"x"'


def test_escaped_apostrophe_inside() -> None:
    assert fix_quotes("'it\\'s'") == '"it\'s"'


def test_double_quoted_passthrough() -> None:
    assert fix_quotes('"hello"') == '"hello"'


def test_internal_double_quote_escaped() -> None:
    assert fix_quotes("'a\"b'") == '"a\\"b"'


def test_clean_object() -> None:
    assert fix_quotes('{"a":1}') == '{"a":1}'


def test_mixed_smart_quotes() -> None:
    assert fix_quotes("“key”: ‘val’") == '"key": "val"'


def test_empty_single_quoted() -> None:
    assert fix_quotes("''") == '""'
