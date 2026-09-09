class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.siguiente = None


class ListaEnlazada:
    def __init__(self):
        self.cabeza = None
        self.size = 0

    def insertar_principio(self,dato):
        nuevo = Nodo(dato)
        nuevo.siguiente = self.cabeza
        self.cabeza = nuevo
        self.size += 1

    class Nodo:
        def __init__(self, valor):
            self.valor = valor
            self.siguiente = None

    def eliminar(self, dato):                 # O(n) por la busqueda, O(1) por el reajuste
        if self.cabeza is None:
            return False
        if self.cabeza.dato == dato:          # eliminar la cabeza
            self.cabeza = self.cabeza.siguiente
            self._tamano -= 1
            return True
        anterior = self.cabeza
        while anterior.siguiente is not None:
            if anterior.siguiente.dato == dato:
                anterior.siguiente = anterior.siguiente.siguiente   # saltar el nodo: O(1)
                self._tamano -= 1
                return True
            anterior = anterior.siguiente
        return False
