import numpy as np

imagen = np.ones((2,2,3))

escala = np.array([0.5, 1.0, 1.5])

escaladas = imagen * escala  ## (2,2,3)

print(escaladas.shape)

print(escaladas[0,0])
