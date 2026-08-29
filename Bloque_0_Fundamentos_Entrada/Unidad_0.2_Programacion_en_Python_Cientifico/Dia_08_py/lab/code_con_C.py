import pandas as pd

df = pd.DataFrame({"obj": ["persona", "coche", "bici"],
                   "conf": [0.9, 0.7, 0.95]},
                  index=["d1", "d2", "d3"])

print(df)

# Por ETIQUETA (.loc): usa etiquetas del índice y nombres de columna
print(df.loc["d1", "conf"])  # 0.9  (fila 'd1', columna 'conf')
print(df.loc["d1":"d2"])  # filas 'd1' a 'd2' (INCLUSIVO)

# Por POSICIÓN (.iloc): usa enteros 0-indexados (como NumPy, Día 7)
print(df.iloc[0, 1])  # 0.9  (fila 0, columna 1)
print(df.iloc[0:2])  # filas 0 y 1 (EXCLUSIVO del extremo)

# Columnas y filtrado booleano
print(df["obj"])  # la columna 'obj' (Series)
fiables = df[df["conf"] >= 0.9]  # FILTRA filas donde conf >= 0.9 (booleano)
print(fiables["obj"].tolist())  # ['persona', 'bici']
