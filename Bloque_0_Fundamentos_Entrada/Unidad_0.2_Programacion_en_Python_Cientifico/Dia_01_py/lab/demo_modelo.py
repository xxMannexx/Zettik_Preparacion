## 1.	Tripleta de objetos: la inspección con id() y type() de varios objetos, con la explicación de qué responde cada función.
import dis

for objeto in [2, (1,2,3), ['carro','mujer'],{"clave": "valor"}]:
    ## ID: mostrara la identidad el espacio en memoria, valor muestra de forma representativa el valor del objeto, Tipo muestra de manera correcta el tipo ligado al objeto en tiempo de ejecucionno s
    print(f"ID: {id(objeto):15} Valor: {repr(objeto):20} Tipo: {type(objeto).__name__:8}")

## 2.	Aliasing demostrado: la evidencia, con is e id(), de que la asignación comparte el objeto (mutable, observable) y de que la inmutabilidad hace la compartición inobservable, con la explicación del porqué.

##Prueba para tipo con mutabilidad
a = [5,7,9] ## Creamos el objeto principal
b = a ## Creamos una referencia extra por nombre

b.append(12); print(f"a = {a} y b = {b}"); ## Demostramos el cambio desde cualquier referencia (solo tipo mutable)

## Apuntan al mismo objeto
if a is b:
    print(f"\nTanto A como B apuntan al mismo objeto \nId de a: {id(a):18} Id de b: {id(b):18}")
else:
    print("\nNo apuntan al mismo objeto")

## Prueba de aliasing en tipos inmutables

x = 10 ## Creamos el objeto principal
y = x ## Creamos una referencia por nombre (aliasing)

if x is y:
    print(f"\nAqui apuntan al mismo objeto \nId de x: {id(x):18} Id de y: {id(y):18}")
else:
    print(f"\nNo apuntan al mismo objeto \nId de x: {id(x):18} Id de y: {id(y):18}")

## El aliasing no es observable explicitamente desde inmutables por que un cambio en una referencia causa la reasignacion, no hay mutacion in situ
y = y + 3 ## Genera un nuevo objeto mientras que x sigue intacto respeta inmutabilidad

if y is x:
    print(f"\nAqui tanto x como y apuntan al mismo objeto \nId de x: {id(x):18} Id de y: {id(y):18}")
else:
    print(f"\nAqui no apuntan al mismo objeto \nId de x: {id(x):18} Id de y: {id(y):18}")


## 3.	Paso de argumentos: una función que mute su argumento y otra que lo reasigne, mostrando con id() por qué una afecta al llamador y la otra no.

## Creamos una funcion capaz de mutar in situ siempre y cuando el objeto sea de tipo mutable
def mutable(argumento):
    argumento.append(5)
    return id(argumento)

## Creo la funcion que causa reasignacion de nombre a otro objeto
def reasignacion(argumento):
    argumento = [3,9,0]
    return id(argumento)

lista = [15,8,0,2]

print(f"\nID objeto principal: {id(lista):18} \nValores objeto principal: {lista}")
print(f"\nID objeto despues de pasarla por la funcion de mutabilidad: {mutable(lista):18} \nValores de el objeto principal: {repr(lista)}")
print(f"\nID objeto de la funcion reasignacion: {reasignacion(lista):18} \nValores de el objeto principal: {repr(lista)}")

## 4.	Argumento por omisión mutable: la demostración del defecto clásico y su corrección con el patrón None.

## Creo la funcion defectuosa
def agregar_defectuoso(argumento, listafuncion = []):
    listafuncion.append(argumento)
    return listafuncion

print(agregar_defectuoso(10))
print(agregar_defectuoso(11))
print(agregar_defectuoso(12))

def acumula_bien(x, acc=None):
    if acc is None: acc = []
    acc.append(x); return acc
print(acumula_bien(1), acumula_bien(2), acumula_bien(3))

## 5.	Tipado fuerte: tres operaciones que produzcan TypeError, con la conversión explícita correcta para cada una, y el bytecode de una función con dis.

## Primero genero 3 operaciones que producen TypeError
# print(1 + "3")
print(f"Correcion debe ser: {1 + int("3")}")
# print((1,2,3) + 5)
print(f"Correcion debe ser: {(1,2,3) + (5,)}")
#print(4 + [2])
print(f"Correccion debe ser: {[2] + [4.6]}")

dis.dis(acumula_bien)
