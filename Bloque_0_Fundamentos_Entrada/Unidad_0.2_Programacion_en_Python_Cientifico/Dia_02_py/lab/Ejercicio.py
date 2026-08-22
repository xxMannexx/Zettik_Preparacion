import functools

def validar_rango(inicio,fin):
    def decorador(funcion):
        @functools.wraps(funcion)
        def envoltura(*args, **kwargs):
            if not kwargs:
                if len(args) == 2:
                    return "El rango es incorrecto" if args != (inicio,fin,) else  funcion(*args, **kwargs)
                else:
                    return "El total de parametros es incorrecto debe ser de dos"

            else:
                return "No se aceptan valores clave:valor"
        return envoltura
    return decorador

@validar_rango(0,100)
def sumar(inicio,fin):
    return sum(range(inicio,fin+1))


print(sumar(1,100))