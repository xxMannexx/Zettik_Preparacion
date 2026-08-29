import numpy as np

imagen = np.array([[100,150],
                   [200,250]])

print(imagen + 50)
print(imagen * 50)

# El escalar 50 se "estira" a cada elemento: broadcasting de () contra (2,2).

## Aplicar escala a cada canal de color de una imagen

## Iamgen rgb de 2x2 pixeles. 3 canales forma: (2,2,3)

imagen = np.ones((2, 2, 3))                     # todos los píxeles a 1.0
print(imagen)

escala_canales = np.array([0.5, 1.0, 1.5])      # un factor por canal: forma (3,)

resultado = imagen * escala_canales             # broadcasting: (2,2,3) * (3,) -> (2,2,3)

print(resultado[0, 0])                           # [0.5 1.0 1.5]  (cada canal escalado)
# La forma (3,) se alinea con la última dimensión de (2,2,3) y se difunde por las demás.

import numpy as np
# Alinear desde la derecha; compatibles si iguales o una es 1; ausente al inicio = 1
A = np.ones((3, 4))      # (3, 4)
B = np.ones((4,))        # (   4)  -> se alinea con la última: (3,4) compatible -> resultado (3,4)
C = np.ones((3, 1))      # (3, 1)  -> la dimensión 1 se estira: (3,4) compatible -> resultado (3,4)
D = np.ones((2,))        # (   2)  -> 2 != 4 y ninguna es 1 -> ERROR de broadcasting
print((A + B).shape)     # (3, 4)
print((A + C).shape)     # (3, 4)
# A + D  ->  ValueError: operands could not be broadcast together with shapes (3,4) (2,)

## Ejemplo


a = np.array([2, 4, 6])
b = np.array([[1, 3, 5], [7, 9, 11]])
res = a + b
print(res)