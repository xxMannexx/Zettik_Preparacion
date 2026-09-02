import pandas as pd
import pytest
import EDA_Zettik.analisis as analisis




# 1. devuelve realmente una instancia Hallazgos
def test_analisis_instancia():
    dataframe = pd.DataFrame({
        "objeto": ["A", "D", "C", ],
        "fotograma": [1, 2, 3],
        "confianza": [0.1, 0.2, 0.3]
    })
    result = analisis.analisis(dataframe)

    assert isinstance(result,analisis.Hallazgos)

# 2. n_datos coincide con el número de filas
def test_numero_datos():
    dataframe = pd.DataFrame({
        "objeto": ["A", "D", "C"],
        "fotograma": [1, 2, 3],
        "confianza": [0.1, 0.2, 0.3]
    })
    result = analisis.analisis(dataframe)
    assert result.n_datos == len(dataframe)

# 3. detecta correctamente la clase predominante
def test_clase_predominante():
    dataframe = pd.DataFrame({
        "objeto": ["A", "D", "A"],
        "fotograma": [1, 2, 3],
        "confianza": [0.1, 0.2, 0.3]
    })

    result = analisis.analisis(dataframe)
    assert  result.clase_predominante == 'A'

# 4. detecciones_por_clase tiene los conteos correctos
def test_conteo_correcto():
    dataframe = pd.DataFrame({
        "objeto": ["A", "D", "C"],
        "fotograma": [1, 2, 3],
        "confianza": [0.1, 0.2, 0.3]
    })



    result = analisis.analisis(dataframe)

    assert result.detecciones_por_clase == {
        "A": 1,
        "D": 1,
        "C": 1
    }

# 5. confianza_por_clase calcula correctamente una media conocida
def test_media_conocida_confianza():
    dataframe = pd.DataFrame({
        "objeto": ["A", "A", "B"],
        "fotograma": [1, 2, 3],
        "confianza": [0.6, 0.8, 0.5]
    })

    result = analisis.analisis(dataframe)
    assert result.confianza_por_clase["mean"]["A"] == pytest.approx(0.7)
    assert result.confianza_por_clase["mean"]["B"] == pytest.approx(0.5)


# 6. correlaciones contiene confianza y fotograma
def test_hallazgos_correlaciones_contiene_variables_esperadas():
    # 1. Creamos un DataFrame controlado para la prueba
    df_prueba = pd.DataFrame({
        'objeto': ['A', 'C', 'B'],
        'fotograma':[1,4,5],
        'confianza': [0.9, 0.6, 0.8]
    })

    # 2. Ejecutamos la función para obtener la instancia de la dataclass
    resultado = analisis.analisis(df_prueba)

    # 3. Validamos que el retorno sea la instancia correcta
    assert isinstance(resultado, analisis.Hallazgos), "El resultado no es una instancia de la dataclass Hallazgos"

    # 4. Validamos que el diccionario 'correlaciones' tenga las llaves principales esperadas
    assert 'confianza' in resultado.correlaciones, "Falta la llave 'confianza' en las correlaciones"
    assert 'fotograma' in resultado.correlaciones, "Falta la llave 'fotograma' en las correlaciones"

# 7. distribucion_confianza contiene una media conocida
def test_distribucion_confianza_media():
    dataframe = pd.DataFrame({                         # Dataset con media fácil de calcular mentalmente
        "objeto": ["A", "B", "C"],                    # Clases arbitrarias
        "fotograma": [1, 2, 3],                       # Fotogramas válidos
        "confianza": [0.2, 0.4, 0.6]                  # Media conocida = 0.4
    })

    resultado = analisis.analisis(dataframe)           # Ejecuta la fase de análisis

    assert resultado.distribucion_confianza["mean"] == pytest.approx(0.4)  # Verifica el oráculo conocido