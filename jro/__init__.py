"""
JRO
===

JSON V2 para Python.

JRO 0.2.0
"""

from .decoder import load, loads
from .encoder import EncoderError, dump, dumps
from .parser import ParserError

__version__ = "0.2.0"
__author__ = "DrakkZ"

__all__ = [
    "dump",
    "dumps",
    "load",
    "loads",
    "EncoderError",
    "ParserError",
]
