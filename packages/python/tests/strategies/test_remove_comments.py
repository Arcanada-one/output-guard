from output_guard.strategies.remove_comments import remove_comments


def test_line_comment_double_slash() -> None:
    assert remove_comments('{"a":1} // tail\n') == '{"a":1} \n'


def test_block_comment() -> None:
    assert remove_comments('{/* note */ "a":1}') == '{ "a":1}'


def test_hash_comment() -> None:
    assert remove_comments('a: 1 # tail\n') == 'a: 1 \n'


def test_preserve_url_inside_string() -> None:
    assert remove_comments('{"u": "https://x.com/y"}') == '{"u": "https://x.com/y"}'


def test_preserve_hash_inside_string() -> None:
    assert remove_comments('{"u": "#tag"}') == '{"u": "#tag"}'


def test_escaped_quote_inside_string() -> None:
    assert remove_comments('{"u": "\\"q\\""}') == '{"u": "\\"q\\""}'


def test_multi_line_block() -> None:
    assert remove_comments('a /*\nmulti\n*/ b') == 'a  b'


def test_no_comment_passthrough() -> None:
    assert remove_comments('{"a":1}') == '{"a":1}'


def test_consecutive_line_comments() -> None:
    assert remove_comments('// one\n// two\n{"a":1}') == '\n\n{"a":1}'


def test_block_without_close_consumes_rest() -> None:
    assert remove_comments('a /* x') == 'a '
