[1mdiff --git a/README.md b/README.md[m
[1mindex e846fb8..a2ae9e5 100644[m
[1m--- a/README.md[m
[1m+++ b/README.md[m
[36m@@ -14,7 +14,7 @@[m [mJRO is a JSON-inspired data format and Python library designed to be simple, rea[m
 [m
 🚧 JRO is currently under development.[m
 [m
[31m-Current version: "0.2.0"[m
[32m+[m[32mCurrent version: 0.2.0[m
 [m
 The project already has:[m
 [m
[36m@@ -22,7 +22,7 @@[m [mThe project already has:[m
 - ✅ Custom parser[m
 - ✅ Encoder[m
 - ✅ Decoder[m
[31m-- ✅ "dumps()" / "loads()"[m
[32m+[m[32m- ✅ dumps() / loads()[m
 - ✅ Comment support[m
 - ✅ Automated tests[m
 - ✅ Python integration[m
[36m@@ -32,18 +32,16 @@[m [mThe project already has:[m
 [m
 ✨ Example[m
 [m
[31m-```jro[m
 {[m
[31m-"name": "DrakkZ",[m
[31m-"age": 10,[m
[31m-"games": [[m
[31m-"Pokémon",[m
[31m-"Minecraft"[m
[31m-],[m
[31m-"active": true,[m
[31m-"nothing": null[m
[32m+[m[32m    "name": "DrakkZ",[m
[32m+[m[32m    "age": 10,[m
[32m+[m[32m    "games": [[m
[32m+[m[32m        "Pokémon",[m
[32m+[m[32m        "Minecraft"[m
[32m+[m[32m    ],[m
[32m+[m[32m    "active": true,[m
[32m+[m[32m    "nothing": null[m
 }[m
[31m-```[m
 [m
 JRO keeps the familiar structure of JSON while leaving room for features of its own.[m
 [m
[36m@@ -51,15 +49,14 @@[m [mJRO keeps the familiar structure of JSON while leaving room for features of its[m
 [m
 🐍 Python[m
 [m
[31m-```python[m
 import jro[m
 [m
 data = {[m
[31m-"name": "DrakkZ",[m
[31m-"age": 10,[m
[31m-"games": ["Pokémon", "Minecraft"],[m
[31m-"active": True,[m
[31m-"nothing": None,[m
[32m+[m[32m    "name": "DrakkZ",[m
[32m+[m[32m    "age": 10,[m
[32m+[m[32m    "games": ["Pokémon", "Minecraft"],[m
[32m+[m[32m    "active": True,[m
[32m+[m[32m    "nothing": None,[m
 }[m
 [m
 text = jro.dumps(data, indent=4)[m
[36m@@ -69,13 +66,10 @@[m [mprint(text)[m
 decoded = jro.loads(text)[m
 [m
 print(decoded == data)[m
[31m-```[m
 [m
 Output:[m
 [m
[31m-```text[m
 True[m
[31m-```[m
 [m
 ---[m
 [m
[36m@@ -83,15 +77,12 @@[m [mTrue[m
 [m
 JRO supports single-line comments:[m
 [m
[31m-```jro[m
 {[m
[31m-// User information[m
[31m-"name": "DrakkZ",[m
[31m-[m
[31m-"age": 10[m
[32m+[m[32m    // User information[m
[32m+[m[32m    "name": "DrakkZ",[m
 [m
[32m+[m[32m    "age": 10[m
 }[m
[31m-```[m
 [m
 ---[m
 [m
[36m@@ -114,9 +105,7 @@[m [mJRO aims to provide:[m
 [m
 Install the development dependencies and run:[m
 [m
[31m-```bash[m
 pytest[m
[31m-```[m
 [m
 The project uses automated tests to verify the lexer, parser, encoder, decoder, errors, comments, and round-trip behavior.[m
 [m
[36m@@ -124,10 +113,9 @@[m [mThe project uses automated tests to verify the lexer, parser, encoder, decoder,[m
 [m
 📁 Project Structure[m
 [m
[31m-```text[m
 jro/[m
 ├── jro/[m
[31m-│   ├── init.py[m
[32m+[m[32m│   ├── __init__.py[m
 │   ├── lexer.py[m
 │   ├── parser.py[m
 │   ├── encoder.py[m
[36m@@ -143,7 +131,6 @@[m [mjro/[m
 ├── .gitignore[m
 ├── LICENSE[m
 └── README.md[m
[31m-```[m
 [m
 ---[m
 [m
