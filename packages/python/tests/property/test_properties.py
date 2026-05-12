"""Hypothesis property tests for strategies and orchestrator."""
from __future__ import annotations

import json

from hypothesis import given, settings
from hypothesis import strategies as st

from output_guard import repair
from output_guard.strategies import (
    fix_booleans,
    fix_closers,
    fix_commas,
    fix_ellipsis,
    fix_encoding,
    fix_keys,
    fix_newlines,
    fix_quotes,
    fix_truncated,
    fix_unicode,
    fix_values,
    remove_comments,
    strip_fences,
)

_json_atom = st.one_of(
    st.none(),
    st.booleans(),
    st.integers(min_value=-1_000, max_value=1_000),
    st.floats(allow_nan=False, allow_infinity=False),
    st.text(
        alphabet=st.characters(
            min_codepoint=0x20,
            max_codepoint=0x7E,
            blacklist_characters='"\\\'/#{}[]:,',
        ),
        max_size=10,
    ),
)
_json_value = st.recursive(
    _json_atom,
    lambda c: st.one_of(
        st.lists(c, max_size=5),
        st.dictionaries(
            st.text(
                alphabet=st.characters(
                    min_codepoint=0x61, max_codepoint=0x7A
                ),
                min_size=1,
                max_size=5,
            ),
            c,
            max_size=5,
        ),
    ),
    max_leaves=10,
)


@given(_json_value)
@settings(max_examples=50, deadline=None)
def test_repair_preserves_clean_json(value: object) -> None:
    serialised = json.dumps(value)
    result = repair(serialised, "json")
    assert result.data == value
    assert result.pass_ == "A"


@given(st.text(max_size=200))
@settings(max_examples=100, deadline=None)
def test_strategies_are_idempotent_on_clean_strings(text: str) -> None:
    # fix-closers / fix-inner-quotes / fix-newlines are intentionally not
    # idempotent: each pass adds closers / escapes based on string-context
    # parsing, so running them twice on adversarial inputs may amplify.
    for fn in (
        fix_encoding,
        strip_fences,
        remove_comments,
        fix_commas,
        fix_quotes,
        fix_keys,
        fix_values,
        fix_booleans,
        fix_truncated,
        fix_ellipsis,
        fix_unicode,
    ):
        assert fn(fn(text)) == fn(text)


@given(_json_value)
@settings(max_examples=30, deadline=None)
def test_trailing_comma_round_trip(value: object) -> None:
    if not isinstance(value, dict | list):
        return
    raw = json.dumps(value)
    if not raw.endswith(("}", "]")):
        return
    broken = raw[:-1] + "," + raw[-1]
    fixed = fix_commas(broken)
    assert json.loads(fixed) == value
