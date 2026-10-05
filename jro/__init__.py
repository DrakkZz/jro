"""
JRO
===

JSON V2 para Python.

JRO 0.1.0
"""

from .encoder import dump, dumps
from .decoder import load, loads

__version__ = "0.1.0"
__author__ = "DrakkZ"

__all__ = [
    "dump",
    "dumps",
    "load",
    "loads",
]
