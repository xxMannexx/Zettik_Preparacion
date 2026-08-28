import pytest

from lab.code_con_D import area_rectangulo

def test_area_basica():                          # una prueba: nombre empieza por test_
    assert area_rectangulo(4,5) == 20    # una prueba: nombre empieza por test_

def test_area_cero():
    assert area_rectangulo(0,5) == 0

@pytest.mark.parametrize("ancho,alto,esperado",[      # parametrización: varios casos con resultado esperado
    (2,3,6),
    (10,10,100),
    (1.5,2,3.0)
])

def test_area_varios(ancho,alto,esperado):  ## Comprueba si los resultados esperados se dan segun los casos de la parametrizacion
    assert area_rectangulo(ancho,alto) == esperado

def test_area_negativa_lanza():
    with pytest.raises(ValueError):          # verificar que se lanza la excepción puesta justo para esta accion(Día 4)
        area_rectangulo(-1,5)

@pytest.fixture
def rectangulo_estandar():
    return (4,5)                    # fixture: prepara datos para las pruebas

def test_con_fixture(rectangulo_estandar):
    ancho, alto = rectangulo_estandar
    assert area_rectangulo(ancho, alto) == 20


