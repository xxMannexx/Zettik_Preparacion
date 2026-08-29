import numpy as np

temperaturas = np.array([
    [20., 22., 24., 26.],
    [21., 23., 25., 27.],
    [19., 21., 23., 25.]
], dtype=np.float16)

medias_sensor = temperaturas.mean(axis=0)
print(medias_sensor)

temperaturas_centradas = temperaturas - medias_sensor

print("shape medias:", medias_sensor.shape)
print(temperaturas_centradas)
print("medias después:", temperaturas_centradas.mean(axis=0))

print("dtype:", temperaturas.dtype)
print("shape:", temperaturas.shape)
print("strides:", temperaturas.strides)

transpuesta = temperaturas.T

print("shape T:", transpuesta.shape)
print("strides T:", transpuesta.strides)
print("comparte memoria:", np.shares_memory(temperaturas, transpuesta))

vista = temperaturas[:, 1:3]
copia = temperaturas[:, [1, 2]]

print("vista comparte:", np.shares_memory(temperaturas, vista))
print("copia comparte:", np.shares_memory(temperaturas, copia))