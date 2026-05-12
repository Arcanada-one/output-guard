"""toml format: parse TOML via stdlib tomllib (Python 3.11+).

Mirror of packages/ts/src/formats/toml.ts.
"""

from __future__ import annotations

import tomllib
from typing import Any

from ..errors import ParseError


def parse_toml(text: str) -> Any:
    try:
        return tomllib.loads(text)
    except tomllib.TOMLDecodeError as e:
        raise ParseError(f"TOML parse failed: {e}", e) from e
