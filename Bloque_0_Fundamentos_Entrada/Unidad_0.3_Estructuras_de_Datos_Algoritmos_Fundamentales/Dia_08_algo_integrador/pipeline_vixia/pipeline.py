from dataclasses import dataclass

@dataclass(frozen=True)
class Deteccion:

    id : str
    clase : str
    confianza : float
    x : float
    y : float
    timestamp : int

def construir_indices(detecciones: list[Deteccion]) -> dict:
    por_id = {}
    por_clase = {}
    vistos = set()
    duplicados = 0

    for i in detecciones:
        if i.id in vistos:
            duplicados += 1
            continue

        por_id[i.id] = i


        if i.clase not in por_clase:
            por_clase[i.clase] = []

        por_clase[i.clase].append(i)

        vistos.add(i.id)

    return {
        "por_id": por_id,
        "por_clase": por_clase,
        "vistos": vistos,
        "duplicados": duplicados
    }

def limite_izquierdo(confianzas: list[float],umbral:float)-> int:
    bajo=0
    alto=len(confianzas)
    while bajo<alto:
        medio=(bajo+alto) // 2

        if confianzas[medio]<umbral:
            bajo=medio+1
        else:
            alto=medio

    return bajo



def seleccionar_por_umbral(detecciones: list[Deteccion],umbral: float) -> list[Deteccion]:

    ordenadas = sorted(detecciones, key=lambda x: x.confianza)

    lista = []
    for i in ordenadas:
        lista.append(i.confianza)

    return ordenadas[limite_izquierdo(lista,umbral):]


detecciones = [
    Deteccion(
        id="obj_01",
        clase="persona",
        confianza=0.91,
        x=10.5,
        y=20.0,
        timestamp=100
    ),
    Deteccion(
        id="obj_02",
        clase="coche",
        confianza=0.78,
        x=15.2,
        y=22.4,
        timestamp=101
    ),
    Deteccion(
        id="obj_03",
        clase="persona",
        confianza=0.84,
        x=8.0,
        y=19.3,
        timestamp=102
    )
]

lista = seleccionar_por_umbral(detecciones,umbral=0.8)
print(lista)













