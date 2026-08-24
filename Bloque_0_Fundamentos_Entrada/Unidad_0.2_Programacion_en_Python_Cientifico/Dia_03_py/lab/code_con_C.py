def contar_hasta(n):
    print("  (inicio)")
    i = 1
    while i <= n:
        yield i  # produce i y SUSPENDE aquí, conservando i y la posición
        print(f"  (reanudado tras yield {i})")
        i += 1


gen = contar_hasta(3)  # NO imprime "(inicio)": el cuerpo aún no se ejecuta
print(next(gen))  # ejecuta hasta el primer yield -> imprime "(inicio)", devuelve 1
print(next(gen))  # REANUDA tras el yield -> imprime "(reanudado... 1)", devuelve 2
print(next(gen))  # devuelve 3
# print(next(gen))            # el while termina; lanza StopIteration

## Generadores como productores de secuencias.
def fibonacci():  # generador de una secuencia INFINITA
    a, b = 0, 1
    while True:  # bucle infinito: válido porque es perezoso (Concepto D)
        yield a
        a, b = b, a + b


# Se consume bajo demanda; nunca se materializa la secuencia infinita completa:
import itertools

primeros_diez = list(itertools.islice(fibonacci(), 10))
print(primeros_diez)  # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

## Delegación con `yield from`. Un generador puede delegar la producción a otro iterable con yield from, que produce todos los valores del iterable delegado:

def encadenar(*iterables):
    for it in iterables:
        yield from it             # produce todos los valores de cada iterable
print(list(encadenar([1, 2], [3, 4], [5])))   # [1, 2, 3, 4, 5]

