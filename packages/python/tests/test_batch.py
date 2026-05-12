from output_guard import repair_batch, validate_batch


def test_validate_batch() -> None:
    results = validate_batch(['{"a":1}', '{"b":2}'])
    assert len(results) == 2
    assert all(r.valid for r in results)


def test_repair_batch_all_ok() -> None:
    results = repair_batch(['{"a":1,}', '{"b":2}'])
    assert len(results) == 2
    # All should be RepairResult objects (not dicts with "error")
    assert all(not isinstance(r, dict) for r in results)


def test_repair_batch_with_errors() -> None:
    results = repair_batch([":::nope:::", '{"a":1}'])
    assert isinstance(results[0], dict) and "error" in results[0]
    assert not isinstance(results[1], dict)


def test_empty_batch() -> None:
    assert validate_batch([]) == []
    assert repair_batch([]) == []
