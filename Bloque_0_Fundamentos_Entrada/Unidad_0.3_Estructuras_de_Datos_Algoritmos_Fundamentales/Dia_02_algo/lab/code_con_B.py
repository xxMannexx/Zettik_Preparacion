import time

# append es O(1) amortizado: agregar n elementos cuesta O(n) en TOTAL, O(1) por elemento
print("append (O(1) amortizado): el tiempo por elemento es ~constante")
for n in [100_000, 1_000_000, 10_000_000]:
    t0 = time.perf_counter()
    lista = []
    for i in range(n):
        lista.append(i)  # O(1) amortizado
    t = time.perf_counter() - t0
    print(f"  n={n:>12,}: {t * 1000:7.1f} ms total, {t / n * 1e9:.1f} ns por append")
# El tiempo por append es aproximadamente constante: confirma O(1) amortizado.
