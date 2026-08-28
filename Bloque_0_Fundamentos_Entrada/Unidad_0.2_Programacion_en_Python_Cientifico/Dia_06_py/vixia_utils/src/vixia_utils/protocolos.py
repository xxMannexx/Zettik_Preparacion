from __future__ import annotations

import logging
from typing import Protocol

from .deteccion import Deteccion

logger = logging.getLogger(__name__)


class Detector(Protocol):
    """Interfaz estructural: no exige herencia."""

    def detectar(self, entrada: str) -> list[Deteccion]:
        ...


def ejecutar_detector(detector: Detector, entrada: str) -> list[Deteccion]:
    """Ejecuta cualquier objeto que satisfaga el Protocol Detector."""
    if not isinstance(entrada, str) or not entrada.strip():
        raise ValueError("entrada debe ser una cadena no vacía")

    resultado = detector.detectar(entrada)

    # Se registra solo información operacional no sensible.
    logger.debug("detector ejecutado; detecciones=%d", len(resultado))
    return resultado
