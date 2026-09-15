# Representacion: lista de adyacencia (dict de listas) -- O(V + E) espacio
grafo_no_dirigido = {
    "A": ["B", "C"],
    "B": ["A", "D", "E"],
    "C": ["A", "F"],
    "D": ["B"],
    "E": ["B", "F"],
    "F": ["C", "E"],
}
# Equivalente con defaultdict para grafos dinamicos:
from collections import defaultdict


def nuevo_grafo(): return defaultdict(list)


def agregar_arista(g, u, v, dirigido=False):
    g[u].append(v)
    if not dirigido:
        g[v].append(u)  # arista bidireccional
