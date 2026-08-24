def enteros_desde(n):
    ## Es una secuencia infinita imposible de meter en memoria
    while True:
        yield n
        n += 1

import itertools

## MATERIALIZAR UN FRAGMENTO DE LA SECUENCIA INFINITA DEMOSTRANDO QUE ES PEREZOSA

print(list(itertools.islice(enteros_desde(10), 10)))

## Si la funcion no fuera generador, no permitieria tratarse como "lista" y computaria toda la secuncia de numeros haciendola computacionalmente imposible

## Comparacion de memoria (ansioso vs perezoso).(ansioso vs perezoso).

import sys
lista = [x for x in range(100000)]  ## O(N) materializa todos los numeros
generador = (x for x in range(100000)) ##O(1)

print(generador)
print(lista)

print(sys.getsizeof(lista))
print(type(generador).__name__)
print(type(enteros_desde).__name__)


