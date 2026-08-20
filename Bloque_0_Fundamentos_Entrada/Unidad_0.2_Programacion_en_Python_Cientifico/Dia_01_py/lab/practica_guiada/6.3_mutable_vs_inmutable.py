# Inmutable: el aliasing no se manifiesta
t1 = (1, 2, 3);
t2 = t1

# t2[0] = 9  ->  TypeError: las tuplas no admiten asignación de elementos (inmutables)
t2 = t2 + (4,)  # crea una tupla nueva; t1 intacta
print(t1, t2)  # (1,2,3) (1,2,3,4)

# Mutable: el aliasing se manifiesta
l1 = [1, 2, 3];
l2 = l1
l2[0] = 9  # muta el objeto compartido
print(l1, l2)  # [9,2,3] [9,2,3]
