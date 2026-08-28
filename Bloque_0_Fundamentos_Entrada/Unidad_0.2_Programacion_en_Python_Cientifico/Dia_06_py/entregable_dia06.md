# Entregable Día 06 — Calidad de código

## Objetivo

Construir una biblioteca mínima tipada, probada, instrumentada, perfilada y empaquetable como embrión de utilidades de VizionarIA.

## 1. Módulo tipado

El paquete `src/vixia_utils/` contiene:

- `Deteccion`, una `dataclass` con anotaciones completas y validación explícita en `__post_init__`.
- `filtrar_por_confianza(...) -> list[Deteccion]`.
- `confianza_media(...) -> float`.
- `ejecutar_detector(...) -> list[Deteccion]`.

Las anotaciones documentan y permiten verificación estática, pero la entrada externa se valida explícitamente en ejecución.

Verificación esperada:

```bash
mypy src/
```

Resultado esperado:

```text
Success: no issues found in ... source files
```

## 2. Protocol

`protocolos.py` define:

```python
class Detector(Protocol):
    def detectar(self, entrada: str) -> list[Deteccion]:
        ...
```

`ejecutar_detector(detector: Detector, entrada: str)` usa el Protocol en su firma.

La prueba `DetectorSimulado` no hereda de `Detector`; es compatible por estructura porque implementa el método exigido.

## 3. Suite pytest

La suite incluye:

- `@pytest.fixture` para preparar detecciones.
- `@pytest.mark.parametrize` para probar varios umbrales.
- `pytest.raises(ValueError)` para entradas inválidas.
- una prueba de duck typing con el `Protocol`.

Ejecución:

```bash
pytest tests/
```

## 4. Logging

Los módulos usan `logging.getLogger(__name__)`.

Se registran únicamente datos operacionales no sensibles, como cantidades y umbrales. No se registran nombres de usuario, imágenes, tokens, rutas privadas ni PII.

La configuración se centraliza en `logging_config.py`, separando emitir mensajes de decidir cuáles mostrar y con qué nivel.

## 5. Profiling

El script:

```bash
python scripts/profile_filtrado.py
```

genera:

```text
profiling/profile_filtrado.txt
```

con `cProfile`, ordenado por tiempo acumulado. El objetivo es identificar el cuello de botella antes de optimizar.

## 6. Empaquetado

`pyproject.toml` declara:

- backend de construcción;
- nombre del paquete;
- versión semántica `0.1.0`;
- Python mínimo;
- descubrimiento del paquete bajo `src/`;
- configuración de pytest y mypy.

Construcción:

```bash
python -m build
```

Debe generar artefactos bajo `dist/`, incluyendo un `.whl`.

## 7. Flujo completo

```bash
cd ~/vixia/dia06_py/vixia_utils
python3 -m venv .venv
source .venv/bin/activate
pip install --quiet mypy pytest build

mypy src/
pytest tests/
python scripts/profile_filtrado.py
python -m build
```

## 8. Git y versionado

Desde `~/vixia`:

```bash
git add dia06_py/
git commit -m "feat(b0): U0.2 día 6 — biblioteca tipada, probada y empaquetada (cierre Tema 0.2.1)"
git tag -a v0.1.0 -m "vixia_utils 0.1.0: primera versión de la biblioteca"
```

La versión inicial es `0.1.0`, siguiendo versionado semántico.
