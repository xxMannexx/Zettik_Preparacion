class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.siguiente = None

## Construimos cadena

a = Nodo("A")
b = Nodo("B")
c = Nodo("C")

a.siguiente = b
b.siguiente = c
## c.siguiente es None cumpliendo la regla

actual = a

while actual != None:
    print(actual.valor,end=" -> ")
    actual = actual.siguiente
print(
    "None"
)