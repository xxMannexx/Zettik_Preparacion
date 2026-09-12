from lab.code_con_B import ABB


# def en_orden(self):
#     resultado = []
#     self._en_orden(self.raiz,resultado)
#     return resultado
# def _en_orden(self,nodo,resultado):
#     if nodo is not None:
#         self._en_orden(nodo.izquierdo, resultado)  # 1. todo lo MENOR (izquierda)
#         resultado.append(nodo.dato)  # 2. el nodo
#         self._en_orden(nodo.derecho, resultado)  # 3. todo lo MAYOR (derecha)
#
# def pre_orden(self):  # nodo primero (util para copiar/serializar)
#     resultado = []
#     self._pre_orden(self.raiz, resultado)
#     return resultado
#
# def _pre_orden(self, nodo, resultado):
#     if nodo is not None:
#         resultado.append(nodo.dato)  # 1. el nodo PRIMERO
#         self._pre_orden(nodo.izquierdo, resultado)
#         self._pre_orden(nodo.derecho, resultado)
#
# def post_orden(self):  # nodo ultimo (util para liberar)
#     resultado = []
#     self._post_orden(self.raiz, resultado)
#     return resultado
#
# def _post_orden(self, nodo, resultado):
#     if nodo is not None:
#         self._post_orden(nodo.izquierdo, resultado)
#         self._post_orden(nodo.derecho, resultado)
#         resultado.append(nodo.dato)  # 3. el nodo AL FINAL

arbol = ABB()
arbol.insertar(19)
arbol.insertar(20)
arbol.insertar(21)
arbol.insertar(22)
arbol.insertar(6)
arbol.insertar(7)
arbol.insertar(8)

print(arbol.en_orden())



