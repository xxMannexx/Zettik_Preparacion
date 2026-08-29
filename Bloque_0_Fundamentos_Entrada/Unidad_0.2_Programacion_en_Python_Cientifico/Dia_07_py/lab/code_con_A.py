import numpy as np, time

N = 100000000
lista = list(range(N))
array = np.arange(N) ## Crea un arraycon valos numericos uniforme dentro de un rango

# Suma con un bucle de Python (lento):
t0 = time.perf_counter()
total_py = sum(x * 2 for x in lista)
t_py = time.perf_counter() - t0

# Suma vectorizada con NumPy (rápida):
t0 = time.perf_counter()
total_np = (array * 2).sum()
t_np = time.perf_counter() - t0

print(f"Python: {t_py * 1000:.2f} ms;  NumPy: {t_np * 1000:.2f} ms;  aceleración: {t_py / t_np:.0f}x")
# NumPy es típicamente decenas de veces más rápido: la diferencia de representación es medible.
