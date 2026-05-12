"""fix-closers: Append missing closing braces/brackets to balance the structure.

Mirror of packages/ts/src/strategies/fix-closers.ts.
"""

from __future__ import annotations


def fix_closers(text: str) -> str:
    stack: list[str] = []
    in_string = False
    escaped = False
    for ch in text:
        if escaped:
            escaped = False
            continue
        if ch == "\\" and in_string:
            escaped = True
            continue
        if ch == '"':
            in_string = not in_string
            continue
        if in_string:
            continue
        if ch == "{":
            stack.append("}")
        elif ch == "[":
            stack.append("]")
        elif ch in ("}", "]") and stack and stack[-1] == ch:
            stack.pop()
    return text + "".join(reversed(stack))
