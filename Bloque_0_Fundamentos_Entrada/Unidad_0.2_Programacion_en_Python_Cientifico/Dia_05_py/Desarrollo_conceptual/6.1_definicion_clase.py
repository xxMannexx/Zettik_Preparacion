class Vector:                  ## Creamos la clase con atributos de instancia
    def __init__(self, x, y):
        self.x = x
        self.y = y

v = Vector(3, 4)
print(v.x)
print(v.y)
print(v.__dict__)  ## Muestra el diccionario de nombres con sus valores