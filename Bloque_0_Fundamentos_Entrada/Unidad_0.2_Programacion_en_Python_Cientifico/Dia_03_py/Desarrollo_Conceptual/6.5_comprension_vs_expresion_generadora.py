import sys

lista = [x for x in range(1000000)]  ## Materializa todo el coste es O(N)
gen = iter(lista)  ## Genera un iterador de una sola pasada y solo computa lo que se consume entonces el coste es solo el valor que dara y no todo O(1)

print("En megabytes: ",(sys.getsizeof(lista)) / 1048576)
print("En bytes: ",sys.getsizeof(gen))

print(sum(x for x in range(10_000)))     # suma sin materializar la lista, computacionalmete mas compacto
