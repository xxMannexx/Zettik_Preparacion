def mutar(argumento):
    argumento.append(99) # MUTA el objeto compartido (efecto visible al llamador)

def reasignar(argumento):
     argumento = [0,0,0] # REVINCULA el parámetro local (sin efecto al llamador <efecto local>)

datos = [1,2,3]
mutar(datos)
print(datos)  # [1, 2, 3, 99]  <- la mutación SÍ afectó a 'datos'# [1, 2, 3, 99]  <- la mutación SÍ afectó a 'datos'

datos = [1,2,3]
reasignar(datos)
print(datos)  # [1, 2, 3]  <- la reasignación NO afectó a 'datos'


def inspecionar(p):
    print("Dentro, antes:", id(p)) # misma identidad que el argumento (mismo objeto)

    p = p + [1] # reasigna: objeto nuevo

    print("Dentro, despues:", id(p)) # identidad distinta (otro objeto, local)

datos = [1,2,3]
print("Fuera: ",id(datos))
inspecionar(datos)
print("Fuera despues estar dentro demostrando que no hay mutabilidad si hay reasignacion: ",id(datos))


