from dataclasses import dataclass
import math
from collections import deque
import random

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

    return ordenadas[limite_izquierdo(lista,umbral):][::-1]

class NodoTiempo:
    """
    Nodo del árbol.
    conserva la Deteccion completa.
    """

    __slots__ = (
        "timestamp",
        "deteccion",
        "izq",
        "der",
    )

    def __init__(
        self,
        deteccion: Deteccion
    ):
        self.timestamp = deteccion.timestamp
        self.deteccion = deteccion

        self.izq: NodoTiempo | None = None
        self.der: NodoTiempo | None = None


class IndiceTemporal:

    def __init__(self):
        self.raiz: NodoTiempo | None = None

    def insertar(
            self,
            deteccion: Deteccion
    ) -> None:

        self.raiz = self._insertar(
            self.raiz,
            deteccion
        )

    def _insertar(
            self,
            nodo: NodoTiempo | None,
            deteccion: Deteccion
    ) -> NodoTiempo:

        # Encontramos el hueco.
        if nodo is None:
            return NodoTiempo(deteccion)

        # Timestamp menor -> izquierda.
        if deteccion.timestamp < nodo.timestamp:
            nodo.izq = self._insertar(
                nodo.izq,
                deteccion
            )

        # Timestamp mayor o igual -> derecha.
        else:
            nodo.der = self._insertar(
                nodo.der,
                deteccion
            )

        return nodo


    def buscar_timestamp(
            self,
            timestamp: int
    ) -> Deteccion | None:

        nodo = self.raiz

        while nodo is not None:

            if timestamp == nodo.timestamp:
                return nodo.deteccion

            if timestamp < nodo.timestamp:
                nodo = nodo.izq

            else:
                nodo = nodo.der

        return None



    def cronologico(self) -> list[Deteccion]:

        resultado: list[Deteccion] = []

        self._en_orden(
            self.raiz,
            resultado
        )

        return resultado

    def _en_orden(
            self,
            nodo: NodoTiempo | None,
            resultado: list[Deteccion]
    ) -> None:

        if nodo is None:
            return

        # Viejos primero.
        self._en_orden(
            nodo.izq,
            resultado
        )

        # Nodo actual.
        resultado.append(
            nodo.deteccion
        )

        # Más recientes después.
        self._en_orden(
            nodo.der,
            resultado
        )



    def mas_reciente(
            self
    ) -> Deteccion | None:

        if self.raiz is None:
            return None

        nodo = self.raiz

        # El máximo de un ABB está
        # todo a la derecha.
        while nodo.der is not None:
            nodo = nodo.der

        return nodo.deteccion




def construir_grafo_proximidad(
        detecciones: list[Deteccion],
        umbral_dist: float
) -> dict[str, list[str]]:

    grafo: dict[str, list[str]] = {
        deteccion.id: []
        for deteccion in detecciones
    }

    # Comparamos cada pareja una sola vez.
    for i, actual in enumerate(detecciones):

        for otro in detecciones[i + 1:]:

            distancia = math.hypot(
                actual.x - otro.x,
                actual.y - otro.y
            )

            if distancia < umbral_dist:
                # Grafo NO dirigido.
                actual_vecinos = grafo[actual.id]
                otro_vecinos = grafo[otro.id]

                actual_vecinos.append(otro.id)
                otro_vecinos.append(actual.id)

    return grafo



def objetos_proximos(
        grafo: dict[str, list[str]],
        inicio: str,
        max_saltos: int
) -> dict[str, int]:
    if inicio not in grafo:
        return {}


    distancias: dict[str, int] = {
        inicio: 0
    }

    # FIFO -> BFS.
    cola = deque([inicio])

    while cola:

        actual = cola.popleft()

        # Ya llegamos a la profundidad solicitada.
        if distancias[actual] >= max_saltos:
            continue

        for vecino in grafo.get(actual, []):

            # Si no fue descubierto todavía.
            if vecino not in distancias:
                distancias[vecino] = (
                        distancias[actual] + 1
                )

                cola.append(vecino)

    return distancias



def grupos_de_objetos(
        grafo: dict[str, list[str]]
) -> list[list[str]]:


    visitados: set[str] = set()

    grupos: list[list[str]] = []

    # Hay que comenzar un DFS por cada
    # componente que todavía no conocemos.
    for inicio in grafo:

        if inicio in visitados:
            continue

        grupo: list[str] = []

        # LIFO -> DFS.
        pila = [inicio]

        while pila:

            actual = pila.pop()

            if actual in visitados:
                continue

            visitados.add(actual)

            grupo.append(actual)

            for vecino in grafo.get(actual, []):

                if vecino not in visitados:
                    pila.append(vecino)

        grupos.append(
            sorted(grupo)
        )

    return grupos


def ejecutar_pipeline(
        detecciones: list[Deteccion],
        *,
        umbral_confianza: float,
        umbral_dist: float,
        max_saltos: int,
        limite_n: int = 100_000
) -> dict:

    # Defensa general: acotar recursos.
    if len(detecciones) > limite_n:
        raise ValueError(
            f"dataset excede el limite: "
            f"{len(detecciones)} > {limite_n}"
        )


    indices = construir_indices(detecciones)

    unicas = list(
        indices["por_id"].values()
    )

    seleccionadas = seleccionar_por_umbral(
        unicas,
        umbral_confianza
    )

    indice_temporal = IndiceTemporal()


    mezcladas = unicas.copy()

    rng = random.Random(42)
    rng.shuffle(mezcladas)

    for deteccion in mezcladas:
        indice_temporal.insertar(deteccion)

    cronologia = indice_temporal.cronologico()
    mas_reciente = indice_temporal.mas_reciente()


    grafo = construir_grafo_proximidad(
        unicas,
        umbral_dist
    )

    grupos = grupos_de_objetos(grafo)

    if unicas:
        primer_id = unicas[0].id

        proximos = objetos_proximos(
            grafo,
            primer_id,
            max_saltos
        )
    else:
        proximos = {}


    if unicas:
        complejidad_dominante = (
            "O(V^2) construccion del grafo"
        )
    else:
        complejidad_dominante = "vacio"

    return {
        "n_unicas": len(unicas),
        "duplicados": indices["duplicados"],
        "seleccionadas": seleccionadas,
        "n_seleccionadas": len(seleccionadas),
        "cronologia": cronologia,
        "mas_reciente": mas_reciente,
        "grafo": grafo,
        "grupos": grupos,
        "proximos_al_primero": proximos,
        "complejidad_dominante": complejidad_dominante,
    }









