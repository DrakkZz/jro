"""
Testes básicos da JRO.

JRO 0.3.0
JSON Reformulated Object
"""

import pytest
import jro


def test_dumps():
    data = {
        "name": "DrakkZ",
        "age": 10,
        "active": True,
    }

    result = jro.dumps(data)

    assert '"name":"DrakkZ"' in result
    assert '"age":10' in result
    assert '"active":true' in result


def test_loads():
    text = """
    {
        "name": "DrakkZ",
        "age": 10,
        "active": true,
        "nothing": null
    }
    """

    result = jro.loads(text)

    assert result["name"] == "DrakkZ"
    assert result["age"] == 10
    assert result["active"] is True
    assert result["nothing"] is None


def test_roundtrip():
    data = {
        "name": "DrakkZ",
        "age": 10,
        "games": ["Pokémon", "Minecraft"],
        "active": True,
        "nothing": None,
    }

    assert jro.loads(jro.dumps(data)) == data


def test_nested_objects():
    data = {
        "user": {
            "name": "DrakkZ",
            "settings": {
                "language": "pt-BR",
                "active": True,
            },
        },
    }

    assert jro.loads(jro.dumps(data)) == data


def test_nested_arrays():
    data = [
        [1, 2, 3],
        ["Pokémon", "Minecraft"],
        [True, False, None],
    ]

    assert jro.loads(jro.dumps(data)) == data


def test_dumps_sort_keys():
    data = {"z": 1, "a": 2, "m": 3}

    result = jro.dumps(data, sort_keys=True)

    assert result == '{"a":2,"m":3,"z":1}'


def test_indent_negative():
    with pytest.raises(ValueError):
        jro.dumps({"a": 1}, indent=-1)


def test_indent_boolean():
    with pytest.raises(TypeError):
        jro.dumps({"a": 1}, indent=True)


def test_indent_float():
    with pytest.raises(TypeError):
        jro.dumps({"a": 1}, indent=2.5)


def test_sort_keys_invalid_type():
    with pytest.raises(TypeError):
        jro.dumps({"a": 1}, sort_keys="sim")


def test_control_characters():
    value = "linha 1\nlinha 2\tfim\x01"
    encoded = jro.dumps(value)

    assert encoded == '"linha 1\\nlinha 2\\tfim\\u0001"'
    assert jro.loads(encoded) == value


def test_quotes_and_backslashes():
    value = 'texto com "aspas" e \\ barra'

    assert jro.loads(jro.dumps(value)) == value


def test_empty_containers():
    assert jro.dumps({}) == "{}"
    assert jro.dumps([]) == "[]"
    assert jro.loads("{}") == {}
    assert jro.loads("[]") == []


def test_non_finite_float_rejected():
    for value in (float("nan"), float("inf"), float("-inf")):
        with pytest.raises(jro.EncoderError):
            jro.dumps(value)


def test_non_string_keys_rejected():
    with pytest.raises(jro.EncoderError):
        jro.dumps({1: "valor"})


def test_unsupported_type_rejected():
    with pytest.raises(jro.EncoderError):
        jro.dumps({ "valor": {1, 2, 3} })


def test_circular_list_rejected():
    data = []
    data.append(data)

    with pytest.raises(jro.EncoderError, match="Referência circular"):
        jro.dumps(data)


def test_circular_dict_rejected():
    data = {}
    data["self"] = data

    with pytest.raises(jro.EncoderError, match="Referência circular"):
        jro.dumps(data)


def test_shared_reference_allowed():
    shared = {"value": 1}

    assert jro.dumps([shared, shared]) == (
        '[{"value":1},{"value":1}]'
    )
