# Mutable: el aliasing es observable
lista_a = [1,2,3]
lista_b = lista_a ## Mismo objeto: aliasing
lista_b[0] = 99
print(lista_a)

# Inmutable: al aliasing existe pero es inobservable
s1 = "Hola"
s2 = s1
s2 = s2 + "Mundo"
print(s1)

# Obtener una copia independiente de un mutable (Evitar aliasing)
lista_c = lista_a.copy() ## Objeto nuevo con mismo valor
lista_c[0] = 0
print(lista_a)
