import numpy as np
import time


def seccion(titulo):
    print(f"\n{'=' * 72}\n{titulo}\n{'=' * 72}")


# ---------------------------------------------------------------------
# 1. Ventaja de la vectorización
# ---------------------------------------------------------------------

seccion("1. Vectorización: NumPy vs generador de Python")

rango = 1_000_000
array = np.arange(rango)

inicio_numpy = time.perf_counter()
resultado_numpy = (array ** 2).sum()
tiempo_numpy = time.perf_counter() - inicio_numpy

gen = (x**2 for x in range(rango))
inicio_gen = time.perf_counter()
resultado_gen = sum(gen)
tiempo_gen = time.perf_counter() - inicio_gen

print("resultado NumPy:", resultado_numpy)
print("resultado generador:", resultado_gen)
print(f"NumPy tardó: {tiempo_numpy * 1000:.2f} ms")
print(f"Generador tardó: {tiempo_gen * 1000:.2f} ms")
print(f"NumPy fue aproximadamente {tiempo_gen / tiempo_numpy:.2f} veces más rápido")


# ---------------------------------------------------------------------
# 2. dtype, nbytes, strides y desbordamiento
# ---------------------------------------------------------------------

seccion("2. dtype, memoria, strides y overflow")

for dtype in (np.int8, np.int32, np.float32, np.float64):
    a = np.array([1, 2, 3, 4], dtype=dtype)
    print(
        f"dtype={a.dtype}, nbytes={a.nbytes}, "
        f"shape={a.shape}, strides={a.strides}"
    )

int8_limite = np.array([127], dtype=np.int8)
with np.errstate(over="ignore"):
    int8_overflow = int8_limite + np.int8(1)

python_int = 127 + 1

print("np.int8 127 + 1:", int8_overflow)
print("int Python 127 + 1:", python_int)


# ---------------------------------------------------------------------
# 3. Normalización vectorizada
# ---------------------------------------------------------------------

seccion("3. Normalización vectorizada")

datos = np.array(
    [[10, 20, 30],
     [40, 50, 60]],
    dtype=np.int16,
)

normalizados = (datos - datos.mean()) / datos.std()

print(normalizados)
print("media:", normalizados.mean())
print("desviación:", normalizados.std())


# ---------------------------------------------------------------------
# 4. Broadcasting y operaciones por eje
# ---------------------------------------------------------------------

seccion("4. Sensores: axis y broadcasting")

temperaturas = np.array(
    [[20., 22., 24., 26.],
     [21., 23., 25., 27.],
     [19., 21., 23., 25.]],
    dtype=np.float16,
)

medias_sensor = temperaturas.mean(axis=0)
temperaturas_centradas = temperaturas - medias_sensor

print("medias por sensor:", medias_sensor)
print("shape medias:", medias_sensor.shape)
print("temperaturas centradas:\n", temperaturas_centradas)
print("medias después:", temperaturas_centradas.mean(axis=0))


# ---------------------------------------------------------------------
# 5. Operaciones por ejes sobre una matriz
# ---------------------------------------------------------------------

seccion("5. Operaciones por ejes")

matriz = np.array(
    [[1, 2, 3],
     [4, 5, 6],
     [7, 8, 9],
     [10, 11, 12]]
)

print("shape matriz:", matriz.shape)
print("suma total:", matriz.sum())
print("suma por columna axis=0:", matriz.sum(axis=0))
print("shape axis=0:", matriz.sum(axis=0).shape)
print("suma por fila axis=1:", matriz.sum(axis=1))
print("shape axis=1:", matriz.sum(axis=1).shape)
print("media por fila:", matriz.mean(axis=1))
print("máximo por columna:", matriz.max(axis=0))


# ---------------------------------------------------------------------
# 6. Strides y transposición como vista
# ---------------------------------------------------------------------

seccion("6. Strides y transposición")

print("dtype:", temperaturas.dtype)
print("shape:", temperaturas.shape)
print("strides:", temperaturas.strides)

transpuesta = temperaturas.T

print("shape T:", transpuesta.shape)
print("strides T:", transpuesta.strides)
print("transpuesta comparte memoria:", np.shares_memory(temperaturas, transpuesta))


# ---------------------------------------------------------------------
# 7. Vista frente a copia
# ---------------------------------------------------------------------

seccion("7. Vista frente a copia")

array = np.array(
    [[1, 2, 3],
     [4, 5, 6],
     [7, 8, 9]]
)

vista = array[1, 0:2]
copia = array[2, [1, 2]]

vista[1] = 10
copia[1] = 10

print("vista:", vista)
print("copia por indexación avanzada:", copia)
print("array original:\n", array)
print("vista comparte:", np.shares_memory(array, vista))
print("copia comparte:", np.shares_memory(array, copia))


# ---------------------------------------------------------------------
# 8. Caso de imagen: brillo seguro
# ---------------------------------------------------------------------

seccion("8. Imagen uint8: brillo seguro")

imagen = np.array([250, 252, 255], dtype=np.uint8)

brillo_alto = np.clip(
    imagen.astype(np.uint16) + 10,
    0,
    255,
).astype(np.uint8)

print("original:", imagen)
print("brillo alto:", brillo_alto)


# ---------------------------------------------------------------------
# 9. Celsius a Fahrenheit
# ---------------------------------------------------------------------

seccion("9. Celsius a Fahrenheit")

celsius = np.array([0, 20, 37, 100])
fahrenheit = (celsius * 1.8) + 32

print(fahrenheit)


# ---------------------------------------------------------------------
# 10. Broadcasting por canal RGB
# ---------------------------------------------------------------------

seccion("10. Broadcasting por canal RGB")

imagen_rgb = np.ones((2, 2, 3))
escala = np.array([0.5, 1.0, 1.5])

escalada = imagen_rgb * escala

print("shape:", escalada.shape)
print("píxel [0,0]:", escalada[0, 0])