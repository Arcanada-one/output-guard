from output_guard.adapters import jsonschema_adapter

_SCHEMA = {
    "type": "object",
    "properties": {"a": {"type": "integer"}, "b": {"type": "string"}},
    "required": ["a", "b"],
}


def test_valid() -> None:
    adapter = jsonschema_adapter(_SCHEMA)
    result = adapter.validate({"a": 1, "b": "x"})
    assert result.valid is True


def test_missing_required() -> None:
    adapter = jsonschema_adapter(_SCHEMA)
    result = adapter.validate({"a": 1})
    assert result.valid is False
    assert any("'b'" in e or "b" in e for e in result.errors)


def test_wrong_type() -> None:
    adapter = jsonschema_adapter(_SCHEMA)
    result = adapter.validate({"a": "no", "b": "x"})
    assert result.valid is False
