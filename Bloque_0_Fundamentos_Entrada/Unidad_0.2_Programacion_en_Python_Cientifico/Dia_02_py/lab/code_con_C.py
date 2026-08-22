x = 10 ## Global

def f():
    x = 5 ## Variable local no modifica la global
    print(x)

f()

print(x) ## 10: la global nunca fue modificada

## Afectacion a la variable global

contador = 0


def incrementar():
    global contador
    contador += 1

incrementar(); incrementar()
print(contador)