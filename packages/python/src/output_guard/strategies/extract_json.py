"""extract-json: Extract first balanced JSON object/array from surrounding text.

Mirror of packages/ts/src/strategies/extract-json.ts.
"""

from __future__ import annotations


def extract_json(text: str) -> str:
    t = text.strip()
    if t.startswith("{") or t.startswith("["):
        return text
    obj_idx = t.find("{")
    arr_idx = t.find("[")
    if obj_idx == -1 and arr_idx == -1:
        return text
    if obj_idx == -1:
        start_idx, open_ch, close_ch = arr_idx, "[", "]"
    elif arr_idx == -1:
        start_idx, open_ch, close_ch = obj_idx, "{", "}"
    elif arr_idx < obj_idx:
        start_idx, open_ch, close_ch = arr_idx, "[", "]"
    else:
        start_idx, open_ch, close_ch = obj_idx, "{", "}"

    depth = 0
    in_string = False
    escaped = False
    for i in range(start_idx, len(t)):
        ch = t[i]
        if escaped:
            escaped = False
            continue
        if ch == "\\":
            escaped = True
            continue
        if ch == '"':
            in_string = not in_string
            continue
        if in_string:
            continue
        if ch == open_ch:
            depth += 1
        elif ch == close_ch:
            depth -= 1
            if depth == 0:
                return t[start_idx : i + 1]
    return text
