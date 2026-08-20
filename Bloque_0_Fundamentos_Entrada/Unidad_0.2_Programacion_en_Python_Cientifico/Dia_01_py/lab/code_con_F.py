## Demostrar el tipado dinamico de Python

x = 10 ##  x referencia un int
x = "Diez" ## x ahora referencia un str: válido (el nombre no tiene tipo)
x = [1, 2]      # x ahora referencia una list: válido

## Demostrar el tipado fuerte de python

print(1 + "2") # TypeError: unsupported operand type(s) for +: 'int' and 'str'

# La conversión, si se desea, debe ser EXPLÍCITA:
print(1 + int("2")) # 3   (conversión explícita de str a int)
print(str(1) + "2") # "12" (conversión explícita de int a str)
