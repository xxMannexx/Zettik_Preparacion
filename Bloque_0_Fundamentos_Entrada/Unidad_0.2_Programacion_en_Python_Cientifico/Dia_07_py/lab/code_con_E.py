import numpy as np

a = np.array([0,1,2,3,4,5])
vista = a[1:4]      # un rebanado: VISTA, comparte memoria con 'a'
print(np.shares_memory(a,vista))     # True: comparten el bloque de datos
print(vista.base is a)                   # True: la vista referencia a 'a'
vista[0] = 99                          # muta la vista...
print(a)

#3 Indexacion avanzada

copia = a[[1, 2, 3]]  # indexación avanzada (array de índices): COPIA
print(np.shares_memory(a, copia))  # False: bloques distintos
copia[0] = -1  # muta la copia...
print(a)  # [ 0 99  2  3  4  5]  <- 'a' NO cambió (independiente)

mascara = a[a > 50]
print(mascara) # indexación booleana: también COPIA
forzar = a[1:4].copy()  # .copy() fuerza una copia independiente de un rebanado
