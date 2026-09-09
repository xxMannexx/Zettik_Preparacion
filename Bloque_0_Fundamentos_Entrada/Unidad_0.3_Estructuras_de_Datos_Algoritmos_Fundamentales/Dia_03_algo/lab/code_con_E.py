class NodoDoble:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None
        self.anterior = None # referencia ADICIONAL al nodo anterior


class ListaDoble:
    def __init__(self):
        self.cabeza = None
        self.cola = None
        self._size = 0

    def insertar_final(self,dato):
        nuevo = NodoDoble(dato)
        if self.cola is None:
            self.cabeza = self.cola = nuevo
        else:
            nuevo.anterior = self.cola  # el nuevo apunta atras a la antigua cola
            self.cola.siguiente = nuevo  # la antigua cola apunta adelante al nuevo
            self.cola = nuevo  # la cola pasa a ser el nuevo
        self._size += 1

    def eliminar_nodo(self, nodo):  # O(1): el nodo conoce a su anterior y siguiente
        if nodo.anterior is not None:
            nodo.anterior.siguiente = nodo.siguiente  # el anterior salta al siguiente
        else:
            self.cabeza = nodo.siguiente  # era la cabeza
        if nodo.siguiente is not None:
            nodo.siguiente.anterior = nodo.anterior  # el siguiente apunta atras al anterior
        else:
            self.cola = nodo.anterior  # era la cola
        self._size -= 1
        # Reajuste de 4 referencias, todas accesibles desde el nodo -> O(1)

    def recorrer_adelante(self):  # de la cabeza a la cola
        actual = self.cabeza
        while actual is not None:
            yield actual.dato
            actual = actual.siguiente

    def recorrer_atras(self):  # de la cola a la cabeza (posible por la doble referencia)
        actual = self.cola
        while actual is not None:
            yield actual.dato
            actual = actual.anterior



