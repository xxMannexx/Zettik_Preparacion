import numpy as np

# Una "imagen" en escala de grises de 3 filas x 4 columnas
imagen = np.array([[10, 20, 30, 40],
                   [50, 60, 70, 80],
                   [90, 100, 110, 120]])

print(imagen.shape)
print(imagen.strides) ## Dara (32,8) osea 32 bytes para saltar de fila ejemplo del 10 al 50 y solo 8 bytes para saltar de columna
#Ejemplo del 50 al 10, tambien si quisieras saltar del 10 al 60 es un paso de 40 bytes 32 para ir del 10 al 50 y 8 para avanzar al 60

print(imagen.sum())  # 780: suma de TODO el array (sin axis)
print(imagen.sum(axis=0))  # [150 180 210 240]: suma por columna (a lo largo de las filas)
print(imagen.sum(axis=1))  # [100 260 420]: suma por fila (a lo largo de las columnas)
print(imagen.mean(axis=1))  # [25. 65. 105.]: media de cada fila
print(imagen.max(axis=0))  # [90 100 110 120]: máximo de cada columna

# Strides: la transposición es O(1) (solo intercambia strides, no mueve datos)
t = imagen.T
print(t.shape, np.shares_memory(imagen, t))  # (4, 3)  True: la transpuesta es una VISTA
