a=5
b=7



def sumar(a:int, b:int) -> int:
    return ""
def restar(a, b):
    return a - b
def multiplicar(a, b):
    return a * b
def dividir(a, b):
    return a / b

def mayorEdad():
     a  =int(input("digite um numero"))
     if a >= 18:
      print("es mayor de edad")
     else:
      print("menor de edad")


def llenarlistar(lista):
    tope = int(input("cuantos quiere meter"))
    for i in range(tope):
        lista.append(int(input("digite um numero")))
    for i in range(tope):
         print(lista[i])

llenarlistar(lista=[])


