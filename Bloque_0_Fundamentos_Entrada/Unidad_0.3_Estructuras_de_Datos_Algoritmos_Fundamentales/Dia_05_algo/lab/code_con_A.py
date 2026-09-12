class NodoArbol:
    __slots__ = ['dato','izquierdo','derecho']
    def __init__(self, dato):
        self.dato = dato
        self.izquierdo = None
        self.derecho = None

# Construir un arbol pequeño:
#        10
#       /  \
#      5    15
#     / \     \
#    3   7     20

raiz = NodoArbol(10)
raiz.izquierdo = NodoArbol(5)
raiz.izquierdo.izquierdo = NodoArbol(3)
raiz.izquierdo.derecho = NodoArbol(7)
raiz.derecho = NodoArbol(15)
raiz.derecho.derecho = NodoArbol(20)
# La raiz (10) no tiene padre; 3, 7, 20 son hojas (sin hijos).
# La altura es 2 (raiz -> 5 -> 3, dos aristas).

