class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.siguiente = None

## Construimos cadena

a = Nodo("A")
b = Nodo("B")
c = Nodo("C")
d = Nodo("D")
elemento_medio = Nodo("Elemento medio")
elemento_nuevo = Nodo("Elemento nuevo")

a.siguiente = b
b.siguiente = elemento_medio
elemento_medio.siguiente = elemento_nuevo
elemento_nuevo.siguiente = c
c.siguiente = d

actual = a

while actual != None:
    print(actual.valor,end=" -> ")
    actual = actual.siguiente
print(
    "None"
)