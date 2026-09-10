class Par:
    __slots__ = ["clave","valor","siguiente"]
    def __init__(self, clave, valor):
        self.clave = clave
        self.valor = valor
        self.siguiente = None ## Base del encadenamiento

class TablaHash:
    def __init__(self,m=8):
        self._m = m
        self._cubetas = [None] * m ## Inicializa el array con m cubetas cada una es una cabeza de lista
        self._n = 0

    def _indice(self, clave):
        return hash(clave) % self._m  ##Funcion hash mas modulo

    def insertar(self,clave,valor):
        i = self._indice(clave)  ## localiza la cubeta
        actual = self._cubetas[i] ## Pone en disponibilidad la cubeta para usarla
        while actual is not None:
            if actual.clave == clave:
                actual.valor = valor  # clave existente: actualizar
                return
            actual = actual.siguiente
        nuevo = Par(clave,valor)
        nuevo.siguiente = self._cubetas[i]
        self._cubetas[i] = nuevo
        self._n += 1

    def buscar(self, clave):
        i = self._indice(clave)          # O(1): localizar la cubeta
        actual = self._cubetas[i]
        while actual is not None:        # recorrer solo la lista de ESA cubeta
            if actual.clave == clave:
                return actual.valor
            actual = actual.siguiente
        raise KeyError(clave)

