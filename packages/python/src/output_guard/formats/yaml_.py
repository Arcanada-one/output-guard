"""yaml format: parse YAML via PyYAML safe_load.

Mirror of packages/ts/src/formats/yaml.ts.
"""

from __future__ import annotations

from typing import Any

import yaml

from ..errors import ParseError


def parse_yaml(text: str) -> Any:
    try:
        return yaml.safe_load(text)
    except yaml.YAMLError as e:
        raise ParseError(f"YAML parse failed: {e}", e) from e
