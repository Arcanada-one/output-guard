"""fix-newlines: Replace literal newlines inside JSON string values with \\n.

Mirror of packages/ts/src/strategies/fix-newlines.ts. Runs LAST.
"""

from __future__ import annotations


def fix_newlines(text: str) -> str:
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
        if ch == "\\":
            out.append(ch)
            i += 1
            if i < n:
                out.append(text[i])
                i += 1
            continue
        if ch == '"':
            in_string = False
            out.append(ch)
            i += 1
            continue
        if ch == "\n":
            out.append("\\n")
            i += 1
            continue
        if ch == "\r":
            out.append("\\r")
            i += 1
            continue
        out.append(ch)
        i += 1
    return "".join(out)
