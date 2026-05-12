"""fix-quotes: Normalise smart quotes and convert single-quoted strings to double.

Mirror of packages/ts/src/strategies/fix-quotes.ts.
"""

from __future__ import annotations

import re

_SMART_OPEN = re.compile(r"[‘‛‹]")
_SMART_CLOSE = re.compile(r"[’›]")
_SMART_DQUOTE = re.compile(r"[“”„‟«»]")


def fix_quotes(text: str) -> str:
    result = _SMART_OPEN.sub("'", text)
    result = _SMART_CLOSE.sub("'", result)
    result = _SMART_DQUOTE.sub('"', result)

    out: list[str] = []
    i = 0
    n = len(result)
    while i < n:
        ch = result[i]
        if ch == "'":
            out.append('"')
            i += 1
            while i < n:
                c = result[i]
                if c == "\\":
                    nxt = result[i + 1] if i + 1 < n else ""
                    if nxt == "'":
                        out.append("'")
                        i += 2
                        continue
                    out.append(result[i] if i < n else "")
                    i += 1
                    if i < n:
                        out.append(result[i])
                        i += 1
                    continue
                if c == "'":
                    out.append('"')
                    i += 1
                    break
                if c == '"':
                    out.append('\\"')
                    i += 1
                    continue
                out.append(c)
                i += 1
        else:
            out.append(ch)
            i += 1
    return "".join(out)
