from vixia_utils.deteccion import Deteccion
from vixia_utils.protocolos import ejecutar_detector


class DetectorSimulado:
    """No hereda de Detector: satisface el Protocol por estructura."""

    def detectar(self, entrada: str) -> list[Deteccion]:
        return [Deteccion("persona", 0.88)]


def test_protocol_por_duck_typing() -> None:
    resultado = ejecutar_detector(DetectorSimulado(), "frame_001")
    assert resultado == [Deteccion("persona", 0.88)]
