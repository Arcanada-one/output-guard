"""fix-commas: Remove trailing commas before } and ].

Mirror of packages/ts/src/strategies/fix-commas.ts.
"""

from __future__ import annotations

import re

_TRAILING = re.compile(r",(\s*[}\]])")


def fix_commas(text: str) -> str:
    return _TRAILING.sub(r"\1", text)
