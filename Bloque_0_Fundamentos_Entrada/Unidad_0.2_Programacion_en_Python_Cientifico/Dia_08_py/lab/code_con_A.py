import pandas as pd, numpy as np

## Series: array + indice
confianzas = pd.Series([0.9,0.7,0.95], index=["Deteccion_1","Deteccion_2","Deteccion_3"], name="confianza")
print(confianzas)
print(confianzas.values, confianzas.index.tolist(), confianzas.dtype)

## Datframe: columnas heterogeneas con indice comun

# DataFrame: columnas heterogéneas con índice común
detecciones = pd.DataFrame({
    "objeto":    ["persona", "coche", "bici"],    # dtype: object (texto)
    "confianza": [0.9, 0.7, 0.95],                # dtype: float64
    "fotograma": [10, 10, 11],                    # dtype: int64
})
print(detecciones)
print(detecciones.dtypes)      # cada columna su propio dtype
print(detecciones.shape)       # (3, 3)
print(detecciones.describe())  # estadísticas de las columnas numéricas


##Datframe de la Series
import pandas as pd

# 1. Creamos las series CON el atributo 'name' definido
serie_conf = pd.Series([0.9, 0.7, 0.95], index=["det1", "det2", "det3"], name="confianza")
serie_clase = pd.Series(["persona", "auto", "persona"], index=["det1", "det2", "det3"], name="clase")

# 2. Creamos el DataFrame pasando las series en una lista
# Usamos .T (Transponer) porque por defecto las mete como filas, con .T las volvemos columnas
df = pd.DataFrame([serie_conf, serie_clase]).T
print(df)

