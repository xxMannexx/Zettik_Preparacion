def saludar(nombre):
    return f"Hola {nombre}"

alias = saludar
registro = [saludar,len,str.upper]

print(alias("Ana"))
print(registro[0]("Eva"))