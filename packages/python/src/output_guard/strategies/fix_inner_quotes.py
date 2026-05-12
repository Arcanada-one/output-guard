"""fix-inner-quotes: Escape unescaped double-quotes inside JSON string values.

Mirror of packages/ts/src/strategies/fix-inner-quotes.ts.
"""

from __future__ import annotations


def fix_inner_quotes(text: str) -> str:
    out: list[str] = []
    in_string = False
    i = 0
    n = len(text)
    while i < n:
        ch = text[i]
        if not in_string:
            if ch == '"':
                in_string = True
                out.append(ch)
                i += 1
                continue
            out.append(ch)
            i += 1
            continue
        if ch == "\\":
            out.append(ch)
            i += 1
            if i < n:
                out.append(text[i])
                i += 1
            continue
        if ch == '"':
            j = i + 1
            while j < n and text[j] in (" ", "\t"):
                j += 1
            nxt = text[j] if j < n else None
            is_closer = nxt in (":", ",", "}", "]", None) or j >= n
            if is_closer:
                in_string = False
                out.append(ch)
            else:
                out.append('\\"')
            i += 1
            continue
        out.append(ch)
        i += 1
    return "".join(out)
