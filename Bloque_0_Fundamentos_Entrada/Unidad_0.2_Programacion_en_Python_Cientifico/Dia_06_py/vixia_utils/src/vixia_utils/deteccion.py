from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Sequence

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Deteccion:
    """Representa una detección validada."""

    objeto: str
    confianza: float

    def __post_init__(self) -> None:
        if not self.objeto.strip():
            raise ValueError("objeto no puede estar vacío")
        if not 0.0 <= self.confianza <= 1.0:
            raise ValueError("confianza debe estar entre 0 y 1")


def filtrar_por_confianza(
    detecciones: Sequence[Deteccion],
    umbral: float,
) -> list[Deteccion]:
    """Conserva las detecciones cuya confianza alcanza el umbral."""
    if not 0.0 <= umbral <= 1.0:
        raise ValueError("umbral debe estar entre 0 y 1")

    resultado = [d for d in detecciones if d.confianza >= umbral]

    # No se registran nombres, imágenes, rutas ni datos sensibles.
    logger.info(
        "filtrado completado: entrada=%d salida=%d umbral=%.2f",
        len(detecciones),
        len(resultado),
        umbral,
    )
    return resultado


def confianza_media(detecciones: Sequence[Deteccion]) -> float:
    """Calcula la confianza media; exige al menos una detección."""
    if not detecciones:
        raise ValueError("se requiere al menos una detección")
    return sum(d.confianza for d in detecciones) / len(detecciones)
