## Objetivo: construir un generador que agrupe un flujo en bloques de tamaño fijo, útil para procesar por lotes

def en_lotes(iterable,size):
    lote = []               ## iniciamos la caja donde caera la particion de nuestros datos completos

    for elemento in iterable:       ## Recorremos todos los elementos
        lote.append(elemento)       ## Agregamos uno a uno a nuestro lote
        if len(lote) == size:       ## Comprobamos si el lote ya teiene el size deseado
            yield lote              ## Si es el caso, damos este primer lote
            lote = []               ## Reiniciamos el lote completamente para generar el siguiente, basicamente entrega y limpia
    if lote:                        ## Si no acompleta el size de igual manera genera el lote con los datos "sobrantes"
        yield lote                  ## Entrega el ultimo lote, si no se acompleto con size


datos = range(10_000)

## Los generamos todos de una pasada
for lote in en_lotes(datos,10):
    print(lote)

## Generamos lote por lote
generador = en_lotes(datos,10) ## Primero hago un generador que va consumiendo el iterador(lo que entrega la funcion)

print(next(generador))  ## Lote 1
print(next(generador))  ## Lote 2
print(next(generador))  ## Lote 3