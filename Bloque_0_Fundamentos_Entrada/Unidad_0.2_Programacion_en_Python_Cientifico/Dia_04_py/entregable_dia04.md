# Entregable Día 04 — Excepciones, manejo de errores y context managers

## 1. Propagación de excepciones

Una excepción no tiene que manejarse exactamente donde ocurre. Si la función actual no tiene un `except` compatible, la excepción sube automáticamente por la pila de llamadas hasta encontrar un manejador.

```python
def c():
    raise ValueError("error en c")

def b():
    return c()

def a():
    try:
        return b()
    except ValueError as e:
        return f"manejado en a: {e}"

print(a())
```

Aquí el error nace en `c()`, atraviesa `b()` sin que esa función tenga que reenviarlo manualmente y termina siendo manejado en `a()`.

La idea importante es separar el lugar donde el error se detecta del lugar donde realmente se maneja.

---

## 2. Garantía de `finally`

`finally` se ejecuta siempre: haya error o no, e incluso aunque el `try` tenga un `return`.

```python
orden = []

def con_finally():
    try:
        orden.append("try")
        return "retorno"
    finally:
        orden.append("finally")

r = con_finally()

print(f"orden de ejecución: {orden}; retorno: {r!r}")
```

El valor del `return` queda preparado, después se ejecuta `finally` y solo entonces la función termina retornando.

Por eso `finally` es un lugar seguro para lógica de limpieza.

---

## 3. Jerarquía de excepciones propias

Las excepciones son clases y pueden organizarse mediante herencia.

```python
class AppError(Exception):
    pass

class EntradaError(AppError):
    pass
```

Si lanzo `EntradaError`, también puedo capturarla con `except AppError` porque `EntradaError` es una subclase de `AppError`.

```python
try:
    raise EntradaError("entrada inválida")
except AppError:
    print("capturada por la base")
```

Esto permite tener una excepción base para toda la aplicación y varias subclases específicas para errores concretos.

---

## 4. Encadenamiento con `raise ... from ...`

A veces conviene transformar un error técnico en otro más significativo, pero sin perder la causa original.

```python
def parsear(t):
    try:
        return int(t)
    except ValueError as e:
        raise RuntimeError(f"fallo al parsear {t!r}") from e
```

`from e` conserva el error original dentro de `__cause__`.

```python
try:
    parsear("abc")
except RuntimeError as e:
    print(type(e.__cause__).__name__)
```

El resultado debe ser `ValueError`.

Eso permite elevar el nivel de abstracción del error sin perder información útil para depuración.

---

## 5. Context managers y liberación garantizada

Un context manager permite adquirir un recurso al entrar a un bloque `with` y liberarlo al salir.

En una implementación basada en clase, `__enter__()` prepara el recurso y `__exit__()` garantiza la limpieza.

```python
eventos = []

class Recurso:
    def __enter__(self):
        eventos.append("adquirido")
        return self

    def __exit__(self, *a):
        eventos.append("liberado")
        return False
```

Ahora genero intencionalmente una excepción:

```python
try:
    with Recurso():
        eventos.append("usando")
        raise ValueError("fallo dentro del with")
except ValueError:
    eventos.append("manejado")
```

El orden esperado es:

```text
adquirido
usando
liberado
manejado
```

Eso demuestra que `__exit__()` se ejecuta incluso cuando ocurre una excepción.

Además, devolver `False` hace que la excepción siga propagándose después de liberar el recurso.

Conceptualmente, `with` ofrece la misma garantía de limpieza que `try/finally`.

---

## 6. Context manager con `contextlib.contextmanager`

También se puede crear un context manager con una función generadora decorada con `@contextmanager`.

```python
from contextlib import contextmanager

traza = []

@contextmanager
def gestor(nombre):
    traza.append(f"abrir {nombre}")
    try:
        yield nombre
    finally:
        traza.append(f"cerrar {nombre}")
```

En esta forma:

- el código antes de `yield` equivale a `__enter__`;
- el valor de `yield` es lo que recibe la variable después de `as`;
- el código después de `yield` equivale a `__exit__`.

```python
with gestor("recurso") as r:
    traza.append(f"usar {r}")
```

El resultado esperado es:

```text
abrir recurso
usar recurso
cerrar recurso
```

El `yield` suspende el generador mientras se ejecuta el cuerpo del `with`. Al salir, el generador se reanuda y el `finally` garantiza el cierre.

---

## Conclusión

Las excepciones permiten que un error se detecte en una función y se maneje en otra más arriba sin obligar a todas las funciones intermedias a comprobarlo manualmente.

`finally` garantiza la ejecución de lógica de limpieza. Las jerarquías de excepciones propias permiten capturar errores de forma general o específica. `raise ... from ...` conserva la causa original mediante `__cause__`.

Los context managers formalizan la adquisición y liberación de recursos. Con clases se implementan `__enter__` y `__exit__`; con `@contextmanager`, el código antes y después de un único `yield` cumple esos mismos papeles.

---

## Script utilizado — `demo_excepciones.py`

```python
from contextlib import contextmanager


def seccion(t):
    print(f"\n{'='*60}\n{t}\n{'='*60}")


seccion("1. Propagación de una excepción por la pila")

def c():
    raise ValueError("error en c")

def b():
    return c()

def a():
    try:
        return b()
    except ValueError as e:
        return f"manejado en a: {e}"

print(f"  {a()}")


seccion("2. finally se ejecuta siempre")

orden = []

def con_finally():
    try:
        orden.append("try")
        return "retorno"
    finally:
        orden.append("finally")

r = con_finally()
print(f"  orden de ejecución: {orden}; retorno: {r!r}")


seccion("3. Jerarquía propia: capturar la base captura las subclases")

class AppError(Exception):
    pass

class EntradaError(AppError):
    pass

capturado_por_base = False

try:
    raise EntradaError("entrada inválida")
except AppError as e:
    capturado_por_base = True

print(f"  EntradaError capturada por except AppError: {capturado_por_base}")


seccion("4. Encadenamiento preserva la causa")

def parsear(t):
    try:
        return int(t)
    except ValueError as e:
        raise RuntimeError(f"fallo al parsear {t!r}") from e

try:
    parsear("abc")
except RuntimeError as e:
    print(f"  error: {e}; causa: {type(e.__cause__).__name__}")


seccion("5. with libera el recurso pese a una excepción")

eventos = []

class Recurso:
    def __enter__(self):
        eventos.append("adquirido")
        return self

    def __exit__(self, *a):
        eventos.append("liberado")
        return False

try:
    with Recurso():
        eventos.append("usando")
        raise ValueError("fallo dentro del with")
except ValueError:
    eventos.append("manejado")

print(f"  eventos: {eventos}")


seccion("6. Context manager con contextlib (generador)")

traza = []

@contextmanager
def gestor(nombre):
    traza.append(f"abrir {nombre}")
    try:
        yield nombre
    finally:
        traza.append(f"cerrar {nombre}")

with gestor("recurso") as r:
    traza.append(f"usar {r}")

print(f"  traza: {traza}")
```
