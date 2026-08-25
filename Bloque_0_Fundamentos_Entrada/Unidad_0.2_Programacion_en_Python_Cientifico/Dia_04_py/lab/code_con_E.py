## with es la manera reusmida de un try except

def procesar(f):
    pass

with open("datos.txt") as f:  ## Abre el archivo y lo cerrara de manera segura llamndo a metodos de abrir y cerrar recursos sin dejar corrupciones
    procesar(f)

## Equivale
f = open("datos.txt").__enter__() ## Adquiere el recurso

try:
    procesar(f)
finally:
    f.__enter__()  ## Libera el recurso, Siempre con finally ya que esto siempre ocurre

## Hacer observable la garantía.
class Recurso:
    def __enter__(self):
        print("Recurso adquirido")
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Recurso finalizado")
        return False ## Hace que se propague la excepcion

print("Casoo 1: sin excepcion")
with Recurso():
    print("Usando")

print("Caso 2: con excepcion dentro del with")
try:
    with Recurso():
        print(" Usando")
        raise ValueError("error dentro del with")
except ValueError as e:
    print("   Excepcion manejada fuera")
