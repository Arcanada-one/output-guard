"""JSON Schema adapter: wrap a JSON Schema dict as ``SchemaAdapter``.

Mirror of packages/ts/src/adapters/ajv.ts (optional adapter).
"""

from __future__ import annotations

from typing import Any

from jsonschema import Draft202012Validator

from ..results import ValidationResult
from .pydantic_ import SchemaAdapter


def jsonschema_adapter(schema: dict[str, Any]) -> SchemaAdapter[Any]:
    validator = Draft202012Validator(schema)

    def _validate(data: Any) -> ValidationResult:
        errors = sorted(validator.iter_errors(data), key=lambda e: list(e.absolute_path))
        if not errors:
            return ValidationResult(valid=True, data=data)
        messages = [
            f"{'/'.join(str(p) for p in err.absolute_path) or 'root'}: {err.message}"
            for err in errors
        ]
        return ValidationResult(valid=False, errors=messages)

    return SchemaAdapter(validate=_validate)
