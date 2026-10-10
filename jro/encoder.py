"""
JRO Encoder
===========

Converte estruturas Python em texto JRO.

JRO 0.3.0
JSON Reformulated Object
"""

from __future__ import annotations

import math
from typing import Any


class EncoderError(Exception):
    """Erro encontrado durante a codificação de dados JRO."""


class Encoder:
    def __init__(
        self,
        *,
        indent: int | None = None,
        sort_keys: bool = False,
    ):
        if indent is not None:
            if isinstance(indent, bool) or not isinstance(indent, int):
                raise TypeError("indent deve ser um inteiro ou None.")

            if indent < 0:
                raise ValueError("indent não pode ser negativo.")

        if not isinstance(sort_keys, bool):
            raise TypeError("sort_keys deve ser bool.")

        self.indent = indent
        self.sort_keys = sort_keys
        self._active_containers: set[int] = set()

    def encode(self, data: Any) -> str:
        """Converte dados Python em texto JRO."""
        return self._encode_value(data, 0)

    def _encode_value(self, value: Any, level: int) -> str:
        """Codifica um valor Python."""

        if value is None:
            return "null"

        if value is True:
            return "true"

        if value is False:
            return "false"

        if isinstance(value, str):
            return self._encode_string(value)

        if isinstance(value, int):
            return str(value)

        if isinstance(value, float):
            return self._encode_float(value)

        if isinstance(value, dict):
            return self._encode_container(value, level)

        if isinstance(value, (list, tuple)):
            return self._encode_container(value, level)

        raise EncoderError(
            f"Tipo não suportado: {type(value).__name__}"
        )

    def _encode_string(self, value: str) -> str:
        """Codifica uma string e escapa caracteres especiais."""

        escapes = {
            '"': '\\"',
            "\\": "\\\\",
            "\n": "\\n",
            "\r": "\\r",
            "\t": "\\t",
            "\b": "\\b",
            "\f": "\\f",
        }

        result = ['"']

        for char in value:
            if char in escapes:
                result.append(escapes[char])
            elif ord(char) < 0x20:
                result.append(f"\\u{ord(char):04x}")
            else:
                result.append(char)

        result.append('"')
        return "".join(result)

    def _encode_float(self, value: float) -> str:
        """Codifica um número decimal finito."""

        if not math.isfinite(value):
            raise EncoderError(
                "JRO não permite NaN ou Infinity."
            )

        return repr(value)

    def _encode_container(self, value, level: int) -> str:
        """Codifica containers e detecta referências circulares."""

        container_id = id(value)

        if container_id in self._active_containers:
            raise EncoderError(
                "Referência circular não é permitida em JRO."
            )

        self._active_containers.add(container_id)

        try:
            if isinstance(value, dict):
                return self._encode_object(value, level)

            return self._encode_array(value, level)
        finally:
            self._active_containers.remove(container_id)

    def _encode_object(
        self,
        value: dict[Any, Any],
        level: int,
    ) -> str:
        """Codifica um dicionário como objeto JRO."""

        if not value:
            return "{}"

        for key in value:
            if not isinstance(key, str):
                raise EncoderError(
                    "As chaves de objetos JRO devem ser strings."
                )

        items_source = value.items()

        if self.sort_keys:
            items_source = sorted(
                items_source,
                key=lambda item: item[0],
            )

        items = []

        for key, item in items_source:
            encoded_key = self._encode_string(key)
            encoded_value = self._encode_value(
                item,
                level + 1,
            )

            items.append((encoded_key, encoded_value))

        if self.indent is None:
            return (
                "{"
                + ",".join(
                    f"{key}:{item}"
                    for key, item in items
                )
                + "}"
            )

        spaces = " " * (self.indent * (level + 1))
        closing_spaces = " " * (self.indent * level)

        lines = [
            f"{spaces}{key}: {item}"
            for key, item in items
        ]

        return (
            "{\n"
            + ",\n".join(lines)
            + f"\n{closing_spaces}}}"
        )

    def _encode_array(
        self,
        value: list[Any] | tuple[Any, ...],
        level: int,
    ) -> str:
        """Codifica uma lista ou tupla como array JRO."""

        if not value:
            return "[]"

        items = [
            self._encode_value(item, level + 1)
            for item in value
        ]

        if self.indent is None:
            return "[" + ",".join(items) + "]"

        spaces = " " * (self.indent * (level + 1))
        closing_spaces = " " * (self.indent * level)

        lines = [
            f"{spaces}{item}"
            for item in items
        ]

        return (
            "[\n"
            + ",\n".join(lines)
            + f"\n{closing_spaces}]"
        )


def dumps(
    data: Any,
    *,
    indent: int | None = None,
    sort_keys: bool = False,
) -> str:
    """Converte dados Python em uma string JRO."""

    return Encoder(
        indent=indent,
        sort_keys=sort_keys,
    ).encode(data)


def dump(
    data: Any,
    filename: str,
    *,
    indent: int | None = 4,
    sort_keys: bool = False,
) -> None:
    """Salva dados Python em um arquivo JRO."""

    with open(filename, "w", encoding="utf-8") as file:
        file.write(
            dumps(
                data,
                indent=indent,
                sort_keys=sort_keys,
            )
        )