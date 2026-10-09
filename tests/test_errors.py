"""
Testes de erros da JRO.

JRO 0.3.0
JSON Reformulated Object
"""

import pytest

import jro
from jro.lexer import LexerError
from jro.parser import ParserError


def test_unterminated_string():
    with pytest.raises(ParserError):
        jro.loads('{"name": "DrakkZ}')


def test_unexpected_character():
    with pytest.raises(ParserError):
        jro.loads('{"name": @}')


def test_missing_colon():
    with pytest.raises(ParserError):
        jro.loads('{"name" "DrakkZ"}')


def test_missing_value():
    with pytest.raises(ParserError):
        jro.loads('{"name":}')


def test_invalid_array():
    with pytest.raises(ParserError):
        jro.loads('[1, 2, ]')


def test_invalid_object():
    with pytest.raises(ParserError):
        jro.loads('{"name": "DrakkZ",}')


def test_extra_data():
    with pytest.raises(ParserError):
        jro.loads('true false')


def test_invalid_root():
    with pytest.raises(ParserError):
        jro.loads('{"name": "DrakkZ"')


def test_unsupported_encode_type():
    class CustomObject:
        pass

    with pytest.raises(jro.EncoderError):
        jro.dumps(CustomObject())
