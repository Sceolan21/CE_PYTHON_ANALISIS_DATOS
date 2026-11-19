"""Comprueba qué intérprete ejecuta el programa y si pertenece a un venv."""

import sys


print("Ejecutable:", sys.executable)
print("Prefijo actual:", sys.prefix)
print("Prefijo base:", sys.base_prefix)

if sys.prefix != sys.base_prefix:
    print("Estamos trabajando en un entorno virtual.")
else:
    print("Estamos utilizando el Python global.")
