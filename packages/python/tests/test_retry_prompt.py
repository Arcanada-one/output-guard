from output_guard.retry_prompt import Message, RetryPromptOptions, retry_prompt


def test_minimal_prompt() -> None:
    result = retry_prompt(RetryPromptOptions(previous_response="{bad}"))
    assert "Previous response" in result.prompt
    assert "{bad}" in result.prompt
    assert result.detected_errors == []
    assert result.pointer_paths == []


def test_errors_block() -> None:
    result = retry_prompt(
        RetryPromptOptions(previous_response='{"a":1}', errors=["/a: expected string"])
    )
    assert "Errors detected" in result.prompt
    assert "/a: expected string" in result.prompt


def test_pointer_extraction() -> None:
    result = retry_prompt(
        RetryPromptOptions(
            previous_response="x",
            errors=["/items/0: missing", "/items/1: bad"],
        )
    )
    assert "/items/0" in result.pointer_paths
    assert "/items/1" in result.pointer_paths


def test_pointer_deduplication() -> None:
    result = retry_prompt(
        RetryPromptOptions(
            previous_response="x",
            errors=["/a: e1", "/a: e2"],
        )
    )
    assert result.pointer_paths.count("/a") == 1


def test_schema_block() -> None:
    result = retry_prompt(
        RetryPromptOptions(previous_response="x", schema='{"type":"object"}')
    )
    assert "Expected schema" in result.prompt
    assert '"type":"object"' in result.prompt


def test_history_block() -> None:
    result = retry_prompt(
        RetryPromptOptions(
            previous_response="x",
            history=[
                Message(role="user", content="hello"),
                Message(role="assistant", content="hi"),
            ],
        )
    )
    assert "Conversation history" in result.prompt
    assert "user: hello" in result.prompt
