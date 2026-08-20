x = [1,2,3]

print(id(x)) # un entero: la identidad (direccion) del objeto lista

print(type(x)) # <class 'list'>: el tipo

print(x)

# 'is' compara identidad; '==' compara valor

a = [1,2]
b = [1,2]

print(a == b) # True: mismo VALOR (contienen lo mismo)
print(a is b) # False: distinta IDENTIDAD (son dos objetos diferentes)

c = a

print(a is c)  # True: MISMA identidad (c y a referencian el mismo objeto)