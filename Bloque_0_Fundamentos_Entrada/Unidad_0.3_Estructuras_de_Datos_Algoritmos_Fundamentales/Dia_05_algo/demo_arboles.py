import random
import sys
import time

sys.setrecursionlimit(20000)
random.seed(42)


class NodoArbol:
    __slots__ = ("dato", "izquierdo", "derecho")

    def __init__(self, dato):
        self.dato = dato
        self.izquierdo = None
        self.derecho = None


class ABB:
    """Árbol Binario de Búsqueda sin auto-balanceo."""

    def __init__(self):
        self.raiz = None
        self._tamano = 0

    def __len__(self):
        return self._tamano

    def insertar(self, valor):
        self.raiz = self._insertar(self.raiz, valor)

    def _insertar(self, nodo, valor):
        if nodo is None:
            self._tamano += 1
            return NodoArbol(valor)

        if valor < nodo.dato:
            nodo.izquierdo = self._insertar(nodo.izquierdo, valor)
        elif valor > nodo.dato:
            nodo.derecho = self._insertar(nodo.derecho, valor)

        return nodo

    def buscar(self, dato):
        nodo = self.raiz

        while nodo is not None:
            if nodo.dato == dato:
                return True
            elif nodo.dato < dato:
                nodo = nodo.derecho
            else:
                nodo = nodo.izquierdo

        return False

    def eliminar(self, valor):
        self.raiz = self._eliminar(self.raiz, valor)

    def _eliminar(self, nodo, valor):
        if nodo is None:
            return None

        if valor < nodo.dato:
            nodo.izquierdo = self._eliminar(nodo.izquierdo, valor)
        elif valor > nodo.dato:
            nodo.derecho = self._eliminar(nodo.derecho, valor)
        else:
            if nodo.izquierdo is None:
                self._tamano -= 1
                return nodo.derecho

            if nodo.derecho is None:
                self._tamano -= 1
                return nodo.izquierdo

            sucesor = nodo.derecho
            while sucesor.izquierdo is not None:
                sucesor = sucesor.izquierdo

            nodo.dato = sucesor.dato
            nodo.derecho = self._eliminar(nodo.derecho, sucesor.dato)

        return nodo

    def en_orden(self):
        resultado = []
        self._en_orden(self.raiz, resultado)
        return resultado

    def _en_orden(self, nodo, resultado):
        if nodo is not None:
            self._en_orden(nodo.izquierdo, resultado)
            resultado.append(nodo.dato)
            self._en_orden(nodo.derecho, resultado)

    def pre_orden(self):
        resultado = []
        self._pre_orden(self.raiz, resultado)
        return resultado

    def _pre_orden(self, nodo, resultado):
        if nodo is not None:
            resultado.append(nodo.dato)
            self._pre_orden(nodo.izquierdo, resultado)
            self._pre_orden(nodo.derecho, resultado)

    def post_orden(self):
        resultado = []
        self._post_orden(self.raiz, resultado)
        return resultado

    def _post_orden(self, nodo, resultado):
        if nodo is not None:
            self._post_orden(nodo.izquierdo, resultado)
            self._post_orden(nodo.derecho, resultado)
            resultado.append(nodo.dato)

    def altura(self):
        return self._altura(self.raiz)

    def _altura(self, nodo):
        if nodo is None:
            return -1
        return 1 + max(
            self._altura(nodo.izquierdo),
            self._altura(nodo.derecho),
        )


def verificar_operaciones():
    print("\n1. Verificación funcional")
    arbol = ABB()

    assert arbol.buscar(10) is False
    assert arbol.en_orden() == []
    assert arbol.altura() == -1

    valores = [8, 4, 12, 2, 6, 10, 14]
    for valor in valores:
        arbol.insertar(valor)

    assert len(arbol) == 7
    assert arbol.buscar(10) is True
    assert arbol.buscar(99) is False

    assert arbol.en_orden() == [2, 4, 6, 8, 10, 12, 14]
    assert arbol.pre_orden() == [8, 4, 2, 6, 12, 10, 14]
    assert arbol.post_orden() == [2, 6, 4, 10, 14, 12, 8]

    arbol.eliminar(2)
    assert arbol.en_orden() == [4, 6, 8, 10, 12, 14]

    uno = ABB()
    for valor in [8, 4, 12, 10]:
        uno.insertar(valor)
    uno.eliminar(12)
    assert uno.en_orden() == [4, 8, 10]

    dos = ABB()
    for valor in [8, 4, 12, 10, 15]:
        dos.insertar(valor)
    dos.eliminar(12)
    assert dos.en_orden() == [4, 8, 10, 15]
    assert len(dos) == 4

    print("PASS: vacío, inserción, búsqueda, 3 recorridos y 3 casos de eliminación")


def medir_busqueda_vs_lista():
    print("\n2. ABB con inserción aleatoria vs lista")
    resultados = []

    for n in [10_000, 50_000, 100_000]:
        valores = list(range(n))
        random.shuffle(valores)

        arbol = ABB()
        for valor in valores:
            arbol.insertar(valor)

        lista = list(range(n))
        objetivo = n - 1
        repeticiones = 500

        t0 = time.perf_counter()
        for _ in range(repeticiones):
            arbol.buscar(objetivo)
        t_arbol = time.perf_counter() - t0

        t0 = time.perf_counter()
        for _ in range(repeticiones):
            _ = objetivo in lista
        t_lista = time.perf_counter() - t0

        ventaja = t_lista / t_arbol if t_arbol else float("inf")
        resultados.append((n, arbol.altura(), t_arbol, t_lista, ventaja))

        print(
            f"n={n:>7} | altura={arbol.altura():>3} | "
            f"ABB={t_arbol*1000:>8.3f} ms | "
            f"lista={t_lista*1000:>9.3f} ms | "
            f"ventaja={ventaja:>7.1f}x"
        )

    return resultados


def medir_degeneracion():
    print("\n3. Degeneración por inserción ordenada")
    resultados = []

    for n in [1_000, 2_000, 4_000]:
        valores = list(range(n))
        random.shuffle(valores)

        arbol_ok = ABB()
        for valor in valores:
            arbol_ok.insertar(valor)

        t0 = time.perf_counter()
        for _ in range(200):
            arbol_ok.buscar(n - 1)
        t_ok = time.perf_counter() - t0

        arbol_malo = ABB()
        for valor in range(n):
            arbol_malo.insertar(valor)

        t0 = time.perf_counter()
        for _ in range(200):
            arbol_malo.buscar(n - 1)
        t_malo = time.perf_counter() - t0

        degradacion = t_malo / t_ok if t_ok else float("inf")
        resultados.append((
            n,
            arbol_ok.altura(),
            arbol_malo.altura(),
            t_ok,
            t_malo,
            degradacion,
        ))

        print(
            f"n={n:>5} | altura_aleatoria={arbol_ok.altura():>3} | "
            f"altura_degenerada={arbol_malo.altura():>4} | "
            f"degradación={degradacion:>7.1f}x"
        )

    return resultados


def comparar_hash_vs_arbol():
    print("\n4. Dict vs ABB")

    n = 100_000
    valores = list(range(n))
    random.shuffle(valores)

    arbol = ABB()
    for valor in valores:
        arbol.insertar(valor)

    diccionario = {valor: valor for valor in valores}
    objetivo = n - 1
    repeticiones = 10_000

    t0 = time.perf_counter()
    for _ in range(repeticiones):
        arbol.buscar(objetivo)
    t_arbol = time.perf_counter() - t0

    t0 = time.perf_counter()
    for _ in range(repeticiones):
        _ = objetivo in diccionario
    t_hash = time.perf_counter() - t0

    factor = t_arbol / t_hash if t_hash else float("inf")
    primeros_abb = arbol.en_orden()[:8]
    primeras_claves_dict = list(diccionario.keys())[:8]

    print(
        f"ABB={t_arbol*1000:.3f} ms | "
        f"dict={t_hash*1000:.3f} ms | "
        f"dict≈{factor:.1f}x más rápido en búsqueda pura"
    )
    print(f"ABB en-orden: {primeros_abb}")
    print(f"dict primeras claves: {primeras_claves_dict}")

    return t_arbol, t_hash, factor, primeros_abb, primeras_claves_dict


def demo_vizionaria():
    print("\n5. Índice cronológico de eventos de VizionarIA")

    eventos = ABB()
    datos = [
        (120, "obj_17", "persona"),
        (105, "obj_52", "coche"),
        (135, "obj_31", "bicicleta"),
        (110, "obj_08", "persona"),
        (128, "obj_60", "señal"),
    ]

    for evento in datos:
        eventos.insertar(evento)

    cronologico = eventos.en_orden()

    assert [evento[0] for evento in cronologico] == sorted(
        evento[0] for evento in datos
    )

    print("Eventos ordenados por tiempo:")
    for evento in cronologico:
        print(evento)

    print("PASS: recorrido cronológico correcto")


def main():
    print("=" * 78)
    print("DÍA 5 — ÁRBOLES BINARIOS DE BÚSQUEDA")
    print("=" * 78)

    verificar_operaciones()
    medir_busqueda_vs_lista()
    medir_degeneracion()
    comparar_hash_vs_arbol()
    demo_vizionaria()

    print("\nPASS FINAL")


if __name__ == "__main__":
    main()
