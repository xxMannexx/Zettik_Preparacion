# Entregable Día 07 — NumPy: arrays, vectorización y broadcasting

## Objetivo

Demostrar de forma ejecutable los fenómenos principales del Día 7: velocidad del `ndarray`, efecto del `dtype`, vectorización, broadcasting, vistas frente a copias, operaciones por ejes y modelo de memoria mediante `strides`.

## 1. Ventaja medida de la vectorización

Se comparó la suma de cuadrados de un millón de valores mediante NumPy y mediante un generador de Python.

```python
rango = 1_000_000
array = np.arange(rango)

inicio_numpy = time.perf_counter()
resultado_numpy = (array ** 2).sum()
tiempo_numpy = time.perf_counter() - inicio_numpy

gen = (x**2 for x in range(rango))
inicio_gen = time.perf_counter()
resultado_gen = sum(gen)
tiempo_gen = time.perf_counter() - inicio_gen
```

La operación de NumPy trabaja sobre el array completo y delega el recorrido interno a código compilado. El generador sigue ejecutando iteración a nivel de Python. Por eso NumPy reduce fuertemente la sobrecarga del intérprete por elemento.

## 2. `dtype`, memoria y desbordamiento

Se inspeccionan arrays equivalentes con:

```python
np.int8
np.int32
np.float32
np.float64
```

Para cada uno se muestran `dtype`, `nbytes`, `shape` y `strides`.

El número del tipo indica cuántos bits utiliza cada elemento. Por ejemplo, `int8` ocupa 1 byte y `int32` ocupa 4 bytes. El tipo determina tanto la memoria utilizada como el rango y la precisión disponibles.

También se demuestra el desbordamiento:

```python
int8_limite = np.array([127], dtype=np.int8)
int8_overflow = int8_limite + np.int8(1)
```

El resultado es `-128` porque `int8` tiene rango fijo. En contraste:

```python
127 + 1
```

con un `int` de Python produce `128`, ya que los enteros de Python tienen precisión arbitraria.

## 3. Normalización vectorizada

Se normaliza un array completo sin escribir un bucle:

```python
normalizados = (datos - datos.mean()) / datos.std()
```

Restar la media centra los datos alrededor de cero. Dividir entre la desviación estándar reescala la dispersión para que sea aproximadamente uno.

## 4. Broadcasting y medias por sensor

Se trabajó con una matriz de tres mediciones y cuatro sensores:

```python
medias_sensor = temperaturas.mean(axis=0)
temperaturas_centradas = temperaturas - medias_sensor
```

`axis=0` colapsa las filas y deja una media por columna. El resultado `medias_sensor` tiene forma `(4,)`.

La resta entre `(3,4)` y `(4,)` funciona mediante broadcasting: NumPy alinea las formas desde la derecha y aplica el vector de cuatro medias a cada fila.

## 5. Operaciones por ejes

Sobre una matriz de forma `(4,3)` se calculan:

```python
matriz.sum()
matriz.sum(axis=0)
matriz.sum(axis=1)
matriz.mean(axis=1)
matriz.max(axis=0)
```

`axis=0` colapsa las filas y deja un resultado por columna. `axis=1` colapsa las columnas y deja un resultado por fila.

## 6. `strides` y transposición

Sobre una matriz `float16` de forma `(3,4)` se observó el modelo:

```text
shape: (3, 4)
strides: (8, 2)
```

Cada `float16` ocupa 2 bytes. Avanzar una columna cuesta 2 bytes y avanzar una fila completa cuesta 8 bytes.

Al transponer:

```text
shape T: (4, 3)
strides T: (2, 8)
```

Los datos no se reorganizan. Solo cambian la forma y los pasos con los que NumPy interpreta el mismo bloque de memoria.

La verificación:

```python
np.shares_memory(temperaturas, temperaturas.T)
```

produce `True`, demostrando que la transposición es una vista.

## 7. Vista frente a copia

Se utiliza slicing básico:

```python
vista = array[1, 0:2]
```

y una indexación avanzada:

```python
copia = array[2, [1, 2]]
```

La vista comparte memoria con el array original; por ello modificarla modifica también el original.

La indexación avanzada genera un array con memoria independiente. La evidencia se obtiene con:

```python
np.shares_memory(array, vista)  # True
np.shares_memory(array, copia)  # False
```

## 8. Brillo seguro de una imagen `uint8`

Para aumentar brillo sin provocar overflow:

```python
brillo_alto = np.clip(
    imagen.astype(np.uint16) + 10,
    0,
    255
).astype(np.uint8)
```

La conversión a `uint16` se realiza antes de sumar para ampliar temporalmente el rango. `np.clip` satura los valores al intervalo válido `[0,255]`, y finalmente se vuelve a `uint8`.

## 9. Conversión vectorizada Celsius a Fahrenheit

```python
celsius = np.array([0, 20, 37, 100])
fahrenheit = (celsius * 1.8) + 32
```

La fórmula se aplica a todos los elementos del array sin escribir un bucle de Python.

## 10. Broadcasting por canal RGB

Una imagen de forma `(2,2,3)` se multiplica por:

```python
escala = np.array([0.5, 1.0, 1.5])
```

El vector `(3,)` se alinea con la última dimensión de `(2,2,3)`. El resultado mantiene forma `(2,2,3)` y aplica un factor distinto a cada canal.

## Conclusión

El `ndarray` obtiene su eficiencia de una representación homogénea y compacta en memoria y de operaciones implementadas en código compilado. El `dtype` determina memoria, rango y precisión; la vectorización evita bucles de Python; el broadcasting permite combinar formas compatibles; y el modelo de `strides` explica por qué vistas y transposiciones pueden reutilizar el mismo bloque de memoria sin copiar datos.

La distinción entre slicing e indexación avanzada es crítica: un rebanado puede compartir memoria con el original, mientras que la indexación avanzada produce una copia independiente.
