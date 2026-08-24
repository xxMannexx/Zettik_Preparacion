## Representacion de un for sin for llamada de metodos de iteracion

numeros = [10, 20, 30]
it = iter(numeros)          # obtiene un iterador de la lista
print(next(it))             # 10
print(next(it))             # 20
print(next(it))             # 30
print(next(it))             # StopIteration: se agotó
# Esto es EXACTAMENTE lo que el bucle 'for' hace internamente.


