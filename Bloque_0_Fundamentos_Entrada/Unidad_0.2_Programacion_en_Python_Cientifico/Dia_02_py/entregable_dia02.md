# Entregable Día 02 — Funciones, ámbitos, closures y decoradores

## 1. Función como objeto

En Python una función también es un objeto. Eso significa que se puede asignar a otro nombre, pasar como argumento a otra función o guardarla dentro de una estructura.

En este ejemplo `referencia = f` no ejecuta la función, solamente crea otra referencia por nombre hacia el mismo objeto función.

Después, `funcion_argumento` se pasa como argumento a `referencia` sin paréntesis. Si pusiera `funcion_argumento()`, ya no estaría pasando la función, sino el resultado de ejecutarla.

```python
def f(funcion):
    return "Esta funcion es ", funcion.__name__

referencia = f

def funcion_argumento():
    pass

print(referencia(funcion_argumento))
```

Para demostrar también que una función puede almacenarse dentro de una estructura:

```python
catalogo = {
    "principal": f,
    "argumento": funcion_argumento
}

print(catalogo["principal"](catalogo["argumento"]))
```

Aquí estoy guardando los objetos función, no sus resultados.

---

## 2. Variádicos: `*args` y `**kwargs`

Los variádicos permiten recibir una cantidad variable de argumentos.

`*args` recoge los argumentos posicionales dentro de una **tupla** y `**kwargs` recoge los argumentos enviados como `clave=valor` dentro de un **diccionario**.

```python
def variadicos(*datos, **keyvals):
    return (
        f"Esta funcion recibe argumentos de tipo: "
        f"{type(datos).__name__} y {type(keyvals).__name__}"
    )

print(variadicos())
```

Aunque no mande ningún argumento, `datos` sigue siendo una tupla y `keyvals` sigue siendo un diccionario, solamente vacíos.

---

## 3. LEGB, `global` y `nonlocal`

La regla LEGB indica el orden en que Python busca un nombre:

**Local → Enclosing → Global → Built-in.**

Una asignación dentro de una función crea por defecto un nombre local. Por eso `x = 4` dentro de `legb()` no modifica el `x = 10` global, solamente lo sombrea mientras estamos dentro de la función.

```python
x = 10

def legb():
    x = 4
    print(x)

legb()
print(x)
```

Para modificar realmente el nombre global desde una función necesito usar `global`:

```python
x = 10

def funcion_global():
    global x
    x += 1
    print(x)

funcion_global()
print(x)
```

`nonlocal` sirve para reasignar un nombre del ámbito **Enclosing**, es decir, de una función envolvente.

```python
def enclosing():
    y = 3
    print(y)

    def funcion():
        nonlocal y
        y += 1
        return y

    return funcion
```

Aquí `y` pertenece a `enclosing()`, y `nonlocal y` indica que la función interna quiere modificar esa misma variable y no crear una local nueva.

---

## 4. Closure con estado

La función anterior también demuestra un **closure**.

Un closure ocurre cuando una función interna conserva una referencia hacia variables de su ámbito envolvente incluso después de que la función externa ya terminó.

```python
llamado = enclosing()

print(llamado(), llamado())
print(llamado.__closure__[0].cell_contents)
```

Cuando `enclosing()` termina, devuelve la función interna. Esa función sigue teniendo acceso a `y` porque quedó capturada dentro de una celda de cierre.

En CPython se puede inspeccionar con:

```python
llamado.__closure__
```

y el contenido actual de la celda con:

```python
llamado.__closure__[0].cell_contents
```

La idea importante es que el closure no guarda solamente una copia fija del valor. Conserva acceso a la variable capturada, por eso el estado puede seguir cambiando entre llamadas.

---

## 5. Decorador y late binding

Un decorador permite agregar lógica alrededor de una función sin modificar directamente el código de esa función.

Este decorador recibe `inicio` y `fin`, por eso tiene una capa adicional: primero recibe la configuración y después devuelve el decorador que recibe la función original.

```python
import functools

def validar_rango(inicio, fin):
    def decorador(funcion):
        @functools.wraps(funcion)
        def envoltura(*args, **kwargs):
            if not kwargs:
                if len(args) == 2:
                    return (
                        "El rango es incorrecto"
                        if args != (inicio, fin)
                        else funcion(*args, **kwargs)
                    )
                else:
                    return "El total de parametros es incorrecto debe ser de dos"
            else:
                return "No se aceptan valores clave:valor"

        return envoltura

    return decorador


@validar_rango(0, 100)
def sumar(inicio, fin):
    return sum(range(inicio, fin + 1))

print(sumar(1, 100))
```

La sintaxis `@validar_rango(0, 100)` termina aplicando el decorador a `sumar`. El nombre `sumar` queda apuntando a la función `envoltura`, mientras que la envoltura conserva acceso a la función original mediante un closure.

`functools.wraps(funcion)` no es lo que permite ejecutar la función original. El closure es lo que conserva esa referencia. `wraps` sirve para preservar metadatos como el nombre y la documentación.

La verificación mínima es:

```python
print(sumar.__name__)
```

y debe conservar el nombre:

```text
sumar
```

### Late binding

El late binding aparece cuando varias funciones creadas dentro de un bucle capturan la misma variable y consultan su valor después, cuando el bucle ya terminó.

Versión problemática:

```python
funciones = []

for i in range(3):
    funciones.append(lambda: i)

for f in funciones:
    print(f())
```

Las lambdas capturan la variable `i`, no una copia independiente de su valor en cada iteración.

La corrección consiste en fijar el valor actual como argumento por omisión:

```python
funciones = []

for i in range(3):
    funciones.append(lambda i=i: i)

for f in funciones:
    print(f())
```

Ahora cada lambda conserva su propio valor de `i`.

---

## Conclusión

Lo principal de este día es que las funciones también siguen el modelo de objetos del Día 1. Son objetos y los nombres simplemente apuntan hacia ellas.

Eso explica por qué puedo pasar funciones como argumentos, almacenarlas en estructuras y construir funciones que reciben o devuelven otras funciones.

LEGB define cómo se resuelven los nombres. `global` permite reasignar nombres del módulo y `nonlocal` nombres del ámbito envolvente.

Los closures permiten conservar referencias hacia variables del entorno donde una función fue creada. Los decoradores aprovechan eso para guardar acceso a la función original dentro de una envoltura y agregar lógica sin modificar directamente su código.

Finalmente, el late binding vuelve a mostrar que Python trabaja con referencias a variables y no necesariamente con una copia del valor que tenían al crear una función.
