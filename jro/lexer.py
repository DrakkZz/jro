"""
JRO Lexer
=========

Transforma texto JRO em tokens.

JRO 0.2.0
JSON V2
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto

import json


class TokenType(Enum):
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()

    LEFT_BRACKET = auto()
    RIGHT_BRACKET = auto()

    COLON = auto()
    COMMA = auto()

    STRING = auto()
    NUMBER = auto()

    TRUE = auto()
    FALSE = auto()
    NULL = auto()

    EOF = auto()


@dataclass
class Token:
    type: TokenType
    value: object
    position: int


class LexerError(Exception):
    """Erro encontrado durante a análise léxica."""


class Lexer:
    def __init__(self, text: str):
        self.text = text
        self.position = 0
        self.tokens: list[Token] = []

    def tokenize(self) -> list[Token]:
        while self.position < len(self.text):
            char = self.text[self.position]

            # Espaços, tabs e quebras de linha
            if char.isspace():
                self.position += 1
                continue

            # Comentário de linha
            if char == "/" and self._peek() == "/":
                self._skip_comment()
                continue

            # Objetos
            if char == "{":
                self._add(TokenType.LEFT_BRACE, "{")
                self.position += 1
                continue

            if char == "}":
                self._add(TokenType.RIGHT_BRACE, "}")
                self.position += 1
                continue

            # Arrays
            if char == "[":
                self._add(TokenType.LEFT_BRACKET, "[")
                self.position += 1
                continue

            if char == "]":
                self._add(TokenType.RIGHT_BRACKET, "]")
                self.position += 1
                continue

            # Separadores
            if char == ":":
                self._add(TokenType.COLON, ":")
                self.position += 1
                continue

            if char == ",":
                self._add(TokenType.COMMA, ",")
                self.position += 1
                continue

            # String
            if char == '"':
                self._read_string()
                continue

            # Número
            if char == "-" or char.isdigit():
                self._read_number()
                continue

            # Booleanos
            if self.text.startswith("true", self.position):
                start = self.position

                self.position += 4

                self._add(
                    TokenType.TRUE,
                    True,
                    start,
                )

                continue

            if self.text.startswith("false", self.position):
                start = self.position

                self.position += 5

                self._add(
                    TokenType.FALSE,
                    False,
                    start,
                )

                continue

            # Null
            if self.text.startswith("null", self.position):
                start = self.position

                self.position += 4

                self._add(
                    TokenType.NULL,
                    None,
                    start,
                )

                continue

            raise LexerError(
                f"Caractere inesperado na posição "
                f"{self.position}: {char!r}"
            )

        self.tokens.append(
            Token(
                TokenType.EOF,
                None,
                self.position,
            )
        )

        return self.tokens

    def _add(
        self,
        token_type: TokenType,
        value: object,
        position: int | None = None,
    ):
        """
        Adiciona um token à lista.

        Quando position não é informado, utiliza a posição
        atual do lexer.
        """

        if position is None:
            position = self.position

        self.tokens.append(
            Token(
                token_type,
                value,
                position,
            )
        )

    def _peek(self) -> str:
        """Retorna o próximo caractere sem avançar."""

        next_position = self.position + 1

        if next_position >= len(self.text):
            return ""

        return self.text[next_position]

    def _skip_comment(self):
        """Ignora um comentário de linha."""

        while (
            self.position < len(self.text)
            and self.text[self.position] != "\n"
        ):
            self.position += 1

    def _read_string(self):
        """Lê uma string JRO."""

        start = self.position

        self.position += 1

        while self.position < len(self.text):
            char = self.text[self.position]

            # Caractere escapado
            if char == "\\":
                self.position += 2
                continue

            # Final da string
            if char == '"':
                self.position += 1

                raw = self.text[start:self.position]

                try:
                    value = json.loads(raw)
                except json.JSONDecodeError as error:
                    raise LexerError(
                        f"String inválida na posição {start}"
                    ) from error

                self._add(
                    TokenType.STRING,
                    value,
                    start,
                )

                return

            self.position += 1

        raise LexerError(
            f"String não terminada na posição {start}"
        )

    def _read_number(self):
        """Lê um número inteiro ou decimal."""

        start = self.position

        # Sinal negativo
        if self.text[self.position] == "-":
            self.position += 1

        # Parte inteira
        while (
            self.position < len(self.text)
            and self.text[self.position].isdigit()
        ):
            self.position += 1

        # Parte decimal
        if (
            self.position < len(self.text)
            and self.text[self.position] == "."
        ):
            self.position += 1

            while (
                self.position < len(self.text)
                and self.text[self.position].isdigit()
            ):
                self.position += 1

        raw = self.text[start:self.position]

        try:
            value = (
                float(raw)
                if "." in raw
                else int(raw)
            )
        except ValueError as error:
            raise LexerError(
                f"Número inválido na posição {start}"
            ) from error

        self._add(
            TokenType.NUMBER,
            value,
            start,
        )
