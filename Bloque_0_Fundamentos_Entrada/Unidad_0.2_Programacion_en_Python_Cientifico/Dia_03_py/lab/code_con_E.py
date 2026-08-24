import itertools


def cuadrados(n):
    contador = 0
    while contador <= n:
        yield contador**2
        contador += 1


a =list(itertools.islice(cuadrados(5), 10))

def iterar(*lista):
    for item in lista:
        yield from item

print(list(iterar(a)))

## Comprensiones y generadores

numeros = [1, 2, 3, 4, 5, 6]

# Comprensión de lista: materializa (ansiosa)
cuadrados = [x ** 2 for x in numeros]  # [1, 4, 9, 16, 25, 36]
pares = [x for x in numeros if x % 2 == 0]  # [2, 4, 6] (con filtro)

# Comprensión de conjunto y de diccionario
conjunto = {x % 3 for x in numeros}  # {0, 1, 2}
mapa = {x: x ** 2 for x in numeros}  # {1:1, 2:4, 3:9, ...}

# Expresión generadora: perezosa (mismo aspecto, paréntesis)
gen = (x ** 2 for x in numeros)  # un GENERADOR, no una lista
print(type(gen).__name__)  # 'generator'
print(sum(x ** 2 for x in numeros))  # 91: se consume sin materializar


