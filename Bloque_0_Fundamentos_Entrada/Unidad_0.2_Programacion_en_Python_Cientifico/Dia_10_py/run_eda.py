import logging                                                       # Configura el logging de toda la aplicación
import os                                                            # Construye rutas independientes del cwd

from src.EDA_Zettik.pipeline import ejecutar_pipeline                # Importa únicamente el orquestador


logging.basicConfig(                                                 # Configura formato global del log
    level=logging.INFO,                                              # Muestra eventos INFO o superiores
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"    # Formato consistente de cada registro
)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))                # Obtiene raíz de Dia_10_py

RUTA_CSV = os.path.join(                                             # Construye ruta del dataset
    BASE_DIR,
    "src",
    "EDA_Zettik",
    "data",
    "11_valido_grande_100k.csv"
)

RUTA_SALIDAS = os.path.join(                                         # Construye carpeta de artefactos
    BASE_DIR,
    "src",
    "EDA_Zettik",
    "salidas"
)


if __name__ == "__main__":
    hallazgos = ejecutar_pipeline(
        RUTA_CSV,
        RUTA_SALIDAS
    )

    print(
        f"Pipeline completo | "                                       
        f"filas={hallazgos.n_datos} | "                               
        f"clase predominante={hallazgos.clase_predominante}"
    )