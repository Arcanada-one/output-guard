import pytest
from pydantic import BaseModel

from output_guard import OutputGuard, SchemaValidationError


class _Doc(BaseModel):
    a: int


def test_default_format() -> None:
    g = OutputGuard()
    r = g.repair('{"a":1}')
    assert r.data == {"a": 1}


def test_with_schema() -> None:
    g = OutputGuard(schema=_Doc)
    r = g.repair('{"a":42}')
    assert isinstance(r.data, _Doc)


def test_schema_rejection() -> None:
    g = OutputGuard(schema=_Doc)
    with pytest.raises(SchemaValidationError):
        g.repair('{"a": "not-int"}')


def test_validate_method() -> None:
    g = OutputGuard()
    v = g.validate('{"a":1}')
    assert v.valid is True


@pytest.mark.asyncio
async def test_guarded_success() -> None:
    g = OutputGuard(schema=_Doc)

    async def gen(_prompt: str, _history: object = None) -> str:
        return '{"a": 7}'

    result = await g.guarded(gen, "prompt")
    assert isinstance(result.data, _Doc)
    assert result.report.retries == 0
    assert result.report.final_valid is True


@pytest.mark.asyncio
async def test_guarded_retry_then_success() -> None:
    g = OutputGuard(schema=_Doc, max_retries=2)
    calls = {"n": 0}

    async def gen(_prompt: str, _history: object = None) -> str:
        calls["n"] += 1
        return '{"a": "bad"}' if calls["n"] == 1 else '{"a": 5}'

    result = await g.guarded(gen, "prompt")
    assert isinstance(result.data, _Doc)
    assert result.report.retries == 1
