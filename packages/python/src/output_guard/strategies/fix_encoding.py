"""fix-encoding: Replace BOM, surrogate code points, and GPT tokeniser artefacts.

Mirror of packages/ts/src/strategies/fix-encoding.ts. Runs FIRST.
"""

from __future__ import annotations

import re

_LONE_SURROGATE = re.compile(r"[\ud800-\udfff]")


def fix_encoding(text: str) -> str:
    result = text
    if result and ord(result[0]) == 0xFEFF:
        result = result[1:]
    result = result.replace("Ċ", "\n").replace("Ġ", " ")
    result = _LONE_SURROGATE.sub("�", result)
    return result
