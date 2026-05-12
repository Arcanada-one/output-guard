"""python-literal format: mini-chain converting Python literal → JSON-parseable.

Mirror of packages/ts/src/formats/python-literal.ts.
Pipeline: None→null, True→true, False→false, single→double quotes, strip trailing commas.
"""

from __future__ import annotations

import json
import re
from typing import Any

from ..errors import ParseError

_NONE = re.compile(r"\bNone\b")
_TRUE = re.compile(r"\bTrue\b")
_FALSE = re.compile(r"\bFalse\b")
_SINGLE_QUOTED = re.compile(r"'([^'\\]*(?:\\.[^'\\]*)*)'")
_TRAILING = re.compile(r",(\s*[}\]])")


def _to_python_json(text: str) -> str:
    out = _NONE.sub("null", text)
    out = _TRUE.sub("true", out)
    out = _FALSE.sub("false", out)
    out = _SINGLE_QUOTED.sub(r'"\1"', out)
    out = _TRAILING.sub(r"\1", out)
    return out


def parse_python_literal(text: str) -> Any:
    converted = _to_python_json(text.strip())
    try:
        return json.loads(converted)
    except json.JSONDecodeError as e:
        raise ParseError(f"python-literal parse failed: {e}", e) from e
