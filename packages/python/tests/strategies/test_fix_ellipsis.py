from output_guard.strategies.fix_ellipsis import fix_ellipsis


def test_array_with_ellipsis() -> None:
    assert fix_ellipsis("[1, 2, ...]") == "[1, 2]"


def test_array_with_unicode_ellipsis() -> None:
    assert fix_ellipsis("[1, 2, …]") == "[1, 2]"


def test_object_with_ellipsis() -> None:
    assert fix_ellipsis('{"a":1, ...}') == '{"a":1}'


def test_only_ellipsis_array() -> None:
    assert fix_ellipsis("[...]") == "[]"


def test_only_unicode_ellipsis_array() -> None:
    assert fix_ellipsis("[…]") == "[]"


def test_passthrough_clean() -> None:
    assert fix_ellipsis("[1, 2]") == "[1, 2]"


def test_no_array_no_change() -> None:
    assert fix_ellipsis("text ... more") == "text ... more"


def test_nested() -> None:
    assert fix_ellipsis("[[1, ...], [2, ...]]") == "[[1], [2]]"


def test_mixed_arr_obj() -> None:
    assert fix_ellipsis('{"a":[1, ...], "b": 2}') == '{"a":[1], "b": 2}'


def test_passthrough_no_close_after() -> None:
    assert fix_ellipsis("[1, ..., 2]") == "[1, ..., 2]"
