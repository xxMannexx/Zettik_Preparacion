## Muestra del como un iterador se agota

g = (x for x in range(5)) ## Creamos un generador que a su vez es un iterador
print(sum(g))  ## Dara 10 consumio los 5 valores que genero g y los agota
print(sum(g))  ## Dara 0 g ya esta agotado y no genera un iterador nuevo el era un iterador

## Demostracion de que un iterable genera un iterador cada que es consumido

lista = [0,1,2,3,4]

print(sum(lista)) # 10: iter(lista) produce un iterador nuevo
print(sum(lista)) # 10: iter(lista) produce OTRO iterador nuevo; la lista persiste
