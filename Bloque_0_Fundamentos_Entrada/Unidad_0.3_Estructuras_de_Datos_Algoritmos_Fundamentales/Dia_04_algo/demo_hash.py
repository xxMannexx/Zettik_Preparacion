from __future__ import annotations

import time


class Par:
    __slots__ = ("clave", "valor", "siguiente")

    def __init__(self, clave, valor):
        self.clave = clave
        self.valor = valor
        self.siguiente = None


class TablaHash:
    def __init__(self, capacidad=8, umbral=0.75, auto_redimensionar=True):
        if capacidad <= 0:
            raise ValueError("capacidad debe ser > 0")
        if not (0 < umbral <= 1):
            raise ValueError("umbral debe estar en (0, 1]")
        self._m = capacidad
        self._cubetas = [None] * self._m
        self._n = 0
        self._umbral = umbral
        self._auto_redimensionar = auto_redimensionar

    def __len__(self):
        return self._n

    @property
    def capacidad(self):
        return self._m

    @property
    def factor_carga(self):
        return self._n / self._m

    def _indice(self, clave):
        return hash(clave) % self._m

    def insertar(self, clave, valor):
        i = self._indice(clave)
        actual = self._cubetas[i]

        while actual is not None:
            if actual.clave == clave:
                actual.valor = valor
                return False
            actual = actual.siguiente

        if self._auto_redimensionar and (self._n + 1) / self._m > self._umbral:
            self._redimensionar()
            i = self._indice(clave)

        nuevo = Par(clave, valor)
        nuevo.siguiente = self._cubetas[i]
        self._cubetas[i] = nuevo
        self._n += 1
        return True

    def buscar(self, clave):
        i = self._indice(clave)
        actual = self._cubetas[i]
        while actual is not None:
            if actual.clave == clave:
                return actual.valor
            actual = actual.siguiente
        raise KeyError(clave)

    def eliminar(self, clave):
        i = self._indice(clave)
        anterior = None
        actual = self._cubetas[i]

        while actual is not None:
            if actual.clave == clave:
                if anterior is None:
                    self._cubetas[i] = actual.siguiente
                else:
                    anterior.siguiente = actual.siguiente
                self._n -= 1
                return actual.valor
            anterior = actual
            actual = actual.siguiente

        raise KeyError(clave)

    def _redimensionar(self):
        viejas = self._cubetas
        self._m *= 2
        self._cubetas = [None] * self._m
        n_anterior = self._n
        self._n = 0

        for cabeza in viejas:
            actual = cabeza
            while actual is not None:
                siguiente = actual.siguiente
                i = self._indice(actual.clave)
                actual.siguiente = self._cubetas[i]
                self._cubetas[i] = actual
                self._n += 1
                actual = siguiente

        assert self._n == n_anterior

    def longitudes_cubetas(self):
        resultado = []
        for cabeza in self._cubetas:
            actual = cabeza
            longitud = 0
            while actual is not None:
                longitud += 1
                actual = actual.siguiente
            resultado.append(longitud)
        return resultado

    def longitud_maxima_cubeta(self):
        return max(self.longitudes_cubetas(), default=0)


class ClaveMala:
    __slots__ = ("valor",)

    def __init__(self, valor):
        self.valor = valor

    def __hash__(self):
        return 0

    def __eq__(self, otro):
        return isinstance(otro, ClaveMala) and self.valor == otro.valor


def verificar_tabla():
    print("\n1. Verificación funcional")
    tabla = TablaHash(capacidad=4)

    tabla.insertar("ana", 10)
    tabla.insertar("luis", 20)
    tabla.insertar("mane", 30)

    assert tabla.buscar("ana") == 10
    assert tabla.buscar("luis") == 20
    assert tabla.buscar("mane") == 30

    n_antes = len(tabla)
    creada = tabla.insertar("luis", 99)
    assert creada is False
    assert tabla.buscar("luis") == 99
    assert len(tabla) == n_antes

    eliminado = tabla.eliminar("ana")
    assert eliminado == 10
    try:
        tabla.buscar("ana")
        raise AssertionError("ana debió eliminarse")
    except KeyError:
        pass

    tabla2 = TablaHash(capacidad=2, umbral=0.75)
    for k in range(100):
        tabla2.insertar(f"clave_{k}", k * 10)

    assert len(tabla2) == 100
    assert tabla2.buscar("clave_42") == 420
    assert tabla2.capacidad > 2
    assert tabla2.factor_carga <= 0.75

    try:
        tabla2.insertar([1, 2], "invalido")
        raise AssertionError("una lista no debe ser aceptada como clave")
    except TypeError:
        pass

    print("PASS: inserción, búsqueda, actualización, eliminación, rehash y hashables")


def medir_busqueda_vs_lista():
    print("\n2. Búsqueda: tabla hash O(1) promedio vs lista O(n)")
    for n in (10_000, 50_000, 100_000):
        tabla = TablaHash()
        for k in range(n):
            tabla.insertar(k, k)
        lista = list(range(n))
        objetivo = n - 1
        repeticiones = 300

        t0 = time.perf_counter()
        for _ in range(repeticiones):
            tabla.buscar(objetivo)
        t_hash = time.perf_counter() - t0

        t0 = time.perf_counter()
        for _ in range(repeticiones):
            _ = objetivo in lista
        t_lista = time.perf_counter() - t0

        ventaja = t_lista / t_hash if t_hash else float("inf")
        print(
            f"n={n:>7} | hash={t_hash*1000:>8.3f} ms | "
            f"lista={t_lista*1000:>8.3f} ms | ventaja={ventaja:>8.1f}x"
        )


def medir_factor_carga():
    print("\n3. Efecto del factor de carga en la longitud de las cubetas")
    n = 20_000

    for m in (40_000, 20_000, 5_000, 1_000):
        tabla = TablaHash(capacidad=m, auto_redimensionar=False)
        for k in range(n):
            tabla.insertar(k, k)

        longitudes = tabla.longitudes_cubetas()
        ocupadas = [x for x in longitudes if x > 0]
        media_ocupadas = sum(ocupadas) / len(ocupadas) if ocupadas else 0.0

        print(
            f"m={m:>6} | alpha={tabla.factor_carga:>5.2f} | "
            f"max_cubeta={tabla.longitud_maxima_cubeta():>4} | "
            f"media_cubetas_ocupadas={media_ocupadas:>6.2f}"
        )


def medir_peor_caso():
    print("\n4. Peor caso: hash flooding con __hash__ constante")

    for n in (1_000, 2_000, 4_000):
        normal = TablaHash()
        t0 = time.perf_counter()
        for k in range(n):
            normal.insertar(k, k)
        t_normal = time.perf_counter() - t0

        mala = TablaHash()
        t0 = time.perf_counter()
        for k in range(n):
            mala.insertar(ClaveMala(k), k)
        t_peor = time.perf_counter() - t0

        degradacion = t_peor / t_normal if t_normal else float("inf")
        print(
            f"n={n:>5} | normal={t_normal*1000:>8.3f} ms | "
            f"colisiones={t_peor*1000:>9.3f} ms | "
            f"degradación={degradacion:>8.1f}x"
        )


def demo_vizionaria():
    print("\n5. Índice de seguimientos de VizionarIA con dict y set")

    seguimientos = {}
    vistos_frame = set()

    detecciones = [
        ("obj_17", "persona", 0.93),
        ("obj_52", "coche", 0.88),
        ("obj_17", "persona", 0.91),
    ]

    duplicados_frame = []

    for obj_id, clase, confianza in detecciones:
        if obj_id in vistos_frame:
            duplicados_frame.append(obj_id)

        vistos_frame.add(obj_id)
        seguimientos[obj_id] = {
            "clase": clase,
            "confianza": confianza,
        }

    assert seguimientos["obj_17"]["confianza"] == 0.91
    assert "obj_52" in vistos_frame
    assert duplicados_frame == ["obj_17"]

    print(f"seguimientos={seguimientos}")
    print(f"vistos_frame={sorted(vistos_frame)}")
    print(f"duplicados_frame={duplicados_frame}")
    print("PASS: acceso/actualización por ID y deduplicación por frame")


def main():
    print("=" * 76)
    print("DÍA 4 — TABLAS HASH: O(1) PROMEDIO, COLISIONES Y ENCADENAMIENTO")
    print("=" * 76)

    verificar_tabla()
    medir_busqueda_vs_lista()
    medir_factor_carga()
    medir_peor_caso()
    demo_vizionaria()

    print("\nPASS FINAL")


if __name__ == "__main__":
    main()
