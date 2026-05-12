"""Strategy barrel + CANONICAL_ORDER.

Mirror of packages/ts/src/strategies/index.ts. Order MUST match TS for parity.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Final

from .extract_json import extract_json
from .fix_booleans import fix_booleans
from .fix_closers import fix_closers
from .fix_commas import fix_commas
from .fix_ellipsis import fix_ellipsis
from .fix_encoding import fix_encoding
from .fix_inner_quotes import fix_inner_quotes
from .fix_keys import fix_keys
from .fix_newlines import fix_newlines
from .fix_quotes import fix_quotes
from .fix_truncated import fix_truncated
from .fix_unicode import fix_unicode
from .fix_values import fix_values
from .remove_comments import remove_comments
from .strip_fences import strip_fences

Strategy = Callable[[str], str]

STRATEGY_NAMES: Final[tuple[str, ...]] = (
    "fix-encoding",
    "strip-fences",
    "extract-json",
    "remove-comments",
    "fix-commas",
    "fix-quotes",
    "fix-keys",
    "fix-values",
    "fix-booleans",
    "fix-truncated",
    "fix-ellipsis",
    "fix-unicode",
    "fix-inner-quotes",
    "fix-closers",
    "fix-newlines",
)

CANONICAL_ORDER: Final[tuple[tuple[str, Strategy], ...]] = (
    ("fix-encoding", fix_encoding),
    ("strip-fences", strip_fences),
    ("extract-json", extract_json),
    ("remove-comments", remove_comments),
    ("fix-commas", fix_commas),
    ("fix-quotes", fix_quotes),
    ("fix-keys", fix_keys),
    ("fix-values", fix_values),
    ("fix-booleans", fix_booleans),
    ("fix-truncated", fix_truncated),
    ("fix-ellipsis", fix_ellipsis),
    ("fix-unicode", fix_unicode),
    ("fix-inner-quotes", fix_inner_quotes),
    ("fix-closers", fix_closers),
    ("fix-newlines", fix_newlines),
)

__all__ = [
    "CANONICAL_ORDER",
    "STRATEGY_NAMES",
    "Strategy",
    "extract_json",
    "fix_booleans",
    "fix_closers",
    "fix_commas",
    "fix_ellipsis",
    "fix_encoding",
    "fix_inner_quotes",
    "fix_keys",
    "fix_newlines",
    "fix_quotes",
    "fix_truncated",
    "fix_unicode",
    "fix_values",
    "remove_comments",
    "strip_fences",
]
