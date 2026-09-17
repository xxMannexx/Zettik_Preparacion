import random

from pipeline_vixia.pipeline import (
    Deteccion,
    ejecutar_pipeline
)


def generar_dataset_demo(
        n: int,
        seed: int = 42
) -> list[Deteccion]:

    rng = random.Random(seed)

    clases = [
        "persona",
        "coche",
        "bici"
    ]

    detecciones = []

    for i in range(n):
        detecciones.append(
            Deteccion(
                id=f"obj_{i}",
                clase=rng.choice(clases),
                confianza=round(
                    rng.uniform(0.4, 1.0),
                    3
                ),
                x=round(
                    rng.uniform(0, 500),
                    1
                ),
                y=round(
                    rng.uniform(0, 500),
                    1
                ),
                timestamp=1000 + i
            )
        )

    return detecciones


def main():

    dataset = generar_dataset_demo(
        n=40,
        seed=42
    )

    # Duplicados deliberados.
    dataset += dataset[:3]

    resultado = ejecutar_pipeline(
        dataset,
        umbral_confianza=0.70,
        umbral_dist=120,
        max_saltos=2
    )

    print("=" * 60)
    print("PIPELINE VIXIA — U0.3")
    print("=" * 60)

    print(
        "Detecciones unicas:",
        resultado["n_unicas"]
    )

    print(
        "Duplicados:",
        resultado["duplicados"]
    )

    print(
        "Seleccionadas:",
        resultado["n_seleccionadas"]
    )

    if resultado["mas_reciente"] is not None:
        print(
            "Timestamp mas reciente:",
            resultado["mas_reciente"].timestamp
        )

    print(
        "Grupos espaciales:",
        len(resultado["grupos"])
    )

    print(
        "Complejidad dominante:",
        resultado["complejidad_dominante"]
    )


if __name__ == "__main__":
    main()