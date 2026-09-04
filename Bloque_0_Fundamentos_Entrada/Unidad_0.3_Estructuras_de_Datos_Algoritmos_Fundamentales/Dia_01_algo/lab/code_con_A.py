import time


def suma_lineal(n):  # O(n): un bucle
    total = 0
    for i in range(n):
        total += i
    return total


def suma_cuadratica(n):  # O(n^2): dos bucles anidados
    total = 0
    for i in range(n):
        for j in range(n):
            total += 1
    return total


# Medir cómo escala cada uno al DUPLICAR n:
for funcion, nombre in [(suma_lineal, "O(n)"), (suma_cuadratica, "O(n^2)")]:
    print(f"\n{nombre}:")
    t_prev = None
    for n in [1000, 2000, 4000]:
        t0 = time.perf_counter();
        funcion(n);
        t = time.perf_counter() - t0
        factor = f"  (x{t / t_prev:.1f} al duplicar n)" if t_prev else ""
        print(f"  n={n:>5}: {t * 1000:7.2f} ms{factor}")
        t_prev = t
# O(n): al duplicar n, el tiempo se duplica aprox (x2).
# O(n^2): al duplicar n, el tiempo se cuadruplica aprox (x4).
# El cociente de tiempos CONFIRMA empíricamente la clase asintótica.
