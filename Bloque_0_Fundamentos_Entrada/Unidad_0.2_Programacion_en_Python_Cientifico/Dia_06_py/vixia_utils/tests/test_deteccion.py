import pytest

from vixia_utils.deteccion import (
    Deteccion,
    confianza_media,
    filtrar_por_confianza,
)


@pytest.fixture
def detecciones() -> list[Deteccion]:
    return [
        Deteccion("persona", 0.90),
        Deteccion("coche", 0.50),
        Deteccion("bicicleta", 0.70),
    ]


@pytest.mark.parametrize(
    ("umbral", "esperado"),
    [
        (0.0, 3),
        (0.6, 2),
        (0.95, 0),
    ],
)
def test_filtrar_varios_umbrales(
    detecciones: list[Deteccion],
    umbral: float,
    esperado: int,
) -> None:
    assert len(filtrar_por_confianza(detecciones, umbral)) == esperado


def test_confianza_media(detecciones: list[Deteccion]) -> None:
    assert confianza_media(detecciones) == pytest.approx(0.70)


def test_umbral_invalido_lanza(detecciones: list[Deteccion]) -> None:
    with pytest.raises(ValueError):
        filtrar_por_confianza(detecciones, 1.5)


def test_deteccion_invalida_lanza() -> None:
    with pytest.raises(ValueError):
        Deteccion("persona", 1.2)
