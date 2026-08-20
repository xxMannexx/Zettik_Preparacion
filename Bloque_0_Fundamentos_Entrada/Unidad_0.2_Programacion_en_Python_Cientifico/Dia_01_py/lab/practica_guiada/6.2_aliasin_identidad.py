a = [1,2,3]
b = a ## Aliasing por referencia de nombre
c = a.copy() ## Copia independiente no apunta al mismo objeto

print(a is b) ## Da True debido a que son el mismo objeto
print(a is c) ## Da false mismos valores pero diferente objeto es una copia

print(a == c) ## True debido a que contienen los mismos valores

b.append(4); print(a) ## Muestra el aliasing de manera explicita los dos nombres apuntan a un objeto mutable

c.append(9); print(a) ## La mutacion de c no implica el objeto de a debido a que son dos diferentes


