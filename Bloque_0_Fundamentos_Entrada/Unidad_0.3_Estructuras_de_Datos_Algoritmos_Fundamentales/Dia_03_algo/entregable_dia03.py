from __future__ import annotations

import time


class Nodo:
    __slots__ = ("dato", "siguiente")

    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None


class ListaEnlazada:
    """Lista enlazada simple con cabeza, cola y tamaño."""

    def __init__(self):
        self.cabeza = None
        self.cola = None
        self._tamano = 0

    def __len__(self):
        return self._tamano

    def insertar_principio(self, dato):
        """O(1): crea un nodo y reajusta cabeza."""
        nuevo = Nodo(dato)
        nuevo.siguiente = self.cabeza
        self.cabeza = nuevo
        if self.cola is None:
            self.cola = nuevo
        self._tamano += 1
        return nuevo

    def insertar_final(self, dato):
        """O(1) porque se conserva una referencia a la cola."""
        nuevo = Nodo(dato)
        if self.cola is None:
            self.cabeza = self.cola = nuevo
        else:
            self.cola.siguiente = nuevo
            self.cola = nuevo
        self._tamano += 1
        return nuevo

    def __iter__(self):
        actual = self.cabeza
        while actual is not None:
            yield actual.dato
            actual = actual.siguiente

    def buscar(self, dato):
        """O(n): puede requerir recorrer toda la cadena."""
        actual = self.cabeza
        while actual is not None:
            if actual.dato == dato:
                return True
            actual = actual.siguiente
        return False

    def obtener(self, indice):
        """O(n): no existe acceso aleatorio por índice."""
        if indice < 0:
            indice += self._tamano
        if indice < 0 or indice >= self._tamano:
            raise IndexError("índice fuera de rango")

        actual = self.cabeza
        for _ in range(indice):
            actual = actual.siguiente
        return actual.dato

    def eliminar(self, dato):
        """O(n) por localizar; el reajuste de referencias es O(1)."""
        anterior = None
        actual = self.cabeza

        while actual is not None and actual.dato != dato:
            anterior = actual
            actual = actual.siguiente

        if actual is None:
            return False

        if anterior is None:
            self.cabeza = actual.siguiente
        else:
            anterior.siguiente = actual.siguiente

        if actual is self.cola:
            self.cola = anterior

        self._tamano -= 1
        if self._tamano == 0:
            self.cabeza = self.cola = None
        return True

    def invertir(self):
        """O(n) tiempo y O(1) espacio adicional."""
        anterior = None
        actual = self.cabeza
        self.cola = self.cabeza

        while actual is not None:
            siguiente = actual.siguiente
            actual.siguiente = anterior
            anterior = actual
            actual = siguiente

        self.cabeza = anterior


class NodoDoble:
    __slots__ = ("dato", "siguiente", "anterior")

    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None
        self.anterior = None


class ListaDoble:
    """Lista doblemente enlazada con recorrido bidireccional."""

    def __init__(self):
        self.cabeza = None
        self.cola = None
        self._tamano = 0

    def __len__(self):
        return self._tamano

    def insertar_final(self, dato):
        nuevo = NodoDoble(dato)
        if self.cola is None:
            self.cabeza = self.cola = nuevo
        else:
            nuevo.anterior = self.cola
            self.cola.siguiente = nuevo
            self.cola = nuevo
        self._tamano += 1
        return nuevo

    def eliminar_nodo(self, nodo):
        """O(1) si ya se tiene la referencia al nodo."""
        if nodo is None:
            return False

        if nodo.anterior is None:
            self.cabeza = nodo.siguiente
        else:
            nodo.anterior.siguiente = nodo.siguiente

        if nodo.siguiente is None:
            self.cola = nodo.anterior
        else:
            nodo.siguiente.anterior = nodo.anterior

        nodo.anterior = None
        nodo.siguiente = None
        self._tamano -= 1
        return True

    def adelante(self):
        actual = self.cabeza
        while actual is not None:
            yield actual.dato
            actual = actual.siguiente

    def atras(self):
        actual = self.cola
        while actual is not None:
            yield actual.dato
            actual = actual.anterior


def detectar_ciclo(cabeza):
    """Floyd: O(n) tiempo y O(1) espacio."""
    lento = rapido = cabeza
    while rapido is not None and rapido.siguiente is not None:
        lento = lento.siguiente
        rapido = rapido.siguiente.siguiente
        if lento is rapido:
            return True
    return False


def medir_insercion_principio():
    resultados = []
    for n in (5_000, 10_000, 20_000):
        t0 = time.perf_counter()
        enl = ListaEnlazada()
        for i in range(n):
            enl.insertar_principio(i)
        t_enl = time.perf_counter() - t0

        t0 = time.perf_counter()
        arr = []
        for i in range(n):
            arr.insert(0, i)
        t_arr = time.perf_counter() - t0

        ratio = t_arr / t_enl if t_enl else float("inf")
        resultados.append((n, t_enl, t_arr, ratio))
    return resultados


def medir_acceso_posicion():
    resultados = []
    repeticiones = 200
    for n in (10_000, 50_000, 100_000):
        enl = ListaEnlazada()
        for i in range(n):
            enl.insertar_final(i)
        arr = list(range(n))
        pos = n // 2

        t0 = time.perf_counter()
        for _ in range(repeticiones):
            enl.obtener(pos)
        t_enl = time.perf_counter() - t0

        t0 = time.perf_counter()
        for _ in range(repeticiones):
            _ = arr[pos]
        t_arr = time.perf_counter() - t0

        ratio = t_enl / t_arr if t_arr else float("inf")
        resultados.append((n, t_enl, t_arr, ratio))
    return resultados


def verificar_casos():
    # Lista vacía
    vacia = ListaEnlazada()
    assert len(vacia) == 0
    assert vacia.buscar(1) is False
    assert vacia.eliminar(1) is False

    # Un solo nodo / cabeza
    una = ListaEnlazada()
    una.insertar_principio(7)
    assert list(una) == [7]
    assert una.eliminar(7) is True
    assert len(una) == 0
    assert una.cabeza is None and una.cola is None

    # Inserción al principio y final
    l = ListaEnlazada()
    l.insertar_final(2)
    l.insertar_principio(1)
    l.insertar_final(3)
    assert list(l) == [1, 2, 3]
    assert l.buscar(2) is True
    assert l.obtener(1) == 2
    assert l.eliminar(2) is True
    assert list(l) == [1, 3]

    # Inversión O(1) espacio
    l.invertir()
    assert list(l) == [3, 1]
    assert l.cabeza.dato == 3
    assert l.cola.dato == 1

    # Lista doble y eliminación O(1) de nodo conocido
    ld = ListaDoble()
    n1 = ld.insertar_final(1)
    n2 = ld.insertar_final(2)
    n3 = ld.insertar_final(3)
    n4 = ld.insertar_final(4)
    assert list(ld.adelante()) == [1, 2, 3, 4]
    assert list(ld.atras()) == [4, 3, 2, 1]
    assert ld.eliminar_nodo(n3) is True
    assert list(ld.adelante()) == [1, 2, 4]
    assert list(ld.atras()) == [4, 2, 1]

    # Floyd: sin ciclo y con ciclo
    normal = ListaEnlazada()
    for x in (1, 2, 3):
        normal.insertar_final(x)
    assert detectar_ciclo(normal.cabeza) is False

    a, b, c = Nodo("a"), Nodo("b"), Nodo("c")
    a.siguiente = b
    b.siguiente = c
    c.siguiente = a
    assert detectar_ciclo(a) is True

    return True


def main():
    print("=" * 70)
    print("DÍA 3 — LISTAS ENLAZADAS: COMPROMISO INVERSO AL ARRAY")
    print("=" * 70)

    verificar_casos()
    print("PASS: casos límite, inversión, lista doble y Floyd")

    print("\nInserción al principio: lista enlazada vs array")
    for n, t_enl, t_arr, ratio in medir_insercion_principio():
        print(
            f"n={n:>6} | enlazada={t_enl*1000:>8.3f} ms | "
            f"array={t_arr*1000:>8.3f} ms | array/enlazada={ratio:>7.2f}x"
        )

    print("\nAcceso por posición: lista enlazada vs array")
    for n, t_enl, t_arr, ratio in medir_acceso_posicion():
        print(
            f"n={n:>6} | enlazada={t_enl*1000:>8.3f} ms | "
            f"array={t_arr*1000:>8.3f} ms | enlazada/array={ratio:>7.2f}x"
        )

    print("\nPASS FINAL")


if __name__ == "__main__":
    main()
