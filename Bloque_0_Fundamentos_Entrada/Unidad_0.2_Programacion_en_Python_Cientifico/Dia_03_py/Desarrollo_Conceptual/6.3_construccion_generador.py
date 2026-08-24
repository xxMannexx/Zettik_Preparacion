## Un generador provoca un iterable yield decide que valor entrega en cada punto de ejecucion (posicion/indice), conserva su estado

def pares_hasta(n):
    i = 0
    while i <= n:
        yield i
        i += 2

gen = pares_hasta(100) ## Genera un objeto iterador con la logica de la funcion

## Equivalente a:

gen2 = (x  for x in range(100) if x % 2 == 0)

## TAMBIEN PUEDO OBTENER UNO A UNO SIN MATERIALIZAR
print(next(gen2))

## MATERIALIZARLO TODO LOS QUE ENTREGA EN UNA LISTA
print(list(gen2))

print(next(gen)) ## Me da el primero es como si de una lista obtuviera el indice 0 pero aqui no estan materializados todos solo el que necesito
print(next(gen))
print(list(gen))  ## Hace la secuencia completa la lista la materializa pero sin entregar los valores queya dio, un generador recuerda su ultimo punto de ejecucion
