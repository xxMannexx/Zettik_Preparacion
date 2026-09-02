
import EDA_Zettik.Excepciones.excepciones as excepciones
import numpy as np
import pandas as pd
import pytest
import EDA_Zettik.limpieza as limpieza


# 1. elimina duplicados
def test_elimina_duplicados():
    df_con_duplicados = pd.DataFrame({
        'objeto': ['A', 'A', 'B'],
        'fotograma': [2,2,4],
        'confianza': [0.5, 0.5, 0.8]
    })

    resultado = limpieza.limpieza(df_con_duplicados)
    assert len(resultado) == 2
# 2. elimina filas con objeto/fotograma faltante
def test_elimina_faltantes():
    df_con_faltantes = pd.DataFrame({
        'objeto': ['A', 'A', np.nan],
        'fotograma': [2,np.nan,4],
        'confianza': [0.5,0.6,0.8]
    })

    resultado = limpieza.limpieza(df_con_faltantes)
    assert len(resultado) == 1
# 3. imputa confianza NaN con la mediana
def test_modificar_faltantes():
    df_con_faltantes = pd.DataFrame({
        'objeto': ['A', 'A', 'A'],
        'fotograma': [2,2,4],
        'confianza': [0.5,0.6,np.nan]
    })



    # 3. Ejecutamos tu función de limpieza
    resultado = limpieza.limpieza(df_con_faltantes)
    mediana_esperada = resultado['confianza'].median()


    # 4. PRUEBA EXACTA:
    # Verificamos que la celda modificada (índice 1) tenga el valor de la mediana calculada
    valor_imputado = resultado.loc[2, 'confianza']

    assert valor_imputado == mediana_esperada
    resultado_relleno = resultado['confianza'].isna().any()

    assert resultado_relleno == False

# 4. recorta confianza al rango [0, 1]
def test_recorta_confianza():
    df_con_confianza = pd.DataFrame({
        'objeto': ['A', 'A', 'A'],
        'fotograma': [2,2,4],
        'confianza': [-0.1,0.6,1.2]
    })
    resultado = limpieza.limpieza(df_con_confianza)
    valores_no_recortados = ((resultado['confianza'] < 0).sum()) + (resultado['confianza'] > 1).sum()
    assert valores_no_recortados == 0


# 5. NO modifica el DataFrame original
def test_no_modificacion():
    df_original = pd.DataFrame({
        'objeto': ['A', 'C', 'B'],
        'fotograma': [2,2,4],
        'confianza': [0.9,0.6,2]
    })
    copia = df_original.copy()
    resultado =limpieza.limpieza(df_original)
    assert df_original.compare(copia).empty

#6. si toda confianza es NaN -> ErrorFaltantes
def test_nan_excepcion():
    df_original = pd.DataFrame({
        'objeto': ['A', 'C', 'B'],
        'fotograma': [2,2,4],
        'confianza': [np.nan,np.nan,np.nan]
    })

    with pytest.raises(excepciones.ErrorFaltantes):
        resultado = limpieza.limpieza(df_original)

##7. Conversión de tipos
def test_conversion():                                                        # Verifica los tipos finales producidos por limpieza
    df_original = pd.DataFrame({                                              # Construye datos deliberadamente convertibles
        'objeto': ['A', 'C', 'B'],                                            # Valores categóricos de texto
        'fotograma': [2, 1.0, "4"],                                           # Mezcla int, float entero y string numérico
        'confianza': [0.9, 3.0, "2"]                                         # Mezcla float y string numérico
    })

    resultado = limpieza.limpieza(df_original)                                # Ejecuta la conversión definitiva

    assert pd.api.types.is_string_dtype(resultado['objeto'].dtype)            # objeto debe terminar como texto
    assert pd.api.types.is_float_dtype(resultado['confianza'].dtype)          # confianza debe terminar como flotante
    assert pd.api.types.is_integer_dtype(resultado['fotograma'].dtype)        # fotograma debe terminar como entero


