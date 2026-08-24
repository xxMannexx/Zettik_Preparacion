## Un generador infinito va mas alla de lo que podamos manejar al materializarlo, con evaluacion perezosa es computable debido a que solo computa lo que consume sin generar numeros infinitos

import itertools

def naturales():
    n = 1
    while True:
        yield n
        n += 1

print(list(itertools.islice(naturales(), 10))) ## Tiene la secuencia infinita todo pero genera solo lo que necesita sin matar la memoria

