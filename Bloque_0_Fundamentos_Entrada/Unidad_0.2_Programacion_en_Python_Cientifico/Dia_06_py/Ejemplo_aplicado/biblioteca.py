
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass  # dataclass (Día 5) con anotaciones (hoy)
class Deteccion:
    objeto: str
    confianza: float


def filtrar_por_confianza(detecciones: list[Deteccion], umbral: float) -> list[Deteccion]:
    """Conserva las detecciones cuya confianza alcanza el umbral."""
    if not (0.0 <= umbral <= 1.0):
        raise ValueError(f"umbral fuera de [0, 1]: {umbral}")  # excepción (Día 4)
    resultado = [d for d in detecciones if d.confianza >= umbral]
    logger.info("filtradas %d de %d detecciones (umbral=%.2f)",
                len(resultado), len(detecciones), umbral)  # logging (hoy)
    return resultado


# tests/test_deteccion.py
import pytest
from vixia_utils.deteccion import Deteccion, filtrar_por_confianza


@pytest.fixture
def detecciones():  # fixture: datos de prueba
    return [Deteccion("persona", 0.9), Deteccion("coche", 0.5), Deteccion("bici", 0.7)]


def test_filtra_por_umbral(detecciones):
    resultado = filtrar_por_confianza(detecciones, 0.7)
    assert len(resultado) == 2  # persona (0.9) y bici (0.7)
    assert all(d.confianza >= 0.7 for d in resultado)


@pytest.mark.parametrize("umbral, esperado", [(0.0, 3), (0.6, 2), (0.95, 0)])
def test_filtra_varios_umbrales(detecciones, umbral, esperado):
    assert len(filtrar_por_confianza(detecciones, umbral)) == esperado


def test_umbral_invalido_lanza(detecciones):
    with pytest.raises(ValueError):
        filtrar_por_confianza(detecciones, 1.5)


# mypy
# src /  # verifica los tipos
# pytest
# tests /  # ejecuta las pruebas:  4 passed
