"""
JRO Lexer
=========

Transforma texto JRO em tokens.

JRO 0.2.0
JSON V2
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from enum import Enum, auto


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

            if char.isspace():
                self.position += 1
                continue

            if char == "/" and self._peek() == "/":
                self._skip_comment()
                continue

            if char == "{":
                self._add(TokenType.LEFT_BRACE, "{")
                self.position += 1
                continue

            if char == "}":
                self._add(TokenType.RIGHT_BRACE, "}")
                self.position += 1
                continue

            if char == "[":
                self._add(TokenType.LEFT_BRACKET, "[")
                self.position += 1
                continue

            if char == "]":
                self._add(TokenType.RIGHT_BRACKET, "]")
                self.position += 1
                continue

            if char == ":":
                self._add(TokenType.COLON, ":")
                self.position += 1
                continue

            if char == ",":
                self._add(TokenType.COMMA, ",")
                self.position += 1
                continue

            if char == '"':
                self._read_string()
                continue

            if char == "-" or char.isdigit():
                self._read_number()
                continue

            if self.text.startswith("true", self.position):
                self._read_keyword(
                    "true",
                    TokenType.TRUE,
                    True,
                )
                continue

            if self.text.startswith("false", self.position):
                self._read_keyword(
                    "false",
                    TokenType.FALSE,
                    False,
                )
                continue

            if self.text.startswith("null", self.position):
                self._read_keyword(
                    "null",
                    TokenType.NULL,
                    None,
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
        next_position = self.position + 1

        if next_position >= len(self.text):
            return ""

        return self.text[next_position]

    def _skip_comment(self):
        while (
            self.position < len(self.text)
            and self.text[self.position] != "\n"
        ):
            self.position += 1

    def _read_keyword(
        self,
        keyword: str,
        token_type: TokenType,
        value: object,
    ):
        start = self.position
        end = start + len(keyword)

        if end < len(self.text):
            next_char = self.text[end]

            if (
                next_char.isalnum()
                or next_char == "_"
            ):
                raise LexerError(
                    f"Palavra inválida na posição "
                    f"{start}: {self.text[start:end + 1]!r}"
                )

        self.position = end

        self._add(
            token_type,
            value,
            start,
        )

    def _read_string(self):
        start = self.position

        self.position += 1

        while self.position < len(self.text):
            char = self.text[self.position]

            if char == "\\":
                self.position += 2
                continue

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
        start = self.position

        if self.text[self.position] == "-":
            self.position += 1

        while (
            self.position < len(self.text)
            and self.text[self.position].isdigit()
        ):
            self.position += 1

        if (
            self.position < len(self.text)
            and self.text[self.position] == "."
        ):
            self.position += 1

            decimal_start = self.position

            while (
                self.position < len(self.text)
                and self.text[self.position].isdigit()
            ):
                self.position += 1

            if decimal_start == self.position:
                raise LexerError(
                    f"Número inválido na posição {start}"
                )

        if self.position < len(self.text):
            next_char = self.text[self.position]

            if (
                next_char.isalpha()
                or next_char == "_"
            ):
                raise LexerError(
                    f"Número inválido na posição {start}"
                )

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
