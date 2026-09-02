import pandas as pd
from dataclasses import dataclass

@dataclass
class Hallazgos:
    n_datos: int  # Número de filas limpias analizadas
    distribucion_confianza: dict[str, float]  # describe() de la confianza
    detecciones_por_clase: dict[str, int]  # Conteo de objetos por clase
    confianza_por_clase: dict[str, dict[str, float]]  # Métricas de confianza obtenidas con groupby
    correlaciones: dict[str, dict[str, float]]         # Relaciones entre variables numéricas
    clase_predominante: str  # Clase con mayor número de detecciones

def analisis(dataframe: pd.DataFrame) -> Hallazgos:   # DataFrame limpio -> Hallazgos tipados

    datos = len(dataframe)                            # Cuenta las filas analizadas

    distribucion_raw = (                             # Obtiene descriptivas desde Pandas
        dataframe["confianza"]
        .describe()
        .to_dict()
    )

    distribucion_confianza: dict[str, float] = {     # Convierte Hashable/Any al contrato esperado
        str(clave): float(valor)                     # Fuerza clave textual y valor flotante
        for clave, valor in distribucion_raw.items()
    }

    detecciones_raw = (                              # Obtiene conteos por clase
        dataframe["objeto"]
        .value_counts()
        .to_dict()
    )

    detecciones_por_clase: dict[str, int] = {        # Explicita clase -> cantidad
        str(clase): int(cantidad)                    # Normaliza los tipos devueltos por Pandas
        for clase, cantidad in detecciones_raw.items()
    }

    confianza_raw = (                                # Calcula métricas por clase
        dataframe
        .groupby("objeto")["confianza"]
        .agg(["count", "mean", "min", "max", "std"])
        .to_dict()
    )

    confianza_por_clase: dict[str, dict[str, float]] = {  # Explicita estructura anidada
        str(metrica): {                                   # Nombre de la métrica
            str(clase): float(valor)                      # Clase -> valor estadístico
            for clase, valor in valores.items()
        }
        for metrica, valores in confianza_raw.items()
    }

    correlaciones_raw = (                           # Calcula matriz de correlaciones
        dataframe[["confianza", "fotograma"]]
        .corr()
        .to_dict()
    )

    correlaciones: dict[str, dict[str, float]] = {  # Explicita variable -> variable -> valor
        str(variable): {                            # Variable exterior
            str(otra): float(valor)                 # Variable relacionada -> correlación
            for otra, valor in valores.items()
        }
        for variable, valores in correlaciones_raw.items()
    }

    clase_predominante = max(                       # Obtiene la clase con mayor frecuencia
        detecciones_por_clase,                      # Ahora mypy sabe que las claves son str
        key=lambda clase: detecciones_por_clase[clase]  # Compara mediante su conteo entero
    )

    return Hallazgos(                               # Construye el resultado completamente tipado
        n_datos=datos,
        distribucion_confianza=distribucion_confianza,
        detecciones_por_clase=detecciones_por_clase,
        confianza_por_clase=confianza_por_clase,
        correlaciones=correlaciones,
        clase_predominante=clase_predominante,
    )

