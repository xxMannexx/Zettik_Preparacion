# vixia-utils

Biblioteca mínima del Día 6 de Python Científico.

## Verificación local

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --quiet mypy pytest build

mypy src/
pytest tests/
python scripts/profile_filtrado.py
python -m build
```
