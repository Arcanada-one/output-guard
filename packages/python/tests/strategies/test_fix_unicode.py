from output_guard.strategies.fix_unicode import fix_unicode


def test_valid_escape_passthrough() -> None:
    assert fix_unicode("\\u0041") == "\\u0041"


def test_invalid_escape_replaced() -> None:
    # No hex digits consumed; ZZZZ stays as plain text after the replacement.
    assert fix_unicode("\\uZZZZ") == "\\uFFFDZZZZ"


def test_partial_hex_replaced() -> None:
    assert fix_unicode("\\u00") == "\\uFFFD"


def test_partial_hex_with_trailing() -> None:
    # 2 hex digits consumed, ZZ stays as plain text.
    assert fix_unicode("\\u00ZZ") == "\\uFFFDZZ"


def test_non_u_escape_passthrough() -> None:
    assert fix_unicode("\\n") == "\\n"


def test_double_backslash() -> None:
    assert fix_unicode("\\\\u0041") == "\\\\u0041"


def test_no_escape_passthrough() -> None:
    assert fix_unicode("hello") == "hello"


def test_empty_string() -> None:
    assert fix_unicode("") == ""


def test_trailing_backslash() -> None:
    # Lone trailing backslash: result accumulates it (i+1 < n is false)
    assert fix_unicode("a\\") == "a\\"


def test_multiple_escapes_mixed() -> None:
    assert fix_unicode("\\u00FF\\uZZZZ") == "\\u00FF\\uFFFDZZZZ"
