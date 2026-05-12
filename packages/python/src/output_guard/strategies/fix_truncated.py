"""fix-truncated: Repair truncated JSON.

Mirror of packages/ts/src/strategies/fix-truncated.ts.
"""

from __future__ import annotations

import re

_ELLIPSIS_UC = re.compile(r"…$")
_ELLIPSIS_DOTS = re.compile(r"\.{3}$")
_TRAILING_COMMA = re.compile(r",\s*$")


def fix_truncated(text: str) -> str:
    result = text.rstrip()
    result = _ELLIPSIS_UC.sub("", result).rstrip()
    result = _ELLIPSIS_DOTS.sub("", result).rstrip()
    result = _TRAILING_COMMA.sub("", result).rstrip()
    if result.rfind('"') != -1:
        quote_count = 0
        i = 0
        n = len(result)
        while i < n:
            if result[i] == "\\":
                i += 2
                continue
            if result[i] == '"':
                quote_count += 1
            i += 1
        if quote_count % 2 == 1:
            result = result + '"'
    return result
