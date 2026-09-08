import time

##El acceso por indice es O(1)

for n in [1000,1000000,100000000]:
    lista = list(range(n))
    indice = n // 2
    t0 = time.perf_counter()
    for i in range(1000000):
        i = lista[indice]
    t = time.perf_counter() - t0
    print(f"n={n:>12,}: {t * 1000:.1f} ms para 1M accesos")
    # El tiempo por acceso es CONSTANTE, sin importar que la lista tenga mil o cien millones.
