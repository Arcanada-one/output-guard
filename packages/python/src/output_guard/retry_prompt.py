"""retry-prompt: Build a correction prompt with JSON-pointer-localised errors.

Mirror of packages/ts/src/retry-prompt.ts.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

_POINTER = re.compile(r"/[\w/\[\]]+")


@dataclass(frozen=True, slots=True)
class Message:
    role: str
    content: str


@dataclass(frozen=True, slots=True)
class RetryPromptOptions:
    previous_response: str
    schema: str | None = None
    errors: list[str] = field(default_factory=list)
    history: list[Message] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class RetryPromptResult:
    prompt: str
    detected_errors: list[str]
    pointer_paths: list[str]


def _extract_pointers(errors: list[str]) -> list[str]:
    pointers: list[str] = []
    for e in errors:
        matches = _POINTER.findall(e)
        pointers.extend(matches)
    seen: dict[str, None] = {}
    for p in pointers:
        seen.setdefault(p, None)
    return list(seen.keys())


def retry_prompt(opts: RetryPromptOptions) -> RetryPromptResult:
    errors = list(opts.errors)
    history = list(opts.history)
    pointer_paths = _extract_pointers(errors)

    error_block = (
        "\n\nErrors detected:\n" + "\n".join(f"{i + 1}. {e}" for i, e in enumerate(errors))
        if errors
        else ""
    )
    pointer_block = (
        "\n\nAffected fields: " + ", ".join(pointer_paths) if pointer_paths else ""
    )
    schema_block = (
        f"\n\nExpected schema:\n```\n{opts.schema}\n```" if opts.schema else ""
    )
    history_block = (
        "\n\nConversation history:\n"
        + "\n".join(f"{m.role}: {m.content}" for m in history)
        if history
        else ""
    )

    prompt = "".join(
        [
            "Your previous response could not be parsed or did not match the expected schema.",
            f"\n\nPrevious response:\n```\n{opts.previous_response}\n```",
            error_block,
            pointer_block,
            schema_block,
            history_block,
            "\n\nPlease provide a corrected response that is valid JSON "
            "(or the requested format) and matches the schema exactly.",
        ]
    )

    return RetryPromptResult(prompt=prompt, detected_errors=errors, pointer_paths=pointer_paths)
