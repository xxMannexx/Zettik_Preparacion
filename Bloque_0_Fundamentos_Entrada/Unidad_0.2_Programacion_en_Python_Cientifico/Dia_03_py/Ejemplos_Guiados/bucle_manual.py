datos = [10,20,30]


## Equivalente a for x in datos: print(x)

it = iter(datos)

while True:
    try:
                            ##Hacemos un bucle manual sabiendo que un iterador para en StopIteration
        dato = next(it)
        print(dato)
    except StopIteration:
        break