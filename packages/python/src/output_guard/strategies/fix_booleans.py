"""fix-booleans: Replace Python booleans (True/False/None) with JSON equivalents.

Mirror of packages/ts/src/strategies/fix-booleans.ts. Word-boundary based; known
limitation: ``"True"`` inside a string is safe because ``"`` is non-word, but
embedded forms like ``"x True y"`` still match — see Implementation Notes M2 #1.
"""

from __future__ import annotations

import re

_TRUE = re.compile(r"\bTrue\b")
_FALSE = re.compile(r"\bFalse\b")
_NONE = re.compile(r"\bNone\b")


def fix_booleans(text: str) -> str:
    result = _TRUE.sub("true", text)
    result = _FALSE.sub("false", result)
    result = _NONE.sub("null", result)
    return result
