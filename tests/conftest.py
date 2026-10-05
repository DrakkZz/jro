"""
Configuração dos testes da JRO.

JRO 0.2.0
JSON V2
"""

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent.parent

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
