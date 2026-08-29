import pandas as pd

detecciones = pd.DataFrame({
    "objeto": ["persona", "coche", "bici"],
    "confianza": [0.9, 0.7, 0.95],
})
metadatos = pd.DataFrame({
    "objeto": ["persona", "coche", "avion"],
    "categoria": ["humano", "vehiculo", "vehiculo"],
})

# INNER: solo las claves en AMBOS (persona, coche; no bici ni avion)
inner = pd.merge(detecciones, metadatos, on="objeto", how="inner")
print(inner)
print(f"inner: {len(inner)} filas")  # 2 (sin bici ni avion)

# LEFT: todas las detecciones; 'bici' sin metadatos -> NaN en 'categoria'
left = pd.merge(detecciones, metadatos, on="objeto", how="outer")

print(f"left: {len(left)} filas")  # 3 (bici con NaN en categoria)
print(left)

# CONCAT: apilar lotes con el mismo esquema
lote1 = pd.DataFrame({"objeto": ["persona"], "confianza": [0.9]})
lote2 = pd.DataFrame({"objeto": ["coche"], "confianza": [0.7]})
print(pd.concat([lote1, lote2], ignore_index=True))  # 2 filas
