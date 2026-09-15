# DFS ITERATIVO: usa la pila (Dia 2) explicitamente
from lab.code_con_C import bfs


def dfs_iterativo(grafo: dict, inicio: str) -> list:
    """DFS iterativo con pila. Devuelve el orden de visita."""
    visitados = set()  # conjunto de visitados: O(1) lookup (Dia 4)
    pila = [inicio]  # pila LIFO (Dia 2)
    orden = []
    while pila:
        actual = pila.pop()  # el mas recientemente descubierto (LIFO)
        if actual in visitados:
            continue
        visitados.add(actual)
        orden.append(actual)
        for vecino in reversed(grafo.get(actual, [])):  # invertir para mantener orden
            if vecino not in visitados:
                pila.append(vecino)  # explorar en profundidad primero
    return orden


# DFS RECURSIVO: la pila de llamadas actua como la pila
def dfs_recursivo(grafo: dict, inicio: str, visitados: set = None) -> list:
    if visitados is None: visitados = set()
    visitados.add(inicio)
    orden = [inicio]
    for vecino in grafo.get(inicio, []):
        if vecino not in visitados:
            orden.extend(dfs_recursivo(grafo, vecino, visitados))  # recursion (Dia 5)
    return orden


# Aplicaciones de DFS:
def tiene_ciclo(grafo: dict) -> bool:
    """Detectar si un grafo no dirigido tiene ciclo."""
    visitados = set()

    def dfs_ciclo(nodo, padre):
        visitados.add(nodo)
        for vecino in grafo.get(nodo, []):
            if vecino not in visitados:
                if dfs_ciclo(vecino, nodo): return True
            elif vecino != padre:  # vecino visitado != padre -> ciclo
                return True
        return False

    for nodo in grafo:
        if nodo not in visitados:
            if dfs_ciclo(nodo, None): return True
    return False


def componentes_conexas(grafo: dict) -> list:
    """Encontrar todos los componentes conexos con DFS."""
    visitados = set();
    componentes = []
    for nodo in grafo:
        if nodo not in visitados:
            comp = dfs_recursivo(grafo, nodo, visitados)
            componentes.append(comp)
    return componentes

grafo = {
    "A": ["B", "C"],
    "B": ["A", "D"],
    "C": ["A", "D"],
    "D": ["B", "C"]
}
print(f"BFS desde A: {list(bfs(grafo, 'A')[0].keys())}")   # A B C D E F (por capas)
print(f"DFS desde A: {dfs_iterativo(grafo, 'A')}")          # A B D E F C (en profundidad)
# BFS: A (capa 0), B C (capa 1), D E F (capa 2) -- por distancia
# DFS: A, luego todo lo alcanzable por B (D, E, F), luego C -- en profundidad
print(f"Tiene ciclo: {tiene_ciclo(grafo)}")
