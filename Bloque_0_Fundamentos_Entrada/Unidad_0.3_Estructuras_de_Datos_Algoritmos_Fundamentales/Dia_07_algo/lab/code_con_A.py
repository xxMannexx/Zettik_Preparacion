def busqueda_binaria(lista_ordenada: list, elemento:int) -> int:
    "Devuelve el indice del objetivo, o -1 si no esta. Requiere lista ORDENADA."""
    bajo,alto = 0, len(lista_ordenada)-1
    while bajo<=alto:
        medio = (bajo+alto)//2                ##Punto medio del rango actual
        if lista_ordenada[medio]==elemento:
            return medio  ## Encontrado
        elif elemento < lista_ordenada[medio]:
            alto = medio - 1
        else:
            bajo = medio + 1
    return -1



## Verificacion
datos = list(range(0, 1000, 2))             # [0, 2, 4, ..., 998] - ordenada
# assert busqueda_binaria(datos, 42) == 21    # 42 esta en el indice 21
# assert busqueda_binaria(datos, 43) == -1    # 43 no existe (impar)

## VARIANTES ##

def binaria_recursiva(lista, objetivo, bajo=0, alto=None) -> int:
    if alto is None: alto = len(lista) - 1
    if bajo > alto: return -1  # caso base: rango vacío -> no existe
    medio = (bajo + alto) // 2
    if lista[medio] == objetivo:
        return medio
    elif objetivo < lista[medio]:
        return binaria_recursiva(lista, objetivo, bajo, medio - 1)
    else:
        return binaria_recursiva(lista, objetivo, medio + 1, alto)


# Variante: buscar el LIMITE IZQUIERDO (primer indice donde lista[i] >= objetivo)
def limite_izquierdo(lista, objetivo) -> int:
    """Primer indice donde lista[i] >= objetivo. Util para buscar en rangos."""
    bajo, alto = 0, len(lista)
    while bajo < alto:
        medio = (bajo + alto) // 2
        if lista[medio] < objetivo:
            bajo = medio + 1
        else:
            alto = medio
    return bajo



## Hacer observable la ventaja

import time, random

n_grande = 1_000_000
datos_sorted = sorted(random.sample(range(n_grande * 10), n_grande))
objetivo = datos_sorted[n_grande // 2]

# Busqueda LINEAL: O(n)
t0 = time.perf_counter()
for _ in range(1000): datos_sorted.index(objetivo)
t_lineal = time.perf_counter() - t0

# Busqueda BINARIA: O(log n)
t0 = time.perf_counter()
for _ in range(1000): busqueda_binaria(datos_sorted, objetivo)
t_binaria = time.perf_counter() - t0

print(f"n={n_grande:,}: lineal={t_lineal * 1000:.1f}ms, binaria={t_binaria * 1000:.2f}ms, "
      f"ventaja={t_lineal / t_binaria:.0f}x")
# La ventaja es enorme: log2(1_000_000) ~ 20 pasos vs 500_000 promedio.
