from collections import deque

def bfs(grafo : dict, inicio : str, destino: str = None) -> dict:
    """
        BFS desde 'inicio'. Devuelve distancias y predecesores.
        Camino mas corto si destino != None.
        """
    distancia = {inicio:0}
    predecesor = {inicio:None}
    cola = deque([inicio])


    while cola:
        atual = cola.popleft()
        if atual == destino:
            break
        for vecino in grafo.get(atual, []):
            if vecino not in distancia:
                distancia[vecino] = distancia[atual] + 1
                predecesor[vecino] = atual
                cola.append(vecino)
    return distancia, predecesor

def reconstruir_camino(predecesor: dict, inicio: str, destino: str) -> list:
    """Reconstruir el camino mas corto desde inicio hasta destino."""
    if destino not in predecesor:
        return []                             # destino no alcanzable
    camino = []
    nodo = destino
    while nodo is not None:
        camino.append(nodo)
        nodo = predecesor[nodo]
    return camino[::-1]


grafo = {
    "A": ["B", "C"], "B": ["A", "D", "E"],
    "C": ["A", "F"], "D": ["B"],
    "E": ["B", "F"], "F": ["C", "E"],
}
dist, pred = bfs(grafo, "A")
print(f"Distancias desde A: {dist}")        # {'A':0,'B':1,'C':1,'D':2,'E':2,'F':2}
camino = reconstruir_camino(pred, "A", "F")
print(f"Camino mas corto A->F: {camino}")   # ['A', 'C', 'F'] (longitud 2)
