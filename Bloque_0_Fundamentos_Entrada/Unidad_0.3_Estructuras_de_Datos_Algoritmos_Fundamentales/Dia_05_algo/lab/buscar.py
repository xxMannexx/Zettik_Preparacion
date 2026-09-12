def buscar(self,dato):
    nodo = self.raiz

    while nodo is not None:
        if nodo.data == dato:
            return nodo.data
        elif nodo.data < dato:
            nodo = nodo.derecha
        else:
            nodo = nodo.izquierda

    return None