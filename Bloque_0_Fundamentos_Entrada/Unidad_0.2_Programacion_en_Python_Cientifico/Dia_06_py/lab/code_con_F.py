import cProfile

def lento():
    return sum(i**2 for i in range(10_000_000))

def rapido():
    return [x for x in range(100)]

def programa():
    for _ in range(5):
        lento()
        rapido()

cProfile.run("programa()")
# Reporta el tiempo por función: revela que 'lento' consume casi todo el tiempo,
# mientras 'rapido' es insignificante. La optimización debe dirigirse a 'lento'.

##timeit, para fragmentos chicos
import timeit
t = timeit.timeit("sum(range(1000000))", number=10000)
print(f"tiempo: {t:.4f} segundos")

