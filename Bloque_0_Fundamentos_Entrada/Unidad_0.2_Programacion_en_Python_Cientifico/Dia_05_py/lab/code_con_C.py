class Animal:
    def __init__(self, nombre):
        self.nombre = nombre

    def describir(self,):
        return  f"{self.nombre} es un animal"

    def sonido(self):
        return f"..."

class Perro(Animal):    # Perro HEREDA de Animal
    def __init__(self, nombre,raza):
        super().__init__(nombre)     # invoca Animal.__init__ (extiende, no reemplaza)
        self.raza = raza # añade un atributo propio

    def sonido(self):      # SOBRESCRIBE el método heredado
        return "Guau"

p = Perro("Rez","Labrador")
print(p.describir())
print(p.sonido())
print(p.raza)


## Con herencia múltiple (una clase que hereda de varias), el MRO determina el orden de búsqueda. La linealización C3 garantiza un orden consistente: una clase siempre precede a sus bases, y se respeta el orden en que se listan las bases.

class A:
    def saludar(self): return "A"


class B(A):
    def saludar(self): return "B -> " + super().saludar()


class C(A):
    def saludar(self): return "C -> " + super().saludar()


class D(C, B):  # herencia múltiple (caso "diamante")
    def saludar(self): return "D -> " + super().saludar()


print(D().saludar())  # 'D -> B -> C -> A'
print([cls.__name__ for cls in D.__mro__])  # ['D', 'B', 'C', 'A', 'object']
