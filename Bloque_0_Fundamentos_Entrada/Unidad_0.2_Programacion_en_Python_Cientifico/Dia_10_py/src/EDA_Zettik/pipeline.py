import os
import src.EDA_Zettik.limpieza as limpieza
import src.EDA_Zettik.carga as cargar
from EDA_Zettik import analisis

columnas_esperadas = {
    "objeto" : str,
    "confianza" : float,
    "fotograma" : int} ## Se definen que columnas que se esperan, cambiar a necesidad

# 1. Obtiene la ruta absoluta de la carpeta donde vive 'carga.py' (src/EDA_Zettik/)

CARGA_DIR = os.path.dirname(os.path.abspath(__file__))

# 2. Construye la ruta apuntando a la carpeta 'data' que está a su lado
ruta_csv = os.path.join(CARGA_DIR, 'data', 'ataque_limpieza_122k.csv')

df = cargar.cargar(ruta_csv, columnas_esperadas)

df = limpieza.limpieza(df)
print("Filas finales:", len(df))                                      # Tamaño final del dataset limpio
print("Duplicados:", df.duplicated().sum())                           # Debe ser 0
print("NaN objeto:", df["objeto"].isna().sum())                       # Debe ser 0
print("NaN confianza:", df["confianza"].isna().sum())                 # Debe ser 0
print("NaN fotograma:", df["fotograma"].isna().sum())                 # Debe ser 0

print("Confianza mínima:", df["confianza"].min())                      # Debe ser >= 0
print("Confianza máxima:", df["confianza"].max())                      # Debe ser <= 1

print("dtype objeto:", df["objeto"].dtype)                             # Debe ser textual
print("dtype confianza:", df["confianza"].dtype)                       # Debe ser float
print("dtype fotograma:", df["fotograma"].dtype)                       # Debe ser entero

hallazgos = analisis.analisis(df)          # Ejecuta el análisis sobre el dataset limpio
print("Datos:", hallazgos.n_datos)                                      # Total de detecciones analizadas

print("\nDistribución de confianza:")                                   # Encabezado de descriptivas
print(hallazgos.distribucion_confianza)                                 # count, mean, std, percentiles, min y max

print("\nDetecciones por clase:")                                       # Encabezado del conteo categórico
print(hallazgos.detecciones_por_clase)                                  # Número de detecciones por objeto

print("\nClase predominante:")                                          # Encabezado de la clase más frecuente
print(hallazgos.clase_predominante)                                     # Clase con mayor número de observaciones

print("\nConfianza por clase:")                                         # Encabezado del groupby
print(hallazgos.confianza_por_clase)                                    # count, mean, min, max y std por clase

print("\nCorrelaciones:")                                               # Encabezado de relaciones numéricas
print(hallazgos.correlaciones)                                          # Matriz de correlación como diccionario