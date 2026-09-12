from lab.code_con_A import NodoArbol


def _insertar(self,nodo,valor):
    if nodo is None:
        return NodoArbol(valor)

    if valor < nodo.dato:
        nodo.izquierdo = self._insertar(nodo.izquierdo, valor)
    elif valor > nodo.dato:
        nodo.derecha = self._insertar(nodo.derecha, valor)

    return nodo