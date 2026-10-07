"""
JRO
===

JSON Reformulated Object para Python.

JRO 0.3.0
"""

from .decoder import load, loads
from .encoder import EncoderError, dump, dumps
from .parser import ParserError

__version__ = "0.3.0"
__author__ = "DrakkZ"

__all__ = [
    "dump",
    "dumps",
    "load",
    "loads",
    "EncoderError",
    "ParserError",
]
