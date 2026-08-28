from __future__ import annotations

import logging


def configurar_logging(nivel: int = logging.INFO) -> None:
    """Configura logging una sola vez para consola."""
    logging.basicConfig(
        level=nivel,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
