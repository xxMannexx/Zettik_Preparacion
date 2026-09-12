from lab.code_con_A import NodoArbol


class ABB:
    def __init__(self):
        self.raiz = None

    def insertar(self,valor):
        self.raiz = self._insertar(self.raiz,valor)

    def _insertar(self,nodo,valor):
        if nodo is None:
            return NodoArbol(valor)
        if valor < nodo.dato:
            nodo.izquierdo = self._insertar(nodo.izquierdo,valor)
        elif valor > nodo.dato:
            nodo.derecho = self._insertar(nodo.derecho,valor)
        return nodo

    def buscar(self,valor):
        nodo = self.raiz
        while nodo is not None:
            if nodo.dato == valor:
                return nodo.dato
            elif valor < nodo.dato:
                nodo = nodo.izquierdo
            else:
                nodo = nodo.derecho
            return False

    def minimo(self):
        if self.raiz is None:
            return None
        nodo = self.raiz
        while nodo.izquierdo is not None:
            nodo = nodo.izquierdo
        return nodo.dato

    def maximo(self):
        if self.raiz is None:
            return None
        nodo = self.raiz
        while nodo.derecho is not None:
            nodo = nodo.derecho
        return nodo.dato

    def en_orden(self):
        resultado = []
        self._en_orden(self.raiz, resultado)
        return resultado

    def _en_orden(self, nodo, resultado):
        if nodo is not None:
            self._en_orden(nodo.izquierdo, resultado)  # 1. todo lo MENOR (izquierda)
            resultado.append(nodo.dato)  # 2. el nodo
            self._en_orden(nodo.derecho, resultado)  # 3. todo lo MAYOR (derecha)

    def pre_orden(self):  # nodo primero (util para copiar/serializar)
        resultado = []
        self._pre_orden(self.raiz, resultado)
        return resultado

    def _pre_orden(self, nodo, resultado):
        if nodo is not None:
            resultado.append(nodo.dato)  # 1. el nodo PRIMERO
            self._pre_orden(nodo.izquierdo, resultado)
            self._pre_orden(nodo.derecho, resultado)

    def post_orden(self):  # nodo ultimo (util para liberar)
        resultado = []
        self._post_orden(self.raiz, resultado)
        return resultado

    def _post_orden(self, nodo, resultado):
        if nodo is not None:
            self._post_orden(nodo.izquierdo, resultado)
            self._post_orden(nodo.derecho, resultado)
            resultado.append(nodo.dato)  # 3. el nodo AL FINAL