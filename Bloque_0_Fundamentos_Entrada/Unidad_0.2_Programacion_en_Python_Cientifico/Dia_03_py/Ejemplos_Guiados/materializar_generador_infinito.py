import itertools


# Defecto 1: materializar un generador INFINITO agota la memoria (no termina)
def contador_infinito():
    n = 0
    while True:
        yield n
        n += 1


# list(contador_infinito())   # ¡NUNCA usar! Intentaría construir una lista infinita -> OOM
# Correcto: recortar antes de materializar
print(list(itertools.islice(contador_infinito(), 5)))  # [0, 1, 2, 3, 4]

# Defecto 2: reutilizar un generador ya agotado devuelve vacío
gen = (x for x in range(3))
total1 = sum(gen)  # 3: consume y agota
total2 = sum(gen)  # 0: agotado
print(total1, total2)  # 3 0  <- la segunda suma es 0, no 3
# Correcto: crear el generador de nuevo, o materializar si se necesitan varios recorridos
valores = list(range(3))  # materializa una vez
print(sum(valores), sum(valores))  # 3 3: la lista permite múltiples recorridos
