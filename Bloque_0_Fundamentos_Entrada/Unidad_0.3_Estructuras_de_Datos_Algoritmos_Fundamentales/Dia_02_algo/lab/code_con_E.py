from collections import deque
import time


# Cola con LISTA: dequeue (pop(0)) es O(n) -> procesar n elementos es O(n^2)
class ColaLista:
    def __init__(self): self._datos = []

    def enqueue(self, x): self._datos.append(x)  # O(1) amortizado

    def dequeue(self): return self._datos.pop(0)  # O(n)  <- PROBLEMA


# Cola con DEQUE: todas las operaciones O(1)
class ColaDeque:
    def __init__(self): self._datos = deque()

    def enqueue(self, x): self._datos.append(x)  # O(1)

    def dequeue(self): return self._datos.popleft()  # O(1)  <- eficiente


# Comparar: vaciar una cola de n elementos
for n in [10_000, 20_000, 40_000]:
    cl = ColaLista();
    [cl.enqueue(i) for i in range(n)]
    cd = ColaDeque();
    [cd.enqueue(i) for i in range(n)]
    t0 = time.perf_counter()
    while cl._datos: cl.dequeue()  # O(n^2) en total
    t_lista = time.perf_counter() - t0
    t0 = time.perf_counter()
    while cd._datos: cd.dequeue()  # O(n) en total
    t_deque = time.perf_counter() - t0
    print(f"n={n:>6}: lista(O(n^2))={t_lista * 1000:8.2f} ms, deque(O(n))={t_deque * 1000:6.2f} ms, "
          f"ventaja={t_lista / t_deque:.0f}x")
# La cola con deque escala linealmente; con lista, cuadraticamente. La ventaja crece con n.
