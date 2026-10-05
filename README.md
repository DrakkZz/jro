JRO

JRO is a JSON-inspired data format and Python library.

It aims to keep the simplicity of JSON while providing room for its own syntax, features, and rules.

Status

🚧 Work in progress.

Current version: 0.2.0

Example

{
    "name": "DrakkZ",
    "age": 10,
    "games": [
        "Pokémon",
        "Minecraft"
    ],
    "active": true,
    "nothing": null
}

Python

import jro

data = {
    "name": "DrakkZ",
    "age": 10,
    "games": ["Pokémon", "Minecraft"],
    "active": True,
    "nothing": None,
}

text = jro.dumps(data, indent=4)
decoded = jro.loads(text)

print(decoded == data)

Goals

- Simple syntax.
- Natural integration with Python data structures.
- Custom lexer and parser.
- Custom encoder and decoder.
- Comment support.
- Automated tests.
- A data format with its own identity.

Development

JRO is written in Python.

Run the test suite with:

pytest

License

This project is licensed under the MIT License.

---

JRO — JSON V2
