## Modulo de visualizacion
import logging
import os
import matplotlib
matplotlib.use('Agg')
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

logger = logging.getLogger(__name__)

sns.set_theme(style="whitegrid")


def visualizar(dataframe_original: pd.DataFrame,ruta_salida: str) -> str:
    ##Verificamos ruta
    os.makedirs(ruta_salida, exist_ok=True)
    ruta = os.path.join(ruta_salida, "panel_eda.png")

    ##Creo el figure con 4 espacios
    fig, ax = plt.subplots(2,2,figsize=(14, 10))

    dataframe = dataframe_original.copy()

    ## Grafico de linea: Evolución/comportamiento de confianza por fotograma
    df_agrupado = (
        dataframe
        .groupby("fotograma")["confianza"]
        .mean()
        .sort_index()
        .reset_index()
    )

    # 2. (Opcional) Suavizar la serie ordenada usando una media móvil
    # 'window=15' promedia los 15 fotogramas vecinos; puedes ajustar este número.
    df_agrupado["confianza_suave"] = (
        df_agrupado["confianza"]
        .rolling(window=15, center=True, min_periods=1)
        .mean()
    )

    # 3. Plot en tu subgráfico ax[0,0]
    # Graficamos la línea suavizada
    sns.lineplot(
        data=df_agrupado,
        x="fotograma",
        y="confianza_suave",
        ax=ax[0, 0],
        linewidth=2,
        color="yellowgreen",
    )
    ax[0,0].set_title("Evolución/comportamiento de confianza por fotograma")
    ax[0,0].set_xlabel("Fotograma")
    ax[0,0].set_ylabel("Confianza ")

    ##boxplot:Distribución de confianza por clase
    sns.boxplot(data=dataframe, x="objeto", y="confianza", ax=ax[0,1], color="lime")
    ax[0,1].set_title("Confianza por clase")
    ax[0,1].set_xlabel("Clase")
    ax[0,1].set_ylabel("Confianza")

    ##barras: Cantidad de detecciones por clase
    sns.countplot(
        data=dataframe,
        x="objeto",
        ax=ax[1, 0],
        order=dataframe['objeto'].value_counts().index  # Ordena de mayor a menor detección

    )
    ax[1,0].set_title("Cantidad de detecciones por clase")
    ax[1,0].set_xlabel("Clase Objeto")
    ax[1,0].set_ylabel("Cantidad de detecciones")

    ##histograma:Distribución global de confianza
    dataframe["confianza"].plot(kind="hist", ax=ax[1,1], bins=20, color="coral", edgecolor="white")
    ax[1,1].set_title("Distribución de confianza")
    ax[1,1].set_xlabel("Confianza");
    ax[1,1].set_ylabel("Frecuencia")

    fig.suptitle("Análisis EDA", fontsize=12, fontweight="bold")
    fig.tight_layout()
    fig.savefig(ruta,dpi=150,bbox_inches='tight')
    plt.close(fig)

    logger.info(f"Figura creada en: {ruta}")
    return ruta