"""Utilidades mínimas de calidad para VizionarIA."""

from .deteccion import Deteccion, confianza_media, filtrar_por_confianza
from .protocolos import Detector, ejecutar_detector

__all__ = [
    "Deteccion",
    "confianza_media",
    "filtrar_por_confianza",
    "Detector",
    "ejecutar_detector",
]
