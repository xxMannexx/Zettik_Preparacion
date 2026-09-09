import time
from collections import deque  # deque es una lista doblemente enlazada de bloques (Dia 2)

# Insercion al PRINCIPIO: lista enlazada O(1) vs array O(n)
print("Insercion al principio: lista enlazada (deque) O(1) vs array (list) O(n)")
for n in [10_000, 20_000, 40_000]:
    # Array (list): insert(0) es O(n) -> O(n^2) en total
    t0 = time.perf_counter()
    arr = []
    for i in range(n): arr.insert(0, i)
    t_arr = time.perf_counter() - t0
    # Lista enlazada (deque): appendleft es O(1) -> O(n) en total
    t0 = time.perf_counter()
    enl = deque()
    for i in range(n): enl.appendleft(i)
    t_enl = time.perf_counter() - t0
    print(f"  n={n:>6}: array O(n^2)={t_arr * 1000:8.2f} ms, enlazada O(n)={t_enl * 1000:6.2f} ms, "
          f"ventaja={t_arr / t_enl:.0f}x")
# La lista enlazada gana DRASTICAMENTE en insercion al principio; el array ganaria en acceso.
