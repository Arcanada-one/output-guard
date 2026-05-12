"""detect-format: heuristic format detection.

Mirror of packages/ts/src/formats/detect.ts.
"""

from __future__ import annotations

import re
from typing import Literal

_TOML_HEADER = re.compile(r"^\[[\w.]+\]")
_TOML_KV = re.compile(r"^[\w-]+\s*=\s*")
_YAML_KV = re.compile(r"^[\w-]+\s*:\s*")
_PYTHON_TOKEN = re.compile(r"\bTrue\b|\bFalse\b|\bNone\b")

ConcreteFormat = Literal["json", "yaml", "toml", "python"]


def detect_format(text: str) -> ConcreteFormat:
    trimmed = text.lstrip()
    if _TOML_HEADER.match(trimmed) or _TOML_KV.match(trimmed):
        return "toml"
    if trimmed.startswith("---") or (
        _YAML_KV.match(trimmed) and not trimmed.startswith("{")
    ):
        return "yaml"
    if trimmed.startswith("{") or trimmed.startswith("["):
        return "json"
    if trimmed.startswith("(") or _PYTHON_TOKEN.search(trimmed):
        return "python"
    return "json"
