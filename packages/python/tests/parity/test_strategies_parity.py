"""Parity gate: byte-equal output between Python strategy and fixtures-shared.

Cross-language: TS test suite consumes the same `fixtures-shared/strategies/*/cases.jsonl`
and must produce identical outputs. Divergence anywhere fails this test.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from output_guard.strategies import (
    CANONICAL_ORDER,
)

_STRATEGY_FN = {name: fn for name, fn in CANONICAL_ORDER}
_ROOT = Path(__file__).resolve().parents[4] / "fixtures-shared" / "strategies"


def _load_cases(name: str) -> list[tuple[str, str]]:
    path = _ROOT / name / "cases.jsonl"
    if not path.exists():
        return []
    out: list[tuple[str, str]] = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            out.append((obj["in"], obj["out"]))
    return out


@pytest.mark.parametrize("name", list(_STRATEGY_FN.keys()))
def test_strategy_parity(name: str) -> None:
    cases = _load_cases(name)
    assert cases, f"No fixtures for {name}"
    fn = _STRATEGY_FN[name]
    for raw_in, expected in cases:
        actual = fn(raw_in)
        assert actual == expected, (
            f"{name} parity drift: in={raw_in!r} expected={expected!r} actual={actual!r}"
        )
