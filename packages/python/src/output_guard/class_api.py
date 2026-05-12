"""OutputGuard: stateful class wrapper around the functional API.

Mirror of packages/ts/src/class.ts.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel

from .adapters.pydantic_ import SchemaAdapter, pydantic_adapter
from .constants import DEFAULT_TIMEOUT_MS, MAX_RETRIES
from .guarded_generate import GenerateCallable, GuardedGenerateOptions, guarded_generate
from .orchestrator import repair, validate
from .results import Format, GuardedGenerateResult, RepairResult, ValidationResult


class OutputGuard:
    __slots__ = ("_adapter", "_format", "_max_retries", "_schema", "_timeout_ms")

    def __init__(
        self,
        format: Format = "auto",
        schema: SchemaAdapter[Any] | type[BaseModel] | None = None,
        max_retries: int = MAX_RETRIES,
        timeout_ms: int = DEFAULT_TIMEOUT_MS,
    ) -> None:
        self._format = format
        self._schema = schema
        self._adapter: SchemaAdapter[Any] | None = self._resolve(schema)
        self._max_retries = max_retries
        self._timeout_ms = timeout_ms

    @staticmethod
    def _resolve(
        schema: SchemaAdapter[Any] | type[BaseModel] | None,
    ) -> SchemaAdapter[Any] | None:
        if schema is None:
            return None
        if isinstance(schema, SchemaAdapter):
            return schema
        return pydantic_adapter(schema)

    def validate(self, text: str) -> ValidationResult:
        return validate(text, self._format, self._adapter)

    def repair(self, text: str) -> RepairResult:
        return repair(text, self._format, self._adapter)

    async def guarded(
        self,
        generate: GenerateCallable,
        prompt: str,
        *,
        format: Format | None = None,
        schema: SchemaAdapter[Any] | type[BaseModel] | None = None,
        max_retries: int | None = None,
        timeout_ms: int | None = None,
    ) -> GuardedGenerateResult:
        resolved_schema = schema if schema is not None else self._schema
        opts = GuardedGenerateOptions(
            generate=generate,
            prompt=prompt,
            format=format if format is not None else self._format,
            schema=resolved_schema,
            max_retries=max_retries if max_retries is not None else self._max_retries,
            timeout_ms=timeout_ms if timeout_ms is not None else self._timeout_ms,
        )
        return await guarded_generate(opts)
