import numpy as np

array = np.array([[1,2,3],
                  [4,5,6],
                  [7,8,9]])
vista = array[1,0:2] ## Vista
indexa = array[2,[1,2]] ## Indexacion

vista[1] = 10 ## Modifica el original en vez de 5 sera 10
indexa[1] = 10 ## No modifica el original ya es copia y en vez de 9 sera 10

print(vista)
print(indexa)
print(array)
print(np.shares_memory(vista.base, indexa))
print(np.shares_memory(vista.base, array))

