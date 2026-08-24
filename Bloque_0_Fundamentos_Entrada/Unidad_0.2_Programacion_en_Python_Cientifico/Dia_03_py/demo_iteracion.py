## 1.	Protocolo manual: la reproducción de un bucle for con iter()/next(), mostrando el papel de StopIteration.
import sys

import itertools

lista = [10,20,30]
iteracion = iter(lista)  ## El for primero cra un iterador de los datos
while True:              ## Iniciamos el bucle
    try:
        print(next(iteracion))      ## Imprimimos el siguiente dato disponible del iterador
    except StopIteration:           ## Una vez agotados los datos del iterdor el for para
        break

## 2.	Agotamiento: la demostración de que un generador se consume una sola vez, frente a una lista que admite varios recorridos.


## Creamos un generador

numeros_pares = (x for x in range(100) if x % 2 == 0) ## Expresion generadora
numeros_parlista = [x for x in range(100) if x % 2 == 0] ## Comprension de lista

print(f"Primera pasada generador: {sum(numeros_pares)}") ## Un ejemplo de consumo es la suma de todos sus elementos
print(f"Primera pasada lista: {sum(numeros_parlista)}") ## Consumimos un iterador de tantos que puede generar una lista

## Segundo consumo
print(f"Segunda pasada generador: {sum(numeros_pares)}")
print(f"Segunda pasada lista: {sum(numeros_parlista)}")

## 3.	Generador con estado: un generador (Fibonacci, lotes, o similar) con la explicación de la suspensión y reanudación.

def cuenta_regresiva(n):
    print("Iniciando")
    while n >= 1:
        yield n
        n -= 1
        print("Reanudando despues del valor anterior" if n > 0 else "Finalizado")

g = cuenta_regresiva(10)
for n in g:
    print(n)

## 4.	Pereza: la demostración de que un flujo infinito es procesable con itertools.islice, y el contraste de memoria entre una comprensión de lista y una expresión generadora con sys.getsizeof.

def desde_n(num):
    sumador = 0
    while True:
        yield num + sumador
        sumador += 1

generador = desde_n(100)
print(list(itertools.islice(generador, 5)))
## Comparacion de size

print(sys.getsizeof(numeros_pares))
print(sys.getsizeof(numeros_parlista))

## 5.	Pipeline: un pipeline de generadores encadenados que procese datos sin materializar resultados intermedios, verificando que es perezoso antes de consumirlo.

datos = [x for x in range(100)]

def solo_pares(iterable):
    for i in iterable:
        if i % 2 == 0:
            yield i

def potencia(flujo):
    for i in flujo:
        yield i**2

pipeline = potencia(solo_pares(datos))
print(type(pipeline).__name__)
print(list(pipeline))

