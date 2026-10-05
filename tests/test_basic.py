import jro


def test_dumps():
    data = {
        "name": "DrakkZ",
        "version": 1
    }

    result = jro.dumps(data)

    assert '"name": "DrakkZ"' in result
    assert '"version": 1' in result


def test_loads():
    text = '{"name": "DrakkZ", "version": 1}'

    result = jro.loads(text)

    assert result["name"] == "DrakkZ"
    assert result["version"] == 1


def test_roundtrip():
    data = {
        "name": "DrakkZ",
        "games": [
            "Pokémon",
            "Minecraft"
        ],
        "active": True,
        "nothing": None
    }

    encoded = jro.dumps(data)
    decoded = jro.loads(encoded)

    assert decoded == data
