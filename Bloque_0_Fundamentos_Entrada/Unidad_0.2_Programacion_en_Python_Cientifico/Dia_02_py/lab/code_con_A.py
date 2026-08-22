def saludar(nombre):
    return f"Hola {nombre}"

otro = saludar ## Aliasing: esto cre otra referencia de nombra a la funcion

print(otro is saludar) ## comprueba que estan bajo la misma identidad

print(otro("Ana")) ## Se invoca la funcion saludar sobre su otro nombre


## Funciones anonimas (cuando necesitas una funcion chica y de un solo uso)

cuadrado = lambda x: x ** 2 ## Equivale a def cuadrado(x): return x ** 2
print(cuadrado(5))

print(f"Las funciones anonimas tambien generan un objeto tipo: {type(cuadrado).__name__}")

# 'lambda' produce un objeto función; aquí se le ha dado el nombre 'cuadrado',
# pero su uso habitual es pasarlo directamente como argumento


## Las funciones sl ser objetos se pueden tratar como datos cualquiera

def doblar(x): return x * 2
def negar(x): return -x

### Almacenar funciones en una estructura de datos: esto demuestra que son objetos de primera clase
operaciones = {"doblar": doblar, "negar": negar}
print(operaciones["doblar"](10)) ## Busca la funcion y se invoca con el parametro


# Pasar una función como argumento (orden superior)
def aplicar_funcion(funcion,valor):
    return funcion(valor)

print(aplicar_funcion(doblar,5))