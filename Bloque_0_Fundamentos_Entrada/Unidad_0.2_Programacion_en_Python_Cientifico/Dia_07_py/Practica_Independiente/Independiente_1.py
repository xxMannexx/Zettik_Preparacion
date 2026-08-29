import numpy as np
import time

rango = 1_000_000
array = np.arange(rango)

# NumPy
time_ini = time.perf_counter()
resultado_numpy = (array ** 2).sum()
time_final = time.perf_counter() - time_ini

print(resultado_numpy)
print(f"Con NumPy tardó: {time_final * 1000:.2f} milisegundos")

# Generador de Python
gen = (x**2 for x in range(rango))

time_ini_gen = time.perf_counter()
resultado_gen = sum(gen)
time_final_gen = time.perf_counter() - time_ini_gen

print(resultado_gen)
print(f"Con generador tardó: {time_final_gen * 1000:.2f} milisegundos")

print(
    f"NumPy fue aproximadamente "
    f"{time_final_gen / time_final:.2f} veces más rápido"
)