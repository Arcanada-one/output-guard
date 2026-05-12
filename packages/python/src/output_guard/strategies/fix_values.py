"""fix-values: Replace non-standard JSON values with null.

Mirror of packages/ts/src/strategies/fix-values.ts.
"""

from __future__ import annotations

import re

_NEG_INF = re.compile(r":\s*-Infinity\b")
_POS_INF = re.compile(r":\s*Infinity\b")
_NAN = re.compile(r":\s*NaN\b")
_UNDEF = re.compile(r":\s*undefined\b")


def fix_values(text: str) -> str:
    result = _NEG_INF.sub(": null", text)
    result = _POS_INF.sub(": null", result)
    result = _NAN.sub(": null", result)
    result = _UNDEF.sub(": null", result)
    return result
