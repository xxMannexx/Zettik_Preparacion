# Posicionales y de palabra clave; valor por omisión:
def conectar(host, puerto=8080, timeout=30):
    return f"{host}:{puerto} (timeout={timeout})"


print(conectar("servidor"))  # 'servidor:8080 (timeout=30)'
print(conectar("servidor", 9090))  # posicional: puerto=9090
print(conectar("servidor", timeout=60))  # palabra clave: salta puerto, fija timeout
print(conectar(puerto=80, host="web"))  # todos por palabra clave, orden libre


# *args: número arbitrario de posicionales (se recogen en una tupla)
def sumar_todos(*numeros):
    return sum(numeros)  # 'numeros' es una tupla


print(sumar_todos(1, 2, 3, 4))  # 10


# **kwargs: número arbitrario de palabra clave (se recogen en un diccionario)
def configurar(**opciones):
    return opciones  # 'opciones' es un dict


print(configurar(modo="rapido", nivel=3))  # {'modo': 'rapido', 'nivel': 3}


# Combinados, en el orden canónico: posicionales, *args, palabra clave, **kwargs
def registro(evento, *detalles, nivel="INFO", **metadatos):
    return (evento, detalles, nivel, metadatos)


print(registro("inicio", "cpu", "memoria", nivel="DEBUG", usuario="ana"))
# ('inicio', ('cpu', 'memoria'), 'DEBUG', {'usuario': 'ana'})

## Los operadores * y ** también desempaquetan en la llamada: f(*lista) pasa los elementos de la lista como argumentos posicionales; f(**diccionario) los pasa como argumentos de palabra clave.

args = [1, 2, 3]
sumar_todos(*args)                             # equivale a sumar_todos(1, 2, 3)
opciones = {"modo": "lento", "nivel": 5}
configurar(**opciones)
