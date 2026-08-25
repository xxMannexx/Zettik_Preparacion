class Detecion:
    def __init__(self,objeto,confianza):
        self.objeto = objeto
        self.confianza = confianza

d1 = Detecion(objeto="Persona",confianza=1)
print(d1.objeto)
print(d1.confianza)
print(type(d1).__name__)        ## Da el tipo de objeto en este caso Detecccion
print(d1.__dict__)             ## Diccionario que se crea a partir de el espacio de nombres de la clase

## Demostrar la distincio de atributo de clase y de instancia

class Contenedor:
    elementos = []                   ## No se crea con self, es para todos, no por instancia
    def agregar(self,x):
        self.elementos.append(x)        ## Aqui si cada instancia puede hacer esto independientemente

a = Contenedor(); b = Contenedor()
a.agregar(10)
print(b.elementos)                      ## Aunque se agrego en a, b lo puede hacer debido a que es de clases en general

## Con atributo de instancia seria asi:

class Contenedor:
    def __init__(self):
        self.elementos = []         # atributo de INSTANCIA: uno NUEVO por instancia
    def agregar(self, x):
        self.elementos.append(x)
a = Contenedor(); b = Contenedor()
a.agregar(1)
print(b.elementos)                  # []  <- correcto: b tiene su propia lista
