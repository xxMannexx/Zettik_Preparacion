import time


# El factor de carga afecta el rendimiento: una tabla sobrecargada degrada
# (Simulamos con una funcion hash mala que concentra las claves)
def medir_con_carga(num_cubetas, num_elementos):
    cubetas = [[] for _ in range(num_cubetas)]  # listas como cubetas
    for k in range(num_elementos):
        i = (k * 2654435761) % num_cubetas  # dispersion
        cubetas[i].append(k)
    # Medir la busqueda promedio
    t0 = time.perf_counter()
    for k in range(0, num_elementos, max(1, num_elementos // 1000)):
        i = (k * 2654435761) % num_cubetas
        _ = k in cubetas[i]  # buscar en la cubeta
    return time.perf_counter() - t0, num_elementos / num_cubetas


print("Efecto del factor de carga (alpha = n/m):")
n = 100_000
for m in [200_000, 100_000, 10_000, 1_000]:  # menos cubetas -> mayor carga
    t, alpha = medir_con_carga(m, n)
    print(f"  m={m:>7} cubetas, alpha={alpha:6.1f}: busqueda {t * 1000:7.2f} ms")
# A mayor factor de carga (listas mas largas), la busqueda se ralentiza.
