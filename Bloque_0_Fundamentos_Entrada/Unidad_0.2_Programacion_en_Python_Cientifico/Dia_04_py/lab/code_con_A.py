## Hacemos una funcion en la que se detecta (en lo profunco)

def nivel_3():
    raise ValueError("Dato invalido en el nivel 3")


def nivel_2():
    return nivel_3()  ## no maneja, la excepcion lo atraviesa

def nivel_1():
    try:
        return nivel_2()
    except ValueError as e:
        print(f"Manejado en el nivel_1: {e}")

nivel_1()

## La excepción se lanza en nivel_3, atraviesa nivel_2 (que no la maneja)
# sin que `nivel_2` tenga que hacer nada explícito,
# y se maneja en nivel_1.

## Lanzar excepciones

def raiz_cuadrada(x):
    if x < 0:
        raise ValueError(f"No se puede calcular la raiz cuadrada de un negativo: {x}")
    return x ** 0.5

print(raiz_cuadrada(-9))