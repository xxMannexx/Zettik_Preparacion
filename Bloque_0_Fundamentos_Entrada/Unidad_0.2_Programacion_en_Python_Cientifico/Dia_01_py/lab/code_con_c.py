a = [1,2,3]
b = a  # vincula el nombre 'b' al MISMO objeto (no copia la lista)

b.append(4) # MUTA el objeto (le añade un elemento)
print(a is b)

print(a)
print(b)

## Contraste de reasignacion vs nuevo objeto

x = 10000
y = x # Mismo objeto que x

#y = y + 1  # Se reevalua el objeto y ya es diferente y +1 = 11, esto le da a y un objeto nuevo con el valor 11
y = y + 1 - 1 # Aunque se reevalua genero el mismo valor por lo cual no se asigna a otro objeto esto solo por optimizacion
print(id(y))
print(id(x))
