from output_guard.strategies.fix_truncated import fix_truncated


def test_trailing_ellipsis_dots() -> None:
    assert fix_truncated('{"a": 1...') == '{"a": 1'


def test_trailing_ellipsis_unicode() -> None:
    assert fix_truncated('{"a": 1…') == '{"a": 1'


def test_trailing_comma() -> None:
    assert fix_truncated('{"a": 1,') == '{"a": 1'


def test_unterminated_string_closed() -> None:
    assert fix_truncated('{"a": "hello') == '{"a": "hello"'


def test_clean_passthrough() -> None:
    assert fix_truncated('{"a": 1}') == '{"a": 1}'


def test_balanced_quotes() -> None:
    assert fix_truncated('{"a": "x"}') == '{"a": "x"}'


def test_strip_trailing_whitespace_only() -> None:
    assert fix_truncated('{"a": 1}   ') == '{"a": 1}'


def test_escaped_quote_count() -> None:
    # \\" counts as escape pair — algorithm skips both chars
    assert fix_truncated('{"a": "x\\"y"') == '{"a": "x\\"y"'


def test_empty_string() -> None:
    assert fix_truncated("") == ""


def test_only_whitespace() -> None:
    assert fix_truncated("   ") == ""
