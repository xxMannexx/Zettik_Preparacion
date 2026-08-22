def crear_contador():
    n = 0  ## VARIABLE LOCAL

    def incrementar():
        nonlocal n           ## Declara que 'n' es de ambito envolvente
        n += 1
        return n
    return incrementar        ## Devuelve la funcion interna, cada pasada debido al closure recordara el ultimo valor de n

contador = crear_contador()
print(contador(), contador())
print(contador(), contador())  ## Se demuestra el closure


## Inspeccionar el closure
print(contador.__closure__)               # una tupla de celdas (cells)
print(contador.__closure__[0].cell_contents)   # el valor actual de 'n' capturado
# Esto hace observable el mecanismo: la función LLEVA consigo las variables capturadas.

## Closure sin estado mutable

def crear_multiplicador(factor):
    def multiplicar(x):
        return x * factor
    return multiplicar

doble = crear_multiplicador(2)
triple = crear_multiplicador(3)
print(doble(10),doble(5), triple(10))