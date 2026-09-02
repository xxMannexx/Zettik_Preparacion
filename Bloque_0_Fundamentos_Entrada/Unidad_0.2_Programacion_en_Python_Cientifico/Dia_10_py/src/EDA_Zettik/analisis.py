import pandas as pd
from dataclasses import dataclass

@dataclass
class Hallazgos:
    n_datos: int  # Número de filas limpias analizadas
    distribucion_confianza: dict  # describe() de la confianza
    detecciones_por_clase: dict  # Conteo de objetos por clase
    confianza_por_clase: dict  # Métricas de confianza obtenidas con groupby
    correlaciones: dict         # Relaciones entre variables numéricas
    clase_predominante: str  # Clase con mayor número de detecciones

def analisis(dataframe: pd.DataFrame) -> Hallazgos:
    # Número de filas limpias analizadas

    datos = len(dataframe)

    # describe() de la confianza
    distribucion_confianza = dataframe['confianza'].describe().to_dict()

    # Conteo de objetos por clase
    detecciones_por_clase = dataframe['objeto'].value_counts().to_dict()

    # Métricas de confianza obtenidas con groupby
    confianza_por_clase = dataframe.groupby('objeto')['confianza'].agg([
    "count",                              # Número de detecciones
    "mean",                               # Confianza media
    "min",                                # Confianza mínima
    "max",                                # Confianza máxima
    "std"                                 # Dispersión de confianza
    ]).to_dict()

    # Relaciones entre variables numéricas
    correlaciones = dataframe[["confianza", "fotograma"]].corr().to_dict()

    # Clase con mayor número de detecciones
    valor = max(detecciones_por_clase,key=detecciones_por_clase.get)

    clase_predominante = valor

    hallazgos = Hallazgos(n_datos=datos,distribucion_confianza=distribucion_confianza,detecciones_por_clase=detecciones_por_clase,confianza_por_clase=confianza_por_clase,correlaciones=correlaciones,clase_predominante=clase_predominante)

    return hallazgos

