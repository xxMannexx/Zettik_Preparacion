import functools

def repetir(veces):  # recibe el parámetro del decorador
    def decorador(funcion):  # el decorador propiamente dicho
        @functools.wraps(funcion)
        def envoltura(*args, **kwargs):
            for _ in range(veces):
                resultado = funcion(*args, **kwargs)
            return resultado

        return envoltura

    return decorador


@repetir(veces=3)  # repetir(3) devuelve el decorador, que se aplica
def saludar(nombre):
    print(f"Hola, {nombre}")


saludar("Ana")  # imprime el saludo 3 veces


def iniciando(funcion):
    @functools.wraps(funcion)
    def envoltura(*args, **kwargs):
        print(f"La funcion: {funcion.__name__} esta iniciando")
        resultado = funcion(*args, **kwargs)
        return resultado
    return envoltura

@iniciando
def sumar(x,y):
    return f"La suma es: {x+y}"

print(sumar(10,20))
