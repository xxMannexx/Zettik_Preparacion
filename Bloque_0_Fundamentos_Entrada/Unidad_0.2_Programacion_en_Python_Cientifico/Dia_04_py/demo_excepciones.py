from contextlib import contextmanager


def seccion(t): print(f"\n{'=' * 60}\n{t}\n{'=' * 60}")


# 1) Propagación a través de varias funciones
seccion("1. Propagación de una excepción por la pila")


def c(): raise ValueError("error en c")


def b(): return c()  # no maneja; la excepción lo atraviesa


def a():
    try:
        return b()
    except ValueError as e:
        return f"manejado en a: {e}"


print(f"  {a()}")

# 2) Garantía de finally (incluso con return)
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

# 3) Jerarquía de excepciones propias
seccion("3. Jerarquía propia: capturar la base captura las subclases")


class AppError(Exception): pass


class EntradaError(AppError): pass


capturado_por_base = False
try:
    raise EntradaError("entrada inválida")
except AppError as e:
    capturado_por_base = True
print(f"  EntradaError capturada por except AppError: {capturado_por_base}")

# 4) Encadenamiento
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

# 5) Garantía de liberación de with (con excepción dentro)
seccion("5. with libera el recurso pese a una excepción")
eventos = []


class Recurso:
    def __enter__(self): eventos.append("adquirido"); return self

    def __exit__(self, *a): eventos.append("liberado"); return False


try:
    with Recurso():
        eventos.append("usando")
        raise ValueError("fallo dentro del with")
except ValueError:
    eventos.append("manejado")
print(f"  eventos: {eventos}")  # adquirido, usando, liberado, manejado

# 6) Context manager basado en generador
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
print(f"  traza: {traza}")  # abrir, usar, cerrar
