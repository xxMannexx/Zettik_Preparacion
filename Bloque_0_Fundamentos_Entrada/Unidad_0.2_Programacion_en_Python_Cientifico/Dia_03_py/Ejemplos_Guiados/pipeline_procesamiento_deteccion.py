import itertools

## Simulamos un flujo (potencialmente infinito) de detecciones (objeto,confianza)

def flujo_detecciones():
    import random
    objetos = ["persona","coche","bicicleta","perro"]  ## Clases que puede detectar
    while True:  ## Generamos un flujo infinito como la deteccion de una camara
        yield random.choice(objetos), round(random.random(),2)


## Etapas del pipeline, todas ellas perezosas

def solo_fiables(flujo,umbral): ## Generamos una funcion que recibe el flujo de deteccion y lo filtra a solo que si es confiable (ubral => 0.7# )
    for obj, conf in flujo:
        if conf >= umbral:
            yield (obj,conf)

## Ahora genramos una funcion que filtre de estos que cumplen la confianza solo los que sean personas
def solo_personas(flujo):
    for obj, conf in flujo:
        if obj == "persona":
            yield (obj,conf)

## Compones el pipeline
random_seed = __import__("random").seed(0) ## Reproducibilidad
pipeline = solo_personas(solo_fiables(flujo_detecciones(),umbral=0.7))

primeras = list(itertools.islice(pipeline, 10)) # consume solo lo necesario del flujo infinito

print(primeras)  # 3 detecciones de persona con confianza >= 0.7