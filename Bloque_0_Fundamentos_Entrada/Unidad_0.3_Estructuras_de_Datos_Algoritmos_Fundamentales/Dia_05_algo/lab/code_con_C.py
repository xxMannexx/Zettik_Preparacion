from lab.code_con_B import ABB


def eliminar(self,valor):
    self.raiz =self._eliminar(self.raiz,valor)

def _eliminar(self,nodo,valor):
    if nodo is None:
        return None
    if valor < nodo.dato:
        nodo.izquierdo = self._eliminar(nodo.izquierdo,valor)
    elif valor > nodo.dato:
        nodo.derecho = self._eliminar(nodo.derecho,valor)
    else:
        if nodo.izquierdo is None:  # 0 o 1 hijo (derecho)
            return nodo.derecho
        if nodo.derecho is None:  # 1 hijo (izquierdo)
            return nodo.izquierdo
            # 2 hijos: reemplazar por el sucesor en-orden (minimo del subarbol derecho)
        sucesor = nodo.derecho
        while sucesor.izquierdo is not None:
            sucesor = sucesor.izquierdo
        nodo.dato = sucesor.dato  # copiar el valor del sucesor
        nodo.derecho = self._eliminar(nodo.derecho, sucesor.dato)  # eliminar el sucesor
    return nodo


import time, random


# Busqueda en un ABB (equilibrado en promedio con insercion aleatoria) vs lista O(n)
def medir_abb_vs_lista(n):
    valores = list(range(n))
    random.shuffle(valores)  # insercion aleatoria -> arbol ~equilibrado
    arbol = ABB()
    for v in valores: arbol.insertar(v)
    lista = list(range(n))
    objetivo = n - 1
    t0 = time.perf_counter()
    for _ in range(1000): arbol.buscar(objetivo)
    t_arbol = time.perf_counter() - t0
    t0 = time.perf_counter()
    for _ in range(1000): _ = objetivo in lista
    t_lista = time.perf_counter() - t0
    return t_arbol, t_lista


for n in [10_000, 100_000, 1_000_000]:
    t_arbol, t_lista = medir_abb_vs_lista(n)
    print(f"n={n:>9,}: ABB O(log n)={t_arbol * 1000:6.2f} ms, lista O(n)={t_lista * 1000:8.2f} ms")
# El ABB escala logaritmicamente: al multiplicar n por 10, los pasos suben poco (log).
