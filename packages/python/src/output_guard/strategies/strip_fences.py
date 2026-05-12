"""strip-fences: Remove markdown code fences wrapping JSON/YAML/TOML/etc.

Mirror of packages/ts/src/strategies/strip-fences.ts.
"""

from __future__ import annotations

import re

_FENCE = re.compile(r"^```[\w-]*\r?\n([\s\S]*?)\r?\n```\s*$", re.IGNORECASE)
_FENCE_INLINE = re.compile(r"^```[\w-]*\r?\n([\s\S]*?)```\s*$", re.IGNORECASE)


def strip_fences(text: str) -> str:
    trimmed = text.strip()
    match = _FENCE.match(trimmed)
    if match is not None:
        return match.group(1).strip()
    inline = _FENCE_INLINE.match(trimmed)
    if inline is not None:
        return inline.group(1).strip()
    return text
