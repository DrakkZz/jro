"""
Testes do lexer da JRO.

JRO 0.2.0
JSON V2
"""

import pytest

from jro.lexer import Lexer, LexerError, TokenType


def test_basic_tokens():
    tokens = Lexer(
        '{"name":"DrakkZ","age":10}'
    ).tokenize()

    assert tokens[0].type == TokenType.LEFT_BRACE

    assert tokens[1].type == TokenType.STRING
    assert tokens[1].value == "name"

    assert tokens[2].type == TokenType.COLON

    assert tokens[3].type == TokenType.STRING
    assert tokens[3].value == "DrakkZ"

    assert tokens[4].type == TokenType.COMMA

    assert tokens[5].type == TokenType.STRING
    assert tokens[5].value == "age"

    assert tokens[6].type == TokenType.COLON

    assert tokens[7].type == TokenType.NUMBER
    assert tokens[7].value == 10

    assert tokens[8].type == TokenType.RIGHT_BRACE
    assert tokens[9].type == TokenType.EOF


def test_booleans():
    tokens = Lexer(
        "true false"
    ).tokenize()

    assert tokens[0].type == TokenType.TRUE
    assert tokens[0].value is True

    assert tokens[1].type == TokenType.FALSE
    assert tokens[1].value is False


def test_null():
    tokens = Lexer("null").tokenize()

    assert tokens[0].type == TokenType.NULL
    assert tokens[0].value is None


def test_numbers():
    tokens = Lexer(
        "0 -42 3.14 -9.5"
    ).tokenize()

    assert tokens[0].value == 0
    assert tokens[1].value == -42
    assert tokens[2].value == 3.14
    assert tokens[3].value == -9.5


def test_comments_are_ignored():
    tokens = Lexer(
        '{ // comentário\n "name": "DrakkZ" }'
    ).tokenize()

    values = [
        token.value
        for token in tokens
        if token.type != TokenType.EOF
    ]

    assert values == [
        "{",
        "name",
        ":",
        "DrakkZ",
        "}",
    ]


def test_invalid_keyword():
    with pytest.raises(LexerError):
        Lexer("truefoo").tokenize()


def test_invalid_false_keyword():
    with pytest.raises(LexerError):
        Lexer("false123").tokenize()


def test_invalid_null_keyword():
    with pytest.raises(LexerError):
        Lexer("null_value").tokenize()


def test_invalid_number():
    with pytest.raises(LexerError):
        Lexer("123abc").tokenize()


def test_invalid_decimal():
    with pytest.raises(LexerError):
        Lexer("3.").tokenize()


def test_unexpected_character():
    with pytest.raises(LexerError):
        Lexer("@").tokenize()


def test_unterminated_string():
    with pytest.raises(LexerError):
        Lexer('"DrakkZ').tokenize()
