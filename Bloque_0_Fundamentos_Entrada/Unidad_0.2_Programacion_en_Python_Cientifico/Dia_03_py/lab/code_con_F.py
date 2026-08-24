import itertools

## Pipeline de etapas generadoras: cada una consume de a anterior perezosamente

def leer(datos):
    ## Etapa 1: produce los datos de uno en uno

    for d in datos:
        yield d

def filtrar_validos(flujo,umbral):
    ## Etapa 2 filtra perezosamente

    for x in flujo:
        if x >= umbral:
            yield x

def escalar(flujo,factor):
    ## Etapa 3 transformar perezosamente

    for x in flujo:
        yield x * factor

datos = [0.2,0.9,0.5,0.8,0.1,0.95]

## Componer el pipeline
pipeline = escalar(filtrar_validos(leer(datos),umbral=0.5),factor=100)

print(type(pipeline).__name__)
print(list(pipeline))