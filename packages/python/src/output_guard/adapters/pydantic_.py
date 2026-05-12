"""Pydantic adapter: wrap a ``pydantic.BaseModel`` as ``SchemaAdapter``.

Mirror of packages/ts/src/adapters/zod.ts. Primary adapter.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ValidationError

from ..results import ValidationResult

T = TypeVar("T", bound=BaseModel)


class SchemaAdapter(Generic[T]):
    __slots__ = ("validate",)

    def __init__(self, validate: Callable[[Any], ValidationResult]) -> None:
        self.validate = validate


def pydantic_adapter(model: type[T]) -> SchemaAdapter[T]:
    def _validate(data: Any) -> ValidationResult:
        try:
            instance = model.model_validate(data)
            return ValidationResult(valid=True, data=instance)
        except ValidationError as e:
            errors = [
                f"{'/'.join(str(p) for p in err['loc']) or 'root'}: {err['msg']}"
                for err in e.errors()
            ]
            return ValidationResult(valid=False, errors=errors)

    return SchemaAdapter(validate=_validate)
