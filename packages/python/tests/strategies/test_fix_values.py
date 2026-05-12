from output_guard.strategies.fix_values import fix_values


def test_nan() -> None:
    assert fix_values('{"a": NaN}') == '{"a": null}'


def test_pos_infinity() -> None:
    assert fix_values('{"a": Infinity}') == '{"a": null}'


def test_neg_infinity() -> None:
    assert fix_values('{"a": -Infinity}') == '{"a": null}'


def test_undefined() -> None:
    assert fix_values('{"a": undefined}') == '{"a": null}'


def test_all_in_one() -> None:
    assert (
        fix_values('{"a": NaN, "b": Infinity, "c": -Infinity, "d": undefined}')
        == '{"a": null, "b": null, "c": null, "d": null}'
    )


def test_passthrough_normal() -> None:
    assert fix_values('{"a": 1, "b": 2.5}') == '{"a": 1, "b": 2.5}'


def test_inside_string_no_replace() -> None:
    assert fix_values('{"a": "NaN"}') == '{"a": "NaN"}'


def test_with_extra_whitespace() -> None:
    assert fix_values('{"a":   NaN}') == '{"a": null}'


def test_no_match() -> None:
    assert fix_values('{"a": true}') == '{"a": true}'


def test_word_boundary() -> None:
    # NaN inside Nancy must not be replaced — but our regex uses \b so Nancy stays
    assert fix_values('{"a": "Nancy"}') == '{"a": "Nancy"}'
