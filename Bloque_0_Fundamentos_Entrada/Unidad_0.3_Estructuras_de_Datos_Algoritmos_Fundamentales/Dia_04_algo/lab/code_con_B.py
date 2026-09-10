import time

# Pertenencia: set/dict O(1) promedio vs lista O(n)
print("Pertenencia: set O(1) promedio vs lista O(n)")
for n in [10_000, 100_000, 1_000_000]:
    lista = list(range(n))
    conjunto = set(range(n))
    objetivo = n - 1  # el peor caso para la lista (ultimo elemento)
    t0 = time.perf_counter()
    for _ in range(1000): _ = objetivo in lista  # O(n) cada uno
    t_lista = time.perf_counter() - t0
    t0 = time.perf_counter()
    for _ in range(1000): _ = objetivo in conjunto  # O(1) promedio cada uno
    t_set = time.perf_counter() - t0
    print(f"  n={n:>9,}: lista O(n)={t_lista * 1000:8.2f} ms, set O(1)={t_set * 1000:6.3f} ms, "
          f"ventaja={t_lista / t_set:.0f}x")
# La ventaja del set CRECE con n: la lista escala O(n), el set se mantiene O(1).
