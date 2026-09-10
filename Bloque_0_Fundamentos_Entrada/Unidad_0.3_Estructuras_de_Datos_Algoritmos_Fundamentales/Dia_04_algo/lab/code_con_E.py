import time


# Demostrar el peor caso: claves que colisionan deliberadamente degradan a O(n)
# (Usamos una funcion hash mala y predecible para ilustrar)
class TablaVulnerable:
    def __init__(self, m=1024):
        self._m = m
        self._cubetas = [[] for _ in range(m)]

    def _indice_malo(self, clave):
        return 0  # PESIMO: todas las claves caen en la cubeta 0

    def _indice_bueno(self, clave):
        return hash(clave) % self._m  # distribuye (con aleatorizacion de Python)

    def insertar(self, clave, malo=False):
        i = self._indice_malo(clave) if malo else self._indice_bueno(clave)
        self._cubetas[i].append((clave, clave))


print("Peor caso (todas las claves en una cubeta) vs caso normal:")
for n in [1_000, 2_000, 4_000]:
    # Caso normal: distribucion uniforme -> O(1) promedio
    t_buena = TablaVulnerable()
    t0 = time.perf_counter()
    for k in range(n): t_buena.insertar(k, malo=False)
    t_normal = time.perf_counter() - t0
    # Peor caso: todas en la cubeta 0 -> O(n) por insercion -> O(n^2)
    t_mala = TablaVulnerable()
    t0 = time.perf_counter()
    for k in range(n): t_mala.insertar(k, malo=True)
    t_peor = time.perf_counter() - t0
    print(f"  n={n:>5}: normal O(n)={t_normal * 1000:7.2f} ms, peor caso O(n^2)={t_peor * 1000:8.2f} ms, "
          f"degradacion={t_peor / t_normal:.0f}x")
# El peor caso (hash flooding) degrada drasticamente, y empeora con n (O(n^2) vs O(n)).
