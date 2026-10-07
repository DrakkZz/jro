JRO

JRO is a JSON-inspired data format and Python library designed to be simple, readable, and extensible.

«JRO — JSON Reformulated Object»

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Work%20in%20Progress-orange)](#status)

---

📌 Status

🚧 JRO is currently under development.

Current version: 0.2.0

The project already has:

- ✅ Custom lexer
- ✅ Custom parser
- ✅ Encoder
- ✅ Decoder
- ✅ dumps() / loads()
- ✅ Comment support
- ✅ Automated tests
- ✅ Python integration
- ✅ GitHub repository

---

✨ Example

```jro
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
```

JRO keeps the familiar structure of JSON while leaving room for features of its own.

---

🐍 Python

```python
import jro

data = {
    "name": "DrakkZ",
    "age": 10,
    "games": ["Pokémon", "Minecraft"],
    "active": True,
    "nothing": None,
}

text = jro.dumps(data, indent=4)

print(text)

decoded = jro.loads(text)

print(decoded == data)
```

Output:

```text
True
```

---

💬 Comments

JRO supports single-line comments:

```jro
{
    // User information
    "name": "DrakkZ",

    "age": 10
}
```

---

🎯 Goals

JRO aims to provide:

- 🧩 A simple data format
- 🐍 Natural Python integration
- 🔍 Its own lexer and parser
- 🔄 Custom encoding and decoding
- 💬 Comment support
- 🧪 Automated testing
- 📦 A clean Python API
- 🚀 Room for future syntax and features

---

🧪 Testing

Install the development dependencies and run:

```bash
pytest
```

The project uses automated tests to verify the lexer, parser, encoder, decoder, errors, comments, and round-trip behavior.

---

📁 Project Structure

```text
jro/
├── jro/
│   ├── __init__.py
│   ├── lexer.py
│   ├── parser.py
│   ├── encoder.py
│   └── decoder.py
│
├── tests/
│   ├── conftest.py
│   ├── test_basic.py
│   ├── test_comments.py
│   ├── test_errors.py
│   └── test_lexer.py
│
├── .gitignore
├── LICENSE
└── README.md
```

---

📜 License

JRO is released under the MIT License.

See [LICENSE](LICENSE) for the full license text.

---

👤 Author

Created and maintained by DrakkZz.

---

<p align="center">
  <b>JRO</b><br>
  A small data format with big plans.
</p>
