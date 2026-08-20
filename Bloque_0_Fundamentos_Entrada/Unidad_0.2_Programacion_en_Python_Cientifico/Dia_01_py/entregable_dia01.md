# Entregable Día 01 — Modelo de ejecución y modelo de datos de Python

## 1. Tripleta de objetos

En Python todo lo que usamos como dato es un objeto. Para inspeccionarlo puedo fijarme en tres cosas: identidad, tipo y valor.

`id(objeto)` me permite observar la identidad del objeto durante esa ejecución. En CPython esa identidad corresponde a una dirección asociada al objeto en memoria. No me interesa memorizar el número exacto, sino usarlo para comparar si dos nombres están apuntando o no al mismo objeto.

`type(objeto)` me dice qué tipo tiene el objeto. El tipo pertenece al objeto, no al nombre que lo referencia.

El valor es el contenido que representa el objeto. Dependiendo del tipo, ese valor puede ser mutable o inmutable.

Código usado:

```python
import dis

for objeto in [2, (1,2,3), ['carro','mujer'], {"clave": "valor"}]:
    print(
        f"ID: {id(objeto):15} "
        f"Valor: {repr(objeto):20} "
        f"Tipo: {type(objeto).__name__:8}"
    )
```

Salida observada:

```text
ID:        11370064 Valor: 2                    Tipo: int
ID: 130485447117056 Valor: (1, 2, 3)            Tipo: tuple
ID: 130485453069504 Valor: ['carro', 'mujer']   Tipo: list
ID: 130485448712960 Valor: {'clave': 'valor'}   Tipo: dict
```

Con esto puedo ver que cada objeto tiene su propia identidad, su tipo y su valor.

---

## 2. Aliasing demostrado

El aliasing ocurre cuando dos nombres diferentes apuntan exactamente al mismo objeto.

En un objeto mutable esto se vuelve observable porque puedo cambiar el objeto en sitio. Por ejemplo, una lista sí permite hacer `append`, y como `a` y `b` apuntan al mismo objeto, el cambio hecho desde `b` también se observa desde `a`.

Código usado:

```python
a = [5,7,9]
b = a

b.append(12)
print(f"a = {a} y b = {b}")

if a is b:
    print(
        f"Tanto A como B apuntan al mismo objeto\n"
        f"Id de a: {id(a):18} Id de b: {id(b):18}"
    )
else:
    print("No apuntan al mismo objeto")
```

La parte importante es que `a is b` da `True`, porque ambos nombres apuntan a la misma identidad. Después de `b.append(12)`, tanto `a` como `b` muestran la lista modificada.

Con un inmutable ocurre algo diferente. También puede existir aliasing al principio, pero como el objeto no se puede mutar en sitio, una operación que parece cambiarlo en realidad crea otro objeto y revincula el nombre.

Código usado:

```python
x = 10
y = x

if x is y:
    print(
        f"Aqui apuntan al mismo objeto\n"
        f"Id de x: {id(x):18} Id de y: {id(y):18}"
    )
else:
    print(
        f"No apuntan al mismo objeto\n"
        f"Id de x: {id(x):18} Id de y: {id(y):18}"
    )

y = y + 3

if y is x:
    print(
        f"Aqui tanto x como y apuntan al mismo objeto\n"
        f"Id de x: {id(x):18} Id de y: {id(y):18}"
    )
else:
    print(
        f"Aqui no apuntan al mismo objeto\n"
        f"Id de x: {id(x):18} Id de y: {id(y):18}"
    )
```

Primero `x` y `y` apuntan al mismo objeto. Después, `y = y + 3` no modifica el entero `10`: crea otro objeto y el nombre `y` queda revinculado. `x` sigue intacto.

Por eso digo que el aliasing es observable de forma directa con mutables, pero con inmutables no existe mutación en sitio que permita observar el efecto compartido.

---

## 3. Paso de argumentos

Python usa una semántica de `call by sharing`: al llamar una función se comparte el objeto, pero no el vínculo del nombre del llamador.

Eso significa que, si una función muta el objeto recibido, el cambio sí se ve afuera. Pero si solamente reasigna su parámetro a otro objeto, ese nuevo vínculo existe de forma local dentro de la función.

Código usado:

```python
def mutable(argumento):
    argumento.append(5)
    return id(argumento)

def reasignacion(argumento):
    argumento = [3,9,0]
    return id(argumento)

lista = [15,8,0,2]

print(
    f"ID objeto principal: {id(lista):18}\n"
    f"Valores objeto principal: {lista}"
)

print(
    f"ID objeto despues de pasarla por la funcion de mutabilidad: "
    f"{mutable(lista):18}\n"
    f"Valores de el objeto principal: {repr(lista)}"
)

print(
    f"ID objeto de la funcion reasignacion: "
    f"{reasignacion(lista):18}\n"
    f"Valores de el objeto principal: {repr(lista)}"
)
```

Salida observada:

```text
ID objeto principal:    134262696543680
Valores objeto principal: [15, 8, 0, 2]

ID objeto despues de pasarla por la funcion de mutabilidad:    134262696543680
Valores de el objeto principal: [15, 8, 0, 2, 5]

ID objeto de la funcion reasignacion:    134262696488064
Valores de el objeto principal: [15, 8, 0, 2, 5]
```

La primera función conserva el mismo `id`, por lo que está mutando el mismo objeto que recibió desde el llamador.

La segunda crea una lista nueva dentro de la función. Su `id` es diferente, y por eso la variable `lista` del llamador sigue apuntando al objeto original.

---

## 4. Argumento por omisión mutable

Un argumento por omisión mutable puede generar un defecto porque el objeto usado como valor por omisión se crea una sola vez cuando se define la función.

Por eso, si uso una lista como valor por omisión, las llamadas posteriores reutilizan el mismo objeto y el estado se va acumulando.

Versión defectuosa:

```python
def agregar_defectuoso(argumento, listafuncion=[]):
    listafuncion.append(argumento)
    return listafuncion

print(agregar_defectuoso(10))
print(agregar_defectuoso(11))
print(agregar_defectuoso(12))
```

Salida:

```text
[10]
[10, 11]
[10, 11, 12]
```

La lista no se reinicia en cada llamada porque se sigue usando el mismo objeto.

La corrección consiste en usar `None` como centinela y crear la lista dentro de la función cuando haga falta.

```python
def acumula_bien(x, acc=None):
    if acc is None:
        acc = []
    acc.append(x)
    return acc

print(acumula_bien(1), acumula_bien(2), acumula_bien(3))
```

Salida:

```text
[1] [2] [3]
```

Ahora cada llamada sin argumento explícito crea una lista nueva, así que ya no se comparte el estado accidentalmente.

---

## 5. Tipado fuerte y bytecode

Python es dinámicamente tipado porque el tipo vive en el objeto, no en el nombre. También es fuertemente tipado porque no hace conversiones silenciosas entre tipos incompatibles.

Cuando una operación no tiene sentido entre los objetos recibidos, Python produce `TypeError` en vez de decidir por su cuenta qué conversión debería hacer.

Tres operaciones usadas para provocar `TypeError` fueron:

```python
1 + "3"
(1,2,3) + 5
4 + [2]
```

Las correcciones explícitas que usé fueron:

```python
print(f"Correccion debe ser: {1 + int('3')}")
print(f"Correccion debe ser: {(1,2,3) + (5,)}")
print(f"Correccion debe ser: {[2] + [4.6]}")
```

La idea es que la conversión o adaptación del tipo sea explícita. Python no debe inventar por mí si quiero sumar números, concatenar secuencias o hacer otra operación.

Para observar el bytecode usé el módulo estándar `dis`:

```python
dis.dis(acumula_bien)
```

Parte de la salida observada:

```text
RESUME                   0
LOAD_FAST_BORROW         1 (acc)
POP_JUMP_IF_NOT_NONE     3
BUILD_LIST               0
STORE_FAST               1 (acc)
LOAD_FAST_BORROW         1 (acc)
LOAD_ATTR                1 (append + NULL|self)
LOAD_FAST_BORROW         0 (x)
CALL                     1
POP_TOP
LOAD_FAST_BORROW         1 (acc)
RETURN_VALUE
```

Esto demuestra que CPython no ejecuta directamente el código fuente como instrucciones de CPU. Primero trabaja con una representación intermedia de bytecode y la máquina virtual de Python ejecuta esas instrucciones.

---

## Conclusión

Lo principal que me llevo de este día es que en Python los nombres no son cajas que contienen valores. Son referencias a objetos.

Cada objeto tiene identidad, tipo y valor. La asignación puede hacer que varios nombres apunten al mismo objeto, y ahí aparece el aliasing.

La diferencia entre mutables e inmutables explica por qué algunas modificaciones se ven desde varias referencias y otras operaciones terminan creando objetos nuevos.

En funciones se mantiene la misma idea: se comparte el objeto, pero no el vínculo del nombre. Por eso mutar puede afectar al llamador y reasignar el parámetro no.

Finalmente, Python combina tipado dinámico con tipado fuerte: los nombres pueden apuntar a objetos de distintos tipos durante la ejecución, pero las operaciones incompatibles producen errores en lugar de coerciones silenciosas.
