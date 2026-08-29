import numpy as np

array = np.array([[10,20,30],
                  [40,50,60]],dtype=np.float32)

normalizar = (array - array.mean()) / array.std()
print(normalizar)

