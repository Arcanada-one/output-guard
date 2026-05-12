from output_guard.strategies.fix_booleans import fix_booleans


def test_true_replaced() -> None:
    assert fix_booleans('{"a": True}') == '{"a": true}'


def test_false_replaced() -> None:
    assert fix_booleans('{"a": False}') == '{"a": false}'


def test_none_replaced() -> None:
    assert fix_booleans('{"a": None}') == '{"a": null}'


def test_all_in_one() -> None:
    assert fix_booleans('[True, False, None]') == '[true, false, null]'


def test_string_quote_boundary() -> None:
    # "True" as string label — word boundary between " and T means \bTrue\b matches
    # this is a documented limitation per Implementation Notes M2 #1
    assert fix_booleans('{"label": "True"}') == '{"label": "true"}'


def test_camelcase_passthrough() -> None:
    assert fix_booleans('{"a": "TrueValue"}') == '{"a": "TrueValue"}'


def test_lowercase_passthrough() -> None:
    assert fix_booleans('{"a": true}') == '{"a": true}'


def test_negative_word_boundary() -> None:
    assert fix_booleans('TrueAndFalse') == 'TrueAndFalse'


def test_multiple_occurrences() -> None:
    assert fix_booleans('True True True') == 'true true true'


def test_passthrough_no_python() -> None:
    assert fix_booleans('{"a": 1}') == '{"a": 1}'
