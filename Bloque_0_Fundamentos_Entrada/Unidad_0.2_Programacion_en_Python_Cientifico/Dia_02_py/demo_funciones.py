import functools

## 1.	Función como objeto: la demostración de asignar una función a otro nombre, pasarla como argumento y almacenarla en una estructura.

def f(funcion):
    return "Esta funcion es ", funcion.__name__

referencia = f

def funcion_argumento():
    pass

print(referencia(funcion_argumento))

## 2.	Variádicos: una función con *args y **kwargs que muestre los tipos (tupla y diccionario) en que se recogen los argumentos.

def variadicos(*datos,**keyvals):
    return f"Esta funcion recibe argumentos de tipo: {type(datos).__name__} y {type(keyvals).__name__}"

print(variadicos())

## 3.	LEGB: un ejemplo que demuestre que la asignación crea un nombre local, y el efecto de global/nonlocal.

x = 10

def legb():
    x = 4
    print(x)

def funcion_global():
    global x
    print(x)

legb()
funcion_global()

def enclosing():
    y = 3
    print(y)

    def funcion():
        nonlocal y
        y += 1; return y
    return funcion

## 4.	Closure con estado: una fábrica que produzca un closure con estado retenido, verificado por inspección de __closure__. Esta misma funcion genera un closure

llamado = enclosing()
print(llamado(), llamado())
print(llamado.__closure__[0].cell_contents)


## 5.	Decorador: un decorador funcional (medición, registro o caché) con functools.wraps, con la verificación de que preserva el nombre de la función; y la demostración del late binding con su corrección.


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

## Late blinding

funciones = []

# for i in range(3): funciones.append(lambda : i)
#
# for f in funciones:
#     print(f())

## bien hecho
for i in range(3): funciones.append(lambda i = i: i)

for f in funciones:
    print(f())