# Ejemplo 1: O(n) -- un bucle sobre n
def contiene(lista, objetivo):  # busqueda lineal
    for x in lista:  # n iteraciones, cuerpo O(1)
        if x == objetivo:  # O(1)
            return True
    return False  # -> O(n)


# Ejemplo 2: O(n^2) -- bucles anidados sobre n
def hay_duplicados(lista):
    for i in range(len(lista)):  # n
        for j in range(i + 1, len(lista)):  # ~n por cada i
            if lista[i] == lista[j]:  # O(1)
                return True
    return False  # -> O(n^2)


# Ejemplo 3: O(log n) -- division a la mitad (busqueda binaria, en lista ORDENADA)
def busqueda_binaria(lista_ordenada, objetivo):
    bajo, alto = 0, len(lista_ordenada) - 1
    while bajo <= alto:  # el rango se reduce a la mitad cada vez
        medio = (bajo + alto) // 2
        if lista_ordenada[medio] == objetivo:
            return medio
        elif lista_ordenada[medio] < objetivo:
            bajo = medio + 1  # descarta la mitad inferior
        else:
            alto = medio - 1  # descarta la mitad superior
    return -1  # -> O(log n)
