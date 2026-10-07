"""
Testes básicos da JRO.

JRO 0.3.0
JSON Reformulated Object
"""

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
        "games": [
            "Pokémon",
            "Minecraft",
        ],
        "active": True,
        "nothing": None,
    }

    encoded = jro.dumps(data)
    decoded = jro.loads(encoded)

    assert decoded == data


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
    data = {
        "z": 1,
        "a": 2,
        "m": 3,
    }

    result = jro.dumps(
        data,
        sort_keys=True,
    )

    assert result == '{"a":2,"m":3,"z":1}'
