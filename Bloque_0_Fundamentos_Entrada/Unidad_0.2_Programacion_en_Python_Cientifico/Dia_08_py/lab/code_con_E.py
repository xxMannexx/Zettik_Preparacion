import pandas as pd

detecciones = pd.DataFrame({
    "objeto": ["persona", "coche", "persona", "bici", "coche", "persona"],
    "confianza": [0.9, 0.7, 0.85, 0.95, 0.6, 0.8],
    "fotograma": [1, 1, 2, 2, 3, 3],
})

print(detecciones)

# Responde D4: confianza media por clase de objeto
print(detecciones.groupby("objeto")["confianza"].mean().round(3))
# objeto
# bici      0.950
# coche     0.650
# persona   0.850

# Varias agregaciones a la vez:
resumen = detecciones.groupby("objeto")["confianza"].agg(["count", "mean", "max"])
print(resumen.round(3))

# Groupby por varias claves:
por_fotograma = detecciones.groupby(["fotograma", "objeto"])["confianza"].mean()
print(por_fotograma)
