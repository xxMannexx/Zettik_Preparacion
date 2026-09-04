# O(1) espacio: opera in situ (intercambia elementos sin copiar)
def invertir_in_situ(lista):
    i, j = 0, len(lista) - 1
    while i < j:
        lista[i], lista[j] = lista[j], lista[i]  # intercambio: O(1) espacio extra
        i += 1;
        j -= 1
    return lista  # tiempo O(n), espacio O(1)


# O(n) espacio: construye una copia nueva
def invertir_copia(lista):
    return lista[::-1]  # nueva lista: tiempo O(n), espacio O(n)
# Misma complejidad temporal O(n), distinta complejidad espacial: O(1) vs O(n).
