import time

# Insertar al FINAL: O(1) amortizado.  Insertar al PRINCIPIO: O(n).
for n in [10_000, 20_000, 400_000]:
    # Final:
    t0 = time.perf_counter()
    lista = []
    for i in range(n): lista.append(i)  # O(1) amortizado cada uno
    t_final = time.perf_counter() - t0
    # Principio:
    t0 = time.perf_counter()
    lista = []
    for i in range(n): lista.insert(0, i)  # O(n) cada uno -> O(n^2) en total
    t_principio = time.perf_counter() - t0
    print(f"n={n:>6}: final={t_final * 1000:7.2f} ms,  principio={t_principio * 1000:8.2f} ms,  "
          f"ratio={t_principio / t_final:.0f}x")
# El principio es drasticamente mas lento, y la diferencia CRECE con n (O(n^2) vs O(n)).
