import pytest
from pydantic import BaseModel

from output_guard import GuardedGenerationError, guarded_generate
from output_guard.guarded_generate import GuardedGenerateOptions


class _Doc(BaseModel):
    a: int


@pytest.mark.asyncio
async def test_first_attempt_success() -> None:
    async def gen(_prompt: str, _history: object = None) -> str:
        return '{"a": 1}'

    result = await guarded_generate(
        GuardedGenerateOptions(generate=gen, prompt="p", schema=_Doc)
    )
    assert result.report.retries == 0
    assert isinstance(result.data, _Doc)


@pytest.mark.asyncio
async def test_exhaustion_raises() -> None:
    async def gen(_prompt: str, _history: object = None) -> str:
        return '{"a": "always-bad"}'

    with pytest.raises(GuardedGenerationError):
        await guarded_generate(
            GuardedGenerateOptions(
                generate=gen, prompt="p", schema=_Doc, max_retries=1
            )
        )


@pytest.mark.asyncio
async def test_pass_field_propagated() -> None:
    async def gen(_prompt: str, _history: object = None) -> str:
        return '{"a":1,}'

    result = await guarded_generate(
        GuardedGenerateOptions(generate=gen, prompt="p", schema=_Doc)
    )
    assert result.report.pass_ == "A"
    assert "fix-commas" in result.report.strategies_applied


@pytest.mark.asyncio
async def test_timeout_triggers_error() -> None:
    import asyncio

    async def slow_gen(_prompt: str, _history: object = None) -> str:
        await asyncio.sleep(0.5)
        return '{"a":1}'

    with pytest.raises(GuardedGenerationError):
        await guarded_generate(
            GuardedGenerateOptions(
                generate=slow_gen,
                prompt="p",
                schema=_Doc,
                timeout_ms=50,
                max_retries=0,
            )
        )
