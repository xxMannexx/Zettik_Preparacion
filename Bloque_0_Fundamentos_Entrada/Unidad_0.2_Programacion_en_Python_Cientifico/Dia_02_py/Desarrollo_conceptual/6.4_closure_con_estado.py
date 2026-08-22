def acumulador():
    total = 0
    def agregar(x):
        nonlocal total
        total += x
        return total
    return agregar

acc = acumulador()
print(acc(10),acc(20),acc(30),acc(40))

print(acc.__closure__[0].cell_contents)