"""
Testes de comentários da JRO.

JRO 0.3.0
JSON Reformulated Object
"""

import jro


def test_single_line_comment():
    text = """
    {
        // Nome do usuário
        "name": "DrakkZ"
    }
    """

    result = jro.loads(text)

    assert result == {
        "name": "DrakkZ"
    }


def test_inline_comment():
    text = """
    {
        "name": "DrakkZ", // Nome
        "age": 10 // Idade
    }
    """

    result = jro.loads(text)

    assert result == {
        "name": "DrakkZ",
        "age": 10,
    }


def test_comment_between_values():
    text = """
    {
        "name": "DrakkZ",

        // Jogos favoritos
        "games": [
            "Pokémon",
            // Segundo jogo
            "Minecraft"
        ]
    }
    """

    result = jro.loads(text)

    assert result == {
        "name": "DrakkZ",
        "games": [
            "Pokémon",
            "Minecraft",
        ],
    }


def test_only_comment():
    text = """
    // Este arquivo não possui dados.
    """

    # Atualmente o JRO exige um valor principal.
    # O teste documenta esse comportamento.
    try:
        jro.loads(text)
    except Exception:
        assert True
    else:
        assert False
