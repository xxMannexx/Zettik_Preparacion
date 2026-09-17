import random
from time import perf_counter

from pipeline_vixia.dataset_demo import generar_dataset_demo
from pipeline_vixia.pipeline import (
    construir_indices,
    seleccionar_por_umbral,
    IndiceTemporal,
    construir_grafo_proximidad,
    objetos_proximos,
    grupos_de_objetos,
)


def medir():
    tamanos = [
        100,
        200,
        400,
        800,
    ]

    print(
        "n\tF1_hash\tF2_sort\tF3_arbol\tF4_grafo"
    )

    for n in tamanos:

        dataset = generar_dataset_demo(
            n,
            seed=42
        )

        # FASE 1
        inicio = perf_counter()

        indices = construir_indices(dataset)

        t1 = perf_counter() - inicio

        unicas = list(
            indices["por_id"].values()
        )

        # FASE 2
        inicio = perf_counter()

        seleccionar_por_umbral(
            unicas,
            0.7
        )

        t2 = perf_counter() - inicio

        # FASE 3
        mezcladas = unicas.copy()

        random.Random(42).shuffle(
            mezcladas
        )

        inicio = perf_counter()

        indice = IndiceTemporal()

        for d in mezcladas:
            indice.insertar(d)

        indice.cronologico()

        t3 = perf_counter() - inicio

        # FASE 4
        inicio = perf_counter()

        grafo = construir_grafo_proximidad(
            unicas,
            50
        )

        if unicas:
            objetos_proximos(
                grafo,
                unicas[0].id,
                2
            )

        grupos_de_objetos(grafo)

        t4 = perf_counter() - inicio

        print(
            f"{n}\t"
            f"{t1:.6f}\t"
            f"{t2:.6f}\t"
            f"{t3:.6f}\t"
            f"{t4:.6f}"
        )


if __name__ == "__main__":
    medir()