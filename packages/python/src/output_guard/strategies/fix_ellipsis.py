"""fix-ellipsis: Remove placeholder ellipsis from arrays/objects.

Mirror of packages/ts/src/strategies/fix-ellipsis.ts.
"""

from __future__ import annotations

import re

_COMMA_DOTS_BEFORE_CLOSE = re.compile(r",\s*\.\.\.\s*(?=[}\]])")
_COMMA_UC_BEFORE_CLOSE = re.compile(r",\s*…\s*(?=[}\]])")
_ONLY_DOTS_ARRAY = re.compile(r"\[\s*\.\.\.\s*\]")
_ONLY_UC_ARRAY = re.compile(r"\[\s*…\s*\]")


def fix_ellipsis(text: str) -> str:
    result = _COMMA_DOTS_BEFORE_CLOSE.sub("", text)
    result = _COMMA_UC_BEFORE_CLOSE.sub("", result)
    result = _ONLY_DOTS_ARRAY.sub("[]", result)
    result = _ONLY_UC_ARRAY.sub("[]", result)
    return result
