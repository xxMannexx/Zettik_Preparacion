# Entregable Día 03 — Iteradores, generadores y evaluación perezosa

## 1. Protocolo manual

Un `for` en Python no necesita conocer si está recorriendo una lista, una cadena, un archivo o cualquier otro tipo concreto. Lo que utiliza es el protocolo de iteración.

Primero se obtiene un iterador con `iter()`. Después se van pidiendo los elementos uno por uno con `next()`. Cuando ya no quedan elementos, el iterador lanza `StopIteration` y ahí termina el recorrido.

```python
lista = [10,20,30]
iteracion = iter(lista)

while True:
    try:
        print(next(iteracion))
    except StopIteration:
        break
```

La secuencia es:

`iterable -> iter() -> iterador -> next() -> next() -> ... -> StopIteration`

El punto importante es que `StopIteration` no representa un fallo inesperado en este caso, sino la señal que indica que el iterador ya se agotó.

---

## 2. Agotamiento

Un generador también es un iterador, por lo que es de una sola pasada.

Para demostrarlo utilizo los mismos números pares de dos maneras distintas: primero con una expresión generadora y después con una comprensión de lista.

```python
numeros_pares = (x for x in range(100) if x % 2 == 0)
numeros_parlista = [x for x in range(100) if x % 2 == 0]

print(f"Primera pasada generador: {sum(numeros_pares)}")
print(f"Primera pasada lista: {sum(numeros_parlista)}")

print(f"Segunda pasada generador: {sum(numeros_pares)}")
print(f"Segunda pasada lista: {sum(numeros_parlista)}")
```

La primera suma del generador consume todos sus elementos.

Cuando se intenta hacer la segunda suma, el generador ya no tiene valores disponibles y por eso el resultado es `0`.

La lista funciona diferente. Sus elementos sí están materializados y cada nuevo recorrido puede obtener un iterador nuevo sobre esos mismos datos.

Por eso una lista puede recorrerse varias veces, mientras que un generador queda agotado después de consumirlo.

---

## 3. Generador con estado

Un generador creado con `yield` no ejecuta todo su cuerpo de una sola vez.

Cada vez que llega a un `yield`, entrega un valor y suspende la ejecución. En ese momento conserva sus variables locales y el punto exacto donde quedó detenido.

```python
def cuenta_regresiva(n):
    print("Iniciando")
    while n >= 1:
        yield n
        n -= 1
        print("Reanudando despues del valor anterior" if n > 0 else "Finalizado")

g = cuenta_regresiva(10)

for n in g:
    print(n)
```

Cuando se llama `g = cuenta_regresiva(10)` se crea el objeto generador.

Al comenzar el recorrido, el generador ejecuta hasta `yield n`, entrega el valor y queda suspendido.

Cuando se solicita el siguiente elemento, continúa exactamente después del `yield` anterior. No comienza nuevamente desde el principio.

La diferencia principal entre `yield` y `return` es que `yield` entrega un valor y suspende conservando el estado, mientras que `return` termina la función.

---

## 4. Evaluación perezosa

La evaluación perezosa significa que los valores se calculan solamente cuando se necesitan.

Esto permite representar incluso una secuencia infinita, siempre que no se intente materializar completa.

```python
def desde_n(num):
    sumador = 0
    while True:
        yield num + sumador
        sumador += 1

generador = desde_n(100)
print(list(itertools.islice(generador, 5)))
```

El resultado es:

```text
[100, 101, 102, 103, 104]
```

Aunque `desde_n()` representa un flujo infinito, `islice` solicita únicamente los cinco valores necesarios.

También se compara el tamaño del generador y de la lista:

```python
print(sys.getsizeof(numeros_pares))
print(sys.getsizeof(numeros_parlista))
```

La comprensión de lista materializa todos sus elementos, por lo que su memoria crece aproximadamente como `O(N)`.

La expresión generadora conserva solamente el estado necesario para continuar produciendo valores, por lo que su uso de memoria se modela como `O(1)` para este tipo de procesamiento.

La cifra exacta de `sys.getsizeof()` depende de la versión e implementación de Python; lo importante aquí es el contraste entre almacenar toda la colección y conservar únicamente el estado del generador.

---

## 5. Pipeline de generadores

Los generadores pueden encadenarse para construir un pipeline.

En lugar de generar una lista intermedia después de cada transformación, una etapa solicita un elemento a la etapa anterior solamente cuando lo necesita.

```python
datos = [x for x in range(100)]

def solo_pares(iterable):
    for i in iterable:
        if i % 2 == 0:
            yield i

def potencia(flujo):
    for i in flujo:
        yield i**2

pipeline = potencia(solo_pares(datos))
print(type(pipeline).__name__)
print(list(pipeline))
```

Antes de consumirlo, `type(pipeline).__name__` debe mostrar:

```text
generator
```

Eso demuestra que la composición sigue siendo perezosa.

Cuando `potencia()` necesita un valor, lo pide a `solo_pares()`. `solo_pares()` obtiene datos del iterable original hasta encontrar uno válido y lo entrega mediante `yield`.

De esta manera no se materializan resultados intermedios: cada valor atraviesa el pipeline conforme es demandado.

---

## Conclusión

El modelo de iteración de Python se basa en `iter()`, `next()` y `StopIteration`.

Un iterable puede producir iteradores nuevos, mientras que un iterador conserva una posición interna que avanza hasta agotarse.

Los generadores son iteradores construidos con `yield`. Pueden suspender su ejecución y continuar más adelante conservando sus variables locales y el punto exacto de ejecución.

De esta suspensión se deriva la evaluación perezosa: los datos se producen solamente cuando son necesarios.

Esto evita materializar colecciones completas, permite trabajar con memoria aproximadamente constante y hace posible procesar flujos mayores que la memoria disponible o incluso secuencias infinitas.

Finalmente, los pipelines de generadores permiten encadenar varias transformaciones sin crear colecciones intermedias. Cada etapa solicita información a la anterior únicamente cuando el consumidor final pide un nuevo valor.

---

## Script utilizado — `demo_iteracion.py`

```python
import sys
import itertools

lista = [10,20,30]
iteracion = iter(lista)
while True:
    try:
        print(next(iteracion))
    except StopIteration:
        break

numeros_pares = (x for x in range(100) if x % 2 == 0)
numeros_parlista = [x for x in range(100) if x % 2 == 0]

print(f"Primera pasada generador: {sum(numeros_pares)}")
print(f"Primera pasada lista: {sum(numeros_parlista)}")
print(f"Segunda pasada generador: {sum(numeros_pares)}")
print(f"Segunda pasada lista: {sum(numeros_parlista)}")

def cuenta_regresiva(n):
    print("Iniciando")
    while n >= 1:
        yield n
        n -= 1
        print("Reanudando despues del valor anterior" if n > 0 else "Finalizado")

g = cuenta_regresiva(10)
for n in g:
    print(n)

def desde_n(num):
    sumador = 0
    while True:
        yield num + sumador
        sumador += 1

generador = desde_n(100)
print(list(itertools.islice(generador, 5)))

print(sys.getsizeof(numeros_pares))
print(sys.getsizeof(numeros_parlista))

datos = [x for x in range(100)]

def solo_pares(iterable):
    for i in iterable:
        if i % 2 == 0:
            yield i

def potencia(flujo):
    for i in flujo:
        yield i**2

pipeline = potencia(solo_pares(datos))
print(type(pipeline).__name__)
print(list(pipeline))
```
