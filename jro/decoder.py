"""
JRO Decoder
===========

Converte texto JRO em estruturas Python.

JRO 0.3.0
JSON Reformulated Object
"""

from __future__ import annotations

from typing import Any

from .parser import parse


def loads(text: str) -> Any:
    """
    Converte uma string JRO em uma estrutura Python.

    Parâmetros:
        text: Texto contendo dados JRO.

    Retorna:
        Uma estrutura Python correspondente aos dados.
    """

    if not isinstance(text, str):
        raise TypeError(
            "loads() esperava uma string."
        )

    return parse(text)


def load(filename: str) -> Any:
    """
    Lê um arquivo .jro e converte seu conteúdo
    para uma estrutura Python.

    Parâmetros:
        filename: Caminho do arquivo JRO.

    Retorna:
        Uma estrutura Python correspondente aos dados.
    """

    with open(
        filename,
        "r",
        encoding="utf-8",
    ) as file:
        return loads(file.read())
