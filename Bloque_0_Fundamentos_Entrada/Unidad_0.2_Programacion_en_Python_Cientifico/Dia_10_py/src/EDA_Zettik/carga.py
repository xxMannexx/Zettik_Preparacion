import pandas as pd
import os
import src.EDA_Zettik.Excepciones.excepciones as excepcion
from pandas.errors import EmptyDataError
import logging

## Configuramos el logger para el loggin
#logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def columnas():
    columnas_esperadas = {
    "objeto" : str,
    "confianza" : float,
    "fotograma" : int} ## Se definen que columnas que se esperan, cambiar a necesidad

    return columnas_esperadas

# 1. Obtiene la ruta absoluta de la carpeta donde vive 'carga.py' (src/EDA_Zettik/)

#CARGA_DIR = os.path.dirname(os.path.abspath(__file__))

# 2. Construye la ruta apuntando a la carpeta 'data' que está a su lado
#ruta_csv = os.path.join(CARGA_DIR, 'data', '03_valido_numeros_como_texto.csv')

columnas_esperadas = columnas()

def cargar(ruta_csv : str,columnas_esperadas : dict[str,type]) -> pd.DataFrame:
    try:
        logger.info(f"Cargando dataset... {ruta_csv}")
        # Intentamos cargar el dataset
        df = pd.read_csv(ruta_csv)

        ##Compruebo si esta vacio, en el caaso pasa con columnas vacias
        if df.empty:
            logger.error(f"No hay datos para cargar en {ruta_csv}")
            raise excepcion.ErrorCargaDataset("El dataset esta vacio, no es posible procesar")

    ## Excepciones mas importantes
    except FileNotFoundError as e:
        logger.error("El archivo no existe")
        raise excepcion.ErrorCargaDataset("Error al cargar el dataset. El archivo no se encontro") from e
    except EmptyDataError as e:
        logger.error("Error al cargar datos para cargar")
        raise excepcion.ErrorCargaDataset("No hay columnas para cargar y comvertir en dataframe") from e

    ## Columnas requeridas
    columnas_minimas = [col for col in columnas_esperadas.keys() if col not in df.columns.tolist()]
    if columnas_minimas:
        logger.error(f"No existen las columnas minimas para empezar: {columnas_minimas}")
        raise excepcion.ErrorCargaDataset(f"Faltan las siguientes columnas: {columnas_minimas}")

    ##Vemos si los tipos son compatibles

    for columna in columnas_esperadas.keys():
        logger.info(f"Observando tipos a los esperados de {columna}")

        if columna != "objeto":
            try:
                es_numero = pd.to_numeric(df[columna], errors='raise')
                validos = es_numero.dropna()
                if columna == "fotograma":
                    son_enteros = (validos % 1 == 0).all()
                    if son_enteros:
                        pass
                    else:
                        raise excepcion.ErrorCargaDataset("Error al cargar los datos de fotograma deben ser enteros"
                                                      "")
            except (ValueError, TypeError, OverflowError) as e:
                raise excepcion.ErrorCargaDataset("El tipo de datos no es compatible") from e

    logger.info("Dataset listo...")
    ## Returnamos el df correcto
    return df

#dataframe = cargar(ruta_csv, columnas_esperadas)
#print(dataframe)

