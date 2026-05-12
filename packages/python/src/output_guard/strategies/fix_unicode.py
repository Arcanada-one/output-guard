"""fix-unicode: Sanitize broken \\uXXXX escape sequences.

Mirror of packages/ts/src/strategies/fix-unicode.ts. Walks char-by-char (not
regex) for boundary-edge robustness; parity fixture required for M3.
"""

from __future__ import annotations

_HEX = set("0123456789abcdefABCDEF")


def fix_unicode(text: str) -> str:
    out: list[str] = []
    i = 0
    n = len(text)
    while i < n:
        if text[i] == "\\" and i + 1 < n:
            if text[i + 1] == "u":
                hex_slice = text[i + 2 : i + 6]
                if len(hex_slice) == 4 and all(c in _HEX for c in hex_slice):
                    out.append(text[i : i + 6])
                    i += 6
                else:
                    hex_count = 0
                    while (
                        hex_count < 4
                        and i + 2 + hex_count < n
                        and text[i + 2 + hex_count] in _HEX
                    ):
                        hex_count += 1
                    out.append("\\uFFFD")
                    i += 2 + hex_count
                continue
            out.append(text[i])
            if i + 1 < n:
                out.append(text[i + 1])
            i += 2
            continue
        out.append(text[i])
        i += 1
    return "".join(out)
