import numpy as np
import pandas as pd

detecciones = pd.DataFrame({
    "Objeto" : ["Persona","Coche","Persona","Bici","Perro","Coche"],
    "Confianza" : [0.92,np.nan,0.84,0.76,0.88,0.91],
    "Fotograma" : [1,2,3,4,5,6]
})

metadatos = pd.DataFrame({
    "Objeto" : ["Persona","Coche","Bici"],
    "Categoria" : ["Humano","Vehiculo","Vehiculo"]
})

print(f"\nEvaluacion de datos faltantes en ambos dataframes:\n{detecciones.isna()}\n{metadatos.isna()}\n")

detecciones["Confianza"] = detecciones["Confianza"].fillna(detecciones["Confianza"].mean())

print(f"\nFiltrado de detecciones con confianza >= 0.8:\n"
      f"{detecciones[detecciones["Confianza"] >= 0.8]}")

print(f"\nMetricas de detecciones con grupby:\n"
      f"{(detecciones.groupby("Objeto")["Confianza"].agg([
          'count',
          'mean',
          'max'
      ]))}")

combinados = pd.merge(detecciones, metadatos, on="Objeto", how="left")

print(f"\n{combinados.groupby("Categoria")["Confianza"].mean()}")

print(f"\n{combinados["Confianza"].isna().any()}")

