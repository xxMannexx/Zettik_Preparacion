import time

from lab.code_con_B import ABB


# Demostrar la degeneracion: insercion ORDENADA produce un arbol lineal O(n)
def medir_degeneracion(n):
    # Caso bueno: insercion ALEATORIA -> arbol ~equilibrado, altura ~log n
    import random
    vals = list(range(n));
    random.shuffle(vals)
    arbol_ok = ABB()
    for v in vals: arbol_ok.insertar(v)
    # Caso malo: insercion ORDENADA -> arbol degenerado (cadena), altura n
    arbol_malo = ABB()
    for v in range(n): arbol_malo.insertar(v)  # 0,1,2,...,n-1 en orden -> cadena a la derecha
    # Medir la busqueda del peor elemento
    t0 = time.perf_counter()
    for _ in range(100): arbol_ok.buscar(n - 1)
    t_ok = time.perf_counter() - t0
    t0 = time.perf_counter()
    for _ in range(100): arbol_malo.buscar(n - 1)
    t_malo = time.perf_counter() - t0
    return t_ok, t_malo


for n in [1_000, 2_000, 4_000]:
    t_ok, t_malo = medir_degeneracion(n)
    print(f"n={n:>5}: equilibrado O(log n)={t_ok * 1000:6.2f} ms, "
          f"degenerado O(n)={t_malo * 1000:7.2f} ms, x{t_malo / t_ok:.0f}")
# El arbol degenerado (insercion ordenada) es drasticamente mas lento: O(n) vs O(log n).
