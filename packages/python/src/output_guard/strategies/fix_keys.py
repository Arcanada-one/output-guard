"""fix-keys: Quote bare (unquoted) object keys.

Mirror of packages/ts/src/strategies/fix-keys.ts.
"""

from __future__ import annotations

import re

_BARE_KEY = re.compile(r"([{,\n\r]\s*)([A-Za-z_$][\w$]*)(\s*):")


def fix_keys(text: str) -> str:
    return _BARE_KEY.sub(r'\1"\2"\3:', text)
