import pandas as pd
import numpy as np
import logging
from . import carga
import src.EDA_Zettik.Excepciones.excepciones as excepcion


logger = logging.getLogger(__name__)

def limpieza(df : pd.DataFrame) -> pd.DataFrame:

    size = len(df)
    ##Cargamos el dataset y eliminamos tanto duplicados y los datos faltantes de las columnas necesarias
    dataframe = (df.copy().drop_duplicates())
    size_com = len(dataframe)
    logger.info(f"Se eliminaron {size - size_com} elementos duplicados")
    dataframe = dataframe.dropna(subset=['objeto','fotograma'])
    logger.info(f"Se eliminaron {size_com - len(dataframe)} elementos faltantes")

    ##Cambiar datos a los tipos esperados
    try:
        for columna in carga.columnas().keys():
            logger.info(f"Convirtiendo tipos a los esperados de {columna}")
            tipo = carga.columnas()[columna]
            dataframe[columna] = dataframe[columna].astype(tipo)
    except (ValueError, TypeError, OverflowError) as e:
        logger.error("Error al cargar datos para cargar, los tipos no son compatibles")
        raise excepcion.ErrorCargaDataset("Los tipos no son compatibles con los esperados para poder procesar") from e

    ## Rellenamos la confianza en datos faltantes con la mediana para asegurar un valor uniforme
    if not dataframe['confianza'].isna().all():
        conteo_faltantes = dataframe['confianza'].isna().sum()
        mediana_conf = dataframe['confianza'].median()
        dataframe['confianza'] = dataframe['confianza'].fillna(mediana_conf)
        logger.info(f"Se rellenaron {conteo_faltantes} elementos")
    else:
        raise excepcion.ErrorFaltantes('Todos los elementos de esta columna estan vacios')


    ##Eliminamos datos atipicos en confianza
    valores_bajos = (dataframe['confianza'] < 0).sum()
    valores_altos = (dataframe['confianza'] > 1).sum()
    total_cambios = valores_bajos + valores_altos
    dataframe['confianza'] = np.clip(dataframe['confianza'], 0, 1)
    logger.info(f"Se afectaron {total_cambios} elementos")

    size_final = len(dataframe)  # Guarda cuántas filas existen antes del último control
    dataframe = dataframe.drop_duplicates()  # Elimina duplicados creados tras astype/fillna/clip
    logger.info(
        f"Se eliminaron {size_final - len(dataframe)} duplicados finales"
    )  # Registra el efecto de esta última limpieza

    return dataframe  # Devuelve el DataFrame ya canónico