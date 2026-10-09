"""JRO Parser
==========

Transforma tokens JRO em estruturas Python.

JRO 0.3.0
JSON Reformulated Object
"""

from __future__ import annotations

from typing import Any

from .lexer import Lexer, LexerError, Token, TokenType


class ParserError(Exception):
    """Erro encontrado durante o parsing de JRO."""


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.position = 0

    def parse(self) -> Any:
        """Interpreta os tokens e retorna uma estrutura Python."""

        value = self._parse_value()

        if self.current.type != TokenType.EOF:
            self._error(
                "Conteúdo inesperado após o valor principal."
            )

        return value

    @property
    def current(self) -> Token:
        """Token atualmente sendo analisado."""

        return self.tokens[self.position]

    def _advance(self) -> Token:
        """Avança para o próximo token."""

        token = self.current

        if self.position < len(self.tokens) - 1:
            self.position += 1

        return token

    def _match(self, token_type: TokenType) -> bool:
        """Verifica se o token atual possui determinado tipo."""

        if self.current.type == token_type:
            self._advance()
            return True

        return False

    def _expect(self, token_type: TokenType):
        """Exige que o token atual seja de determinado tipo."""

        if self.current.type != token_type:
            self._error(
                f"Esperado {token_type.name}, "
                f"mas encontrado {self.current.type.name}."
            )

        return self._advance()

    def _parse_value(self) -> Any:
        """Analisa um valor JRO."""

        token = self.current

        if token.type == TokenType.LEFT_BRACE:
            return self._parse_object()

        if token.type == TokenType.LEFT_BRACKET:
            return self._parse_array()

        if token.type == TokenType.STRING:
            self._advance()
            return token.value

        if token.type == TokenType.NUMBER:
            self._advance()
            return token.value

        if token.type == TokenType.TRUE:
            self._advance()
            return True

        if token.type == TokenType.FALSE:
            self._advance()
            return False

        if token.type == TokenType.NULL:
            self._advance()
            return None

        self._error(
            f"Valor inesperado: {token.type.name}."
        )

    def _parse_object(self) -> dict[str, Any]:
        """Analisa um objeto JRO."""

        self._expect(TokenType.LEFT_BRACE)

        result: dict[str, Any] = {}

        # Objeto vazio
        if self._match(TokenType.RIGHT_BRACE):
            return result

        while True:
            key = self._expect(TokenType.STRING)

            self._expect(TokenType.COLON)

            value = self._parse_value()

            result[key.value] = value

            if self._match(TokenType.RIGHT_BRACE):
                break

            self._expect(TokenType.COMMA)

        return result

    def _parse_array(self) -> list[Any]:
        """Analisa um array JRO."""

        self._expect(TokenType.LEFT_BRACKET)

        result: list[Any] = []

        # Array vazio
        if self._match(TokenType.RIGHT_BRACKET):
            return result

        while True:
            result.append(self._parse_value())

            if self._match(TokenType.RIGHT_BRACKET):
                break

            self._expect(TokenType.COMMA)

        return result

    def _error(self, message: str):
        """Gera um erro com a posição atual."""

        token = self.current

        raise ParserError(
            f"{message} "
            f"(posição {token.position})"
        )


def parse(text: str) -> Any:
    """
    Converte texto JRO em uma estrutura Python.
    """

    try:
        tokens = Lexer(text).tokenize()
    except LexerError as error:
        raise ParserError(str(error)) from error

    return Parser(tokens).parse()
