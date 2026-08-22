numeros = [1,2,3,4,5,6,7,8,9,10]

# map: aplicar una función a cada elemento
list(map(lambda x: x ** 2, numeros))  # [1, 4, 9, 16, 25]

# filter: conservar los que cumplen un predicado
list(filter(lambda x: x % 2 == 0, numeros))  # [2, 4]

# sorted con key: ordenar por un criterio calculado
palabras = ["bb", "a", "cccc", "ddd"]
sorted(palabras, key=len)  # ['a', 'bb', 'ddd', 'cccc'] (por longitud)
sorted(palabras, key=len, reverse=True)  # orden inverso

# Ordenar estructuras por un campo (key con lambda):
detecciones = [("persona", 0.9), ("coche", 0.7), ("bici", 0.95)]
sorted(detecciones, key=lambda d: d[1], reverse=True)  # por confianza, descendente
# [('bici', 0.95), ('persona', 0.9), ('coche', 0.7)]


datos = [("Ana", 90), ("Luis", 70), ("Marta", 85)]

print(sorted(datos, key=lambda d: d[1]))