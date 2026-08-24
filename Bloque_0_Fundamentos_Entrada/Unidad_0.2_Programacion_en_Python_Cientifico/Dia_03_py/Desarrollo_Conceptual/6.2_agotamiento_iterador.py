## ITERADOR

gen = (x for x in range(3))  ## Esto es una expresion generadora crea un iterador de un solo uso una vez consumido se vacia

print(list(gen))  ## Se consume el iterador
print(list(gen))  ## El iterador ya fue consumido no esta materializado y ya no tien elementos

## ITERABLE

lista = [x for x in range(3)] ## Gernera un iterable en este caso una lista, un iterable puede contener tantos iteradores como sea consumido
print(lista) , print(lista) ## Se consume 2 veces genera un iterador cada vez (esta materializada) y no se agota


## Sin embargo en memoria el consumo es muy distinto


