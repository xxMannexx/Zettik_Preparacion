import time


# Dos algoritmos para el mismo problema, distinta clase asintotica:
def maximo_par_lento(lista):  # O(n^2): compara todos los pares
    m = 0
    for i in range(len(lista)):
        for j in range(len(lista)):
            m = max(m, abs(lista[i] - lista[j]))
    return m


def maximo_par_rapido(lista):  # O(n): max - min
    return max(lista) - min(lista)  # dos recorridos lineales -> O(n)


import random

for n in [100, 200, 400]:
    datos = [random.randint(0, 1000) for _ in range(n)]
    t0 = time.perf_counter();
    maximo_par_lento(datos);
    t_lento = time.perf_counter() - t0
    t0 = time.perf_counter();
    maximo_par_rapido(datos);
    t_rapido = time.perf_counter() - t0
    print(f"n={n:>4}: O(n^2)={t_lento * 1000:7.2f} ms, O(n)={t_rapido * 1000:6.3f} ms, "
          f"ratio={t_lento / t_rapido:.0f}x")
# El analisis predice que O(n) escala mejor; la medicion lo confirma y cuantifica.
# Al crecer n, la ventaja del O(n) aumenta -- como predice el analisis asintotico.
