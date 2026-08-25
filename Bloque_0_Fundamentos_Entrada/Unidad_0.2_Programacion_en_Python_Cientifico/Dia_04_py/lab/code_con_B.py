def dividir(a,b):
    try:
        return a / b    ## # con b=0, lanza ZeroDivisionError (no llega a retornar)
    except ZeroDivisionError:
        return "No se permite la division por 0"
    finally:
        print("Finally")   # se ejecuta SIEMPRE, antes de que la función retorne

print(dividir(2,0))


## Demostracion de que finally se ejecuta en cualquier caso

def f():
    try:
        return "Del try"
    finally:
        print("finally antes de retornar")

print(f())

## Capturar varios tipos.
def procesar(dato):
    try:
        numero = int(dato)
        return 100 / numero
    except ValueError:                       # int() de algo no numérico
        return "no es un número"
    except ZeroDivisionError:                # división por cero
        return "no puede ser cero"
    else:
        print("procesado sin errores")
# Varios tipos a la vez: except (ValueError, TypeError) as e
print(procesar(2))

