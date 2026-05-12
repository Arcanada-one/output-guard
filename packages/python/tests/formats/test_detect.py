from output_guard.formats.detect import detect_format


def test_toml_header() -> None:
    assert detect_format("[section]\nx=1") == "toml"


def test_toml_kv() -> None:
    assert detect_format("x = 1") == "toml"


def test_yaml_doc_start() -> None:
    assert detect_format("---\na: 1") == "yaml"


def test_yaml_kv() -> None:
    assert detect_format("key: value") == "yaml"


def test_json_object() -> None:
    assert detect_format('{"a":1}') == "json"


def test_json_array() -> None:
    assert detect_format("[1,2]") == "json"


def test_python_token() -> None:
    assert detect_format("True or False") == "python"


def test_python_tuple() -> None:
    assert detect_format("(1, 2)") == "python"


def test_default_json() -> None:
    assert detect_format("just text") == "json"
