import pytest
from pipeline_vixia.pipeline import Deteccion, construir_indices,limite_izquierdo,seleccionar_por_umbral


def test_analisis_instancia():
    result = Deteccion("objeto_01", "persona", 0.28, 10.5, 20, 3)
    assert isinstance(result, Deteccion)

def test_deduplicacion():
    result1 = Deteccion("a", "persona",0.67, 10.52, 11, 9)
    result2 = Deteccion("a", "persona",0.12, 14.2, 13, 4)
    resultado=construir_indices([result1 ,result2])
    assert resultado["duplicados"]==1
    assert len(resultado["por_id"])==1

    assert  resultado["por_id"]["a"]==result1
    assert resultado["por_clase"]["persona"]==[result1]

def test_limite_izquierdo():
    confianzas = [0.20, 0.45, 0.61, 0.78, 0.93]
    assert limite_izquierdo(confianzas, umbral=0.61) == 2
    assert limite_izquierdo(confianzas, umbral=0.99) == 5
    assert limite_izquierdo(confianzas,umbral=0.61) == 2


def test_seleccion_umbral():
    detecciones = [
        Deteccion(
            id="a",
            clase="persona",
            confianza=0.90,
            x=10.5,
            y=20.0,
            timestamp=100
        ),
        Deteccion(
            id="b",
            clase="coche",
            confianza=0.4,
            x=15.2,
            y=22.4,
            timestamp=101
        ),
        Deteccion(
            id="c",
            clase="persona",
            confianza=0.75,
            x=8.0,
            y=19.3,
            timestamp=102
        )
    ]

    result = seleccionar_por_umbral(detecciones,umbral=0.7)
    assert [d.id for d in result] == ["c", "a"]

    result2 = seleccionar_por_umbral(detecciones,umbral=1)
    assert result2 == []

    result3 = seleccionar_por_umbral(detecciones,umbral=0)
    assert set(result3) == set(detecciones)