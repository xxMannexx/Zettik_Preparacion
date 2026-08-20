x = 1; print(type(x))        # int
x = "a"; print(type(x))      # str: el nombre no tiene tipo (dinámico)

try:
    resultado = 1 + "2"       # fuerte: rechaza la operación
except TypeError as e:
    print("TypeError:", e)
print(1 + int("2"))           # 3: conversión explícita
