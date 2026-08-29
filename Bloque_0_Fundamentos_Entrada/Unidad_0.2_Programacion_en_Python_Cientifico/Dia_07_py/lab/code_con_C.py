import numpy as np

a = np.array([1, 2, 3, 4])
b = np.array([10, 20, 30, 40])

print(a + b)  # [11 22 33 44]  (suma elemento a elemento, sin bucle)
print(a * 2)  # [2 4 6 8]      (escalar aplicado a todo el array)
print(a ** 2)  # [1 4 9 16]
print(np.sqrt(b))  # [3.16 4.47 5.48 6.32]  (ufunc sobre todo el array)
print(a > 2)  # [False False True True]  (comparación vectorizada -> array bool)

# Aplicado: normalizar un array (restar la media, dividir por la desviación) sin bucles
datos = np.array([2.0, 4.0, 6.0, 8.0])
normalizado = (datos - datos.mean()) / datos.std()
print(normalizado)  # operación completa, vectorizada, en una expresión
