"""json format: parse JSON, falling back to json-repair on syntax error.

Mirror of packages/ts/src/formats/json.ts.
"""

from __future__ import annotations

import json
from typing import Any

from json_repair import repair_json as _json_repair

from ..errors import ParseError


def parse_json(text: str) -> Any:
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        try:
            repaired = _json_repair(text)
            return json.loads(repaired)
        except (json.JSONDecodeError, ValueError) as e:
            raise ParseError(f"JSON parse failed: {e}", e) from e


def repair_json(text: str) -> str:
    try:
        return _json_repair(text)
    except (ValueError, TypeError) as e:
        raise ParseError(f"json-repair failed: {e}", e) from e
