import pytest
from pipeline_vixia.pipeline import  construir_indices,limite_izquierdo,seleccionar_por_umbral
from pipeline_vixia.pipeline import (
    Deteccion,
    IndiceTemporal,
    construir_grafo_proximidad,
    objetos_proximos,
    grupos_de_objetos,
)
from pipeline_vixia.pipeline import ejecutar_pipeline
from pipeline_vixia.dataset_demo import generar_dataset_demo

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
    assert [d.id for d in result] == ["a", "c"]

    result2 = seleccionar_por_umbral(detecciones,umbral=1)
    assert result2 == []

    result3 = seleccionar_por_umbral(detecciones,umbral=0)
    assert set(result3) == set(detecciones)

def test_indice_temporal():
    detecciones = [
        Deteccion("a", "persona", 0.90, 0, 0, 100),
        Deteccion("b", "coche",   0.80, 0, 0, 80),
        Deteccion("c", "persona", 0.70, 0, 0, 120),
        Deteccion("d", "bici",    0.60, 0, 0, 90),
    ]

    indice = IndiceTemporal()

    for d in detecciones:
        indice.insertar(d)

    cronologia = indice.cronologico()

    assert [d.timestamp for d in cronologia] == [80, 90, 100, 120]
    assert indice.mas_reciente().id == "c"
    assert indice.buscar_timestamp(90).id == "d"
    assert indice.buscar_timestamp(999) is None

def test_grafo_proximidad():
    detecciones = [
        Deteccion("a", "persona", 0.9, 0,   0,   100),
        Deteccion("b", "persona", 0.8, 3,   4,   101),
        Deteccion("c", "persona", 0.7, 100, 100, 102),
    ]

    grafo = construir_grafo_proximidad(
        detecciones,
        umbral_dist=6
    )

    assert grafo == {
        "a": ["b"],
        "b": ["a"],
        "c": []
    }

def test_bfs_objetos_proximos():
    grafo = {
        "a": ["b"],
        "b": ["a", "c"],
        "c": ["b", "d"],
        "d": ["c"]
    }

    resultado = objetos_proximos(
        grafo,
        inicio="a",
        max_saltos=2
    )

    assert resultado == {
        "a": 0,
        "b": 1,
        "c": 2
    }

    assert "d" not in resultado

def test_grupos_de_objetos():
    grafo = {
        "a": ["b"],
        "b": ["a"],
        "c": ["d"],
        "d": ["c"],
        "e": []
    }

    grupos = grupos_de_objetos(grafo)

    grupos_normalizados = sorted(
        [sorted(grupo) for grupo in grupos]
    )

    assert grupos_normalizados == [
        ["a", "b"],
        ["c", "d"],
        ["e"]
    ]

def test_pipeline_completo():
    detecciones = [
        Deteccion("a", "persona", 0.90, 0, 0, 100),
        Deteccion("b", "coche",   0.60, 3, 4, 80),
        Deteccion("c", "persona", 0.80, 100, 100, 120),
        Deteccion("a", "persona", 0.20, 500, 500, 999),
    ]

    resultado = ejecutar_pipeline(
        detecciones,
        umbral_confianza=0.70,
        umbral_dist=6,
        max_saltos=2
    )

    assert resultado["n_unicas"] == 3
    assert resultado["duplicados"] == 1

    assert [
        d.id for d in resultado["seleccionadas"]
    ] == ["a", "c"]

    assert [
        d.timestamp for d in resultado["cronologia"]
    ] == [80, 100, 120]

    assert resultado["mas_reciente"].id == "c"

    assert resultado["grafo"] == {
        "a": ["b"],
        "b": ["a"],
        "c": []
    }

    assert len(resultado["grupos"]) == 2


def test_robustez_limite_tamano():
    detecciones = [
        Deteccion(
            f"obj_{i}",
            "persona",
            0.8,
            float(i),
            0.0,
            i
        )
        for i in range(10)
    ]

    with pytest.raises(ValueError):
        ejecutar_pipeline(
            detecciones,
            umbral_confianza=0.5,
            umbral_dist=10,
            max_saltos=2,
            limite_n=5
        )


def test_pipeline_vacio():
    resultado = ejecutar_pipeline(
        [],
        umbral_confianza=0.5,
        umbral_dist=10,
        max_saltos=2
    )

    assert resultado["n_unicas"] == 0
    assert resultado["cronologia"] == []
    assert resultado["mas_reciente"] is None
    assert resultado["grupos"] == []
    assert resultado["proximos_al_primero"] == {}

def test_dataset_reproducible():
    d1 = generar_dataset_demo(20, seed=42)
    d2 = generar_dataset_demo(20, seed=42)

    assert d1 == d2