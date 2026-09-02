# import os
# import src.EDA_Zettik.limpieza as limpieza
# import src.EDA_Zettik.carga as cargar
# from EDA_Zettik import analisis
# import EDA_Zettik.visualizacion as visualizacion
# from EDA_Zettik.analisis import Hallazgos
#
# columnas_esperadas = {
#     "objeto" : str,
#     "confianza" : float,
#     "fotograma" : int} ## Se definen que columnas que se esperan, cambiar a necesidad
#
# # 1. Obtiene la ruta absoluta de la carpeta donde vive 'carga.py' (src/EDA_Zettik/)
#
# CARGA_DIR = os.path.dirname(os.path.abspath(__file__))
#
# # 2. Construye la ruta apuntando a la carpeta 'data' que está a su lado
# ruta_csv = os.path.join(CARGA_DIR, 'data', '11_valido_grande_100k.csv')
#
# df = cargar.cargar(ruta_csv, columnas_esperadas)
#
# df = limpieza.limpieza(df)
# print("Filas finales:", len(df))                                      # Tamaño final del dataset limpio
# print("Duplicados:", df.duplicated().sum())                           # Debe ser 0
# print("NaN objeto:", df["objeto"].isna().sum())                       # Debe ser 0
# print("NaN confianza:", df["confianza"].isna().sum())                 # Debe ser 0
# print("NaN fotograma:", df["fotograma"].isna().sum())                 # Debe ser 0
#
# print("Confianza mínima:", df["confianza"].min())                      # Debe ser >= 0
# print("Confianza máxima:", df["confianza"].max())                      # Debe ser <= 1
#
# print("dtype objeto:", df["objeto"].dtype)                             # Debe ser textual
# print("dtype confianza:", df["confianza"].dtype)                       # Debe ser float
# print("dtype fotograma:", df["fotograma"].dtype)                       # Debe ser entero
#
# hallazgos = analisis.analisis(df)          # Ejecuta el análisis sobre el dataset limpio
# print("Datos:", hallazgos.n_datos)                                      # Total de detecciones analizadas
#
# print("\nDistribución de confianza:")                                   # Encabezado de descriptivas
# print(hallazgos.distribucion_confianza)                                 # count, mean, std, percentiles, min y max
#
# print("\nDetecciones por clase:")                                       # Encabezado del conteo categórico
# print(hallazgos.detecciones_por_clase)                                  # Número de detecciones por objeto
#
# print("\nClase predominante:")                                          # Encabezado de la clase más frecuente
# print(hallazgos.clase_predominante)                                     # Clase con mayor número de observaciones
#
# print("\nConfianza por clase:")                                         # Encabezado del groupby
# print(hallazgos.confianza_por_clase)                                    # count, mean, min, max y std por clase
#
# print("\nCorrelaciones:")                                               # Encabezado de relaciones numéricas
# print(hallazgos.correlaciones)                                          # Matriz de correlación como diccionario
#
# ruta = visualizacion.visualizar(df,"salidas")                    # Para verificar existencia y tamaño
# print(ruta)                            # Muestra la ruta devuelta por visualizar
# print(os.path.exists(ruta))            # True si el archivo existe
# print(os.path.getsize(ruta) / 1024)    # Tamaño en KB
#
# def generar_informe(hallazgos: Hallazgos, ruta_fig: str) -> str:
#     lineas = [                                                              # Acumula cada línea del informe Markdown
#         "# Informe EDA — VizionarIA",                                       # Título principal del informe
#         "",                                                                 # Línea en blanco
#         "## Resumen del dataset",                                           # Sección de resumen general
#         f"- Detecciones analizadas: {hallazgos.n_datos}",                  # Número total de filas limpias
#         f"- Clase predominante: {hallazgos.clase_predominante}",            # Clase con mayor frecuencia
#         "",                                                                 # Línea en blanco
#         "## Distribución de clases",                                        # Sección de conteos por clase
#     ]
#
#     for clase, cantidad in hallazgos.detecciones_por_clase.items():          # Recorre cada clase y su número de detecciones
#         lineas.append(f"- {clase}: {cantidad}")                              # Añade una línea por clase
#
#     lineas.extend([                                                          # Añade varias líneas nuevas al informe
#         "",                                                                  # Línea en blanco
#         "## Distribución global de confianza",                               # Sección de descriptivas
#         f"- Media: {hallazgos.distribucion_confianza['mean']:.4f}",          # Media global de confianza
#         f"- Mediana: {hallazgos.distribucion_confianza['50%']:.4f}",         # Percentil 50 = mediana
#         f"- Q1: {hallazgos.distribucion_confianza['25%']:.4f}",              # Primer cuartil
#         f"- Q3: {hallazgos.distribucion_confianza['75%']:.4f}",              # Tercer cuartil
#         f"- Desviación estándar: {hallazgos.distribucion_confianza['std']:.4f}",  # Dispersión global
#         "",                                                                  # Línea en blanco
#         "## Confianza por clase",                                            # Sección de resultados del groupby
#     ])
#
#     for clase, media in hallazgos.confianza_por_clase["mean"].items():       # Recorre la confianza media de cada clase
#         lineas.append(f"- {clase}: {media:.4f}")                             # Añade la media de esa clase
#
#     correlacion = hallazgos.correlaciones["confianza"]["fotograma"]          # Extrae correlación confianza-fotograma
#
#     lineas.extend([                                                          # Añade análisis final
#         "",                                                                  # Línea en blanco
#         "## Relación temporal",                                              # Sección sobre fotogramas
#         f"- Correlación confianza-fotograma: {correlacion:.4f}",             # Valor numérico de correlación
#         "- No se observa una relación lineal relevante entre fotograma y confianza.",  # Interpretación respaldada por el EDA
#         "",                                                                  # Línea en blanco
#         "## Panel EDA",                                                      # Sección de figura
#         f"![Panel EDA]({ruta_fig})",                                         # Inserta referencia Markdown al PNG
#         "",                                                                  # Línea en blanco
#         "## Conclusiones",                                                   # Cierre del informe
#         f"- La clase predominante es {hallazgos.clase_predominante}.",       # Resume desbalance principal
#         "- Las medias de confianza por clase son muy similares entre sí.",   # Resume comportamiento por clase
#         "- La distribución de confianza presenta una dispersión moderada.",  # Resume descriptivas
#         "- No se observa una tendencia lineal clara con el avance de los fotogramas.",  # Resume correlación
#     ])
#
#     return "\n".join(lineas)      # Convierte la lista en un único string Markdown
#

import logging                                                       # Sistema de logging del pipeline
import os                                                            # Manejo de rutas y carpetas
import numpy as np                                                   # Semilla fija para reproducibilidad

from . import limpieza as limpieza
from . import carga as cargar
from . import analisis
from . import visualizacion as visualizacion
from .analisis import Hallazgos


logger = logging.getLogger(__name__)                                 # Logger propio del módulo


columnas_esperadas = {                                               # Contrato mínimo del dataset
    "objeto": str,                                                   # Clase detectada
    "confianza": float,                                              # Confianza de detección
    "fotograma": int                                                 # Número de fotograma
}


def generar_informe(hallazgos: Hallazgos, ruta_fig: str) -> str:     # Convierte Hallazgos en Markdown
    lineas = [                                                       # Acumula las líneas del informe
        "# Informe EDA — VizionarIA",                                # Título principal
        "",                                                          # Separador Markdown
        "## Resumen del dataset",                                    # Primera sección
        f"- Detecciones analizadas: {hallazgos.n_datos}",            # Total de registros analizados
        f"- Clase predominante: {hallazgos.clase_predominante}",     # Clase más frecuente
        "",                                                          # Separador
        "## Distribución de clases",                                 # Sección de conteos
    ]

    for clase, cantidad in hallazgos.detecciones_por_clase.items():  # Recorre los conteos por clase
        lineas.append(f"- {clase}: {cantidad}")                      # Añade cada conteo al informe

    lineas.extend([                                                   # Añade descriptivas globales
        "",
        "## Distribución global de confianza",
        f"- Media: {hallazgos.distribucion_confianza['mean']:.4f}",
        f"- Mediana: {hallazgos.distribucion_confianza['50%']:.4f}",
        f"- Q1: {hallazgos.distribucion_confianza['25%']:.4f}",
        f"- Q3: {hallazgos.distribucion_confianza['75%']:.4f}",
        f"- Desviación estándar: {hallazgos.distribucion_confianza['std']:.4f}",
        "",
        "## Confianza por clase",
    ])

    for clase, media in hallazgos.confianza_por_clase["mean"].items():  # Recorre medias por clase
        lineas.append(f"- {clase}: {media:.4f}")                        # Añade cada media

    correlacion = hallazgos.correlaciones["confianza"]["fotograma"]    # Extrae correlación relevante

    lineas.extend([                                                     # Añade interpretación final
        "",
        "## Relación temporal",
        f"- Correlación confianza-fotograma: {correlacion:.4f}",
        "- No se observa una relación lineal relevante entre fotograma y confianza.",
        "",
        "## Panel EDA",
        f"![Panel EDA]({ruta_fig})",                                   # Referencia relativa al PNG
        "",
        "## Conclusiones",
        f"- La clase predominante es {hallazgos.clase_predominante}.",
        "- Las medias de confianza por clase son muy similares entre sí.",
        "- La distribución de confianza presenta una dispersión moderada.",
        "- No se observa una tendencia lineal clara con el avance de los fotogramas.",
    ])

    return "\n".join(lineas)                                           # Devuelve un único string Markdown


def ejecutar_pipeline(ruta_csv: str, ruta_salida: str) -> Hallazgos:   # Orquesta todas las fases del EDA
    np.random.seed(42)                                                 # Fija semilla para reproducibilidad
    os.makedirs(ruta_salida, exist_ok=True)                            # Garantiza que exista la carpeta de salida

    logger.info("=== Inicio del pipeline EDA ===")                     # Marca inicio de ejecución

    dataframe = cargar.cargar(                                        # Ejecuta Fase 1
        ruta_csv,                                                      # Ruta del dataset
        columnas_esperadas                                             # Contrato de columnas
    )

    dataframe = limpieza.limpieza(dataframe)                           # Ejecuta Fase 2

    hallazgos = analisis.analisis(dataframe)                           # Ejecuta Fase 3

    ruta_figura = visualizacion.visualizar(                            # Ejecuta Fase 4
        dataframe,                                                     # Dataset limpio
        ruta_salida                                                    # Carpeta donde guardar el panel
    )

    nombre_figura = os.path.basename(ruta_figura)                      # Obtiene solo "panel_eda.png"

    informe = generar_informe(                                        # Ejecuta Fase 5
        hallazgos,                                                     # Resultados estructurados
        nombre_figura                                                  # Ruta relativa desde el Markdown
    )

    ruta_informe = os.path.join(                                      # Construye ruta final del informe
        ruta_salida,
        "informe_eda.md"
    )

    with open(ruta_informe, "w", encoding="utf-8") as archivo:         # Abre archivo con cierre automático
        archivo.write(informe)                                        # Escribe el Markdown generado

    logger.info(f"Panel generado en: {ruta_figura}")                   # Registra artefacto visual
    logger.info(f"Informe generado en: {ruta_informe}")                # Registra informe
    logger.info("=== Pipeline EDA completado ===")                     # Marca final correcto

    return hallazgos                                                   # Devuelve resultados al llamador