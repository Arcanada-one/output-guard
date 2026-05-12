"""guarded_generate: Async wrapper around a generate callable with repair + retry.

Mirror of packages/ts/src/guarded-generate.ts.

F4 compliance: ``asyncio.timeout`` per-call (default 30s). ``MAX_RETRIES=3`` hard cap.
"""

from __future__ import annotations

import asyncio
import inspect
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from typing import Any

from pydantic import BaseModel

from .adapters.pydantic_ import SchemaAdapter, pydantic_adapter
from .constants import DEFAULT_TIMEOUT_MS, MAX_RETRIES
from .errors import GuardedGenerationError
from .orchestrator import repair
from .results import Format, GuardedGenerateResult, RepairReport
from .retry_prompt import Message, RetryPromptOptions, retry_prompt

GenerateCallable = Callable[..., Awaitable[str]] | Callable[..., str]


@dataclass(slots=True)
class GuardedGenerateOptions:
    generate: GenerateCallable
    prompt: str
    format: Format = "auto"
    schema: SchemaAdapter[Any] | type[BaseModel] | None = None
    max_retries: int = MAX_RETRIES
    timeout_ms: int = DEFAULT_TIMEOUT_MS
    history: list[Message] = field(default_factory=list)


def _resolve_schema(
    schema: SchemaAdapter[Any] | type[BaseModel] | None,
) -> SchemaAdapter[Any] | None:
    if schema is None:
        return None
    if isinstance(schema, SchemaAdapter):
        return schema
    return pydantic_adapter(schema)


async def _invoke(
    generate: GenerateCallable,
    prompt: str,
    history: list[Message] | None,
    timeout_ms: int,
) -> str:
    async def runner() -> str:
        if inspect.iscoroutinefunction(generate):
            try:
                value: Any = await generate(prompt, history)
            except TypeError:
                value = await generate(prompt)
            assert isinstance(value, str)
            return value
        result: Any = generate(prompt, history) if _accepts_history(generate) else generate(prompt)
        if inspect.isawaitable(result):
            awaited: Any = await result
            assert isinstance(awaited, str)
            return awaited
        assert isinstance(result, str)
        return result

    return await asyncio.wait_for(runner(), timeout=timeout_ms / 1000)


def _accepts_history(fn: Callable[..., Any]) -> bool:
    try:
        sig = inspect.signature(fn)
    except (TypeError, ValueError):
        return False
    return len(sig.parameters) >= 2


async def guarded_generate(opts: GuardedGenerateOptions) -> GuardedGenerateResult:
    """Call ``opts.generate``, validate/repair output, retry with correction prompt on failure."""
    adapter = _resolve_schema(opts.schema)
    history: list[Message] = list(opts.history)
    last_error: BaseException | None = None
    last_response = ""

    for attempt in range(opts.max_retries + 1):
        current_prompt = (
            opts.prompt
            if attempt == 0
            else retry_prompt(
                RetryPromptOptions(
                    previous_response=last_response,
                    errors=[str(last_error)] if last_error is not None else [],
                    history=history,
                )
            ).prompt
        )

        try:
            raw = await _invoke(opts.generate, current_prompt, history or None, opts.timeout_ms)
        except (TimeoutError, Exception) as e:
            raise GuardedGenerationError(
                f"Generation failed on attempt {attempt}: {e}", attempt, e
            ) from e

        last_response = raw
        history.append(Message(role="user", content=current_prompt))
        history.append(Message(role="assistant", content=raw))

        try:
            repair_result = repair(raw, opts.format, adapter)
            report = RepairReport(
                strategies_applied=list(repair_result.strategies_applied),
                retries=attempt,
                final_valid=True,
                pass_=repair_result.pass_,
            )
            return GuardedGenerateResult(data=repair_result.data, report=report)
        except Exception as e:
            last_error = e

    raise GuardedGenerationError(
        f"Exhausted {opts.max_retries} retries without valid output",
        opts.max_retries,
        last_error,
    )
