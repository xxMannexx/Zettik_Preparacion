from __future__ import annotations

import cProfile
import pstats
from pathlib import Path

from vixia_utils.deteccion import Deteccion, filtrar_por_confianza


def carga() -> list[Deteccion]:
    return [
        Deteccion(f"objeto_{i}", (i % 100) / 100)
        for i in range(10_000)
    ]


def benchmark() -> None:
    detecciones = carga()
    for _ in range(200):
        filtrar_por_confianza(detecciones, 0.70)


def main() -> None:
    salida = Path("profiling/profile_filtrado.txt")
    perfil = cProfile.Profile()
    perfil.enable()
    benchmark()
    perfil.disable()

    with salida.open("w", encoding="utf-8") as f:
        stats = pstats.Stats(perfil, stream=f).sort_stats("cumulative")
        stats.print_stats(15)

    print(f"Perfil guardado en {salida}")


if __name__ == "__main__":
    main()
