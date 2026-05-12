from output_guard.strategies.fix_encoding import fix_encoding


def test_strips_bom() -> None:
    assert fix_encoding("﻿{\"a\":1}") == '{"a":1}'


def test_replaces_capital_c_dot() -> None:
    assert fix_encoding("aĊb") == "a\nb"


def test_replaces_capital_g_dot() -> None:
    assert fix_encoding("aĠb") == "a b"


def test_lone_surrogate_replaced() -> None:
    assert fix_encoding("a\ud800b") == "a�b"


def test_passthrough_clean() -> None:
    assert fix_encoding('{"a":1}') == '{"a":1}'


def test_empty_string() -> None:
    assert fix_encoding("") == ""


def test_only_bom() -> None:
    assert fix_encoding("﻿") == ""


def test_multiple_tokens() -> None:
    assert fix_encoding("ĊĊĠĠ") == "\n\n  "


def test_passthrough_unicode_letters() -> None:
    assert fix_encoding("привет") == "привет"


def test_bom_at_start_only() -> None:
    assert fix_encoding("a﻿b") == "a﻿b"
