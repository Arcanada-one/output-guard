from output_guard.strategies.strip_fences import strip_fences


def test_json_fence() -> None:
    assert strip_fences("```json\n{\"a\":1}\n```") == '{"a":1}'


def test_yaml_fence() -> None:
    assert strip_fences("```yaml\na: 1\n```") == "a: 1"


def test_unlabelled_fence() -> None:
    assert strip_fences("```\n{\"x\":2}\n```") == '{"x":2}'


def test_no_fence_passthrough() -> None:
    assert strip_fences('{"a":1}') == '{"a":1}'


def test_inline_no_trailing_newline() -> None:
    assert strip_fences("```json\n{\"a\":1}```") == '{"a":1}'


def test_case_insensitive() -> None:
    assert strip_fences("```JSON\n{\"a\":1}\n```") == '{"a":1}'


def test_with_whitespace_around() -> None:
    assert strip_fences("  ```json\n{\"a\":1}\n```  ") == '{"a":1}'


def test_multiline_body() -> None:
    assert strip_fences("```json\n{\n  \"a\": 1\n}\n```") == '{\n  "a": 1\n}'


def test_crlf_line_endings() -> None:
    assert strip_fences("```json\r\n{\"a\":1}\r\n```") == '{"a":1}'


def test_empty_body() -> None:
    assert strip_fences("```\n\n```") == ""
