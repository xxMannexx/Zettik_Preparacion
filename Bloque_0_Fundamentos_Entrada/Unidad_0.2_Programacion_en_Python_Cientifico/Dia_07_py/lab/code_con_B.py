import numpy as np

a = np.array([127], dtype=np.int8)  # int8: rango [-128, 127]
print(a + 1)  # [-128]  <- ¡desbordamiento! 127 + 1 da la vuelta a -128
print(a.dtype, a.nbytes)  # int8, 1 byte

# Contraste con el int de Python (precisión arbitraria, Día 1):
print(127 + 1)

#3 La eleccion del dtype
a = np.array([1, 2, 3])  # dtype inferido: int64 (en la mayoría de plataformas)
b = np.array([1.0, 2.0, 3.0])  # float64
c = np.array([1, 2, 3], dtype=np.float32)  # tipo explícito: float32 (mitad de memoria que float64)
print(a.dtype, b.dtype, c.dtype)  # int64 float64 float32

# Memoria: una imagen de 1920x1080 en uint8 (un byte por píxel) vs float64 (ocho bytes)
print(f"uint8:   {1920 * 1080 * 1:>10,} bytes")  # ~2 MB
print(f"float64: {1920 * 1080 * 8:>10,} bytes")  # ~16 MB  (ocho veces más)
# La elección del dtype determina el consumo de memoria, crítico al procesar muchas imágenes.
