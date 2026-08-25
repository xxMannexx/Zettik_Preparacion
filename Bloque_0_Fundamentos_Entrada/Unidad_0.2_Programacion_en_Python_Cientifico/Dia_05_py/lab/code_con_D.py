class Perro:
    def sonido(self): return "Guau"

class Gato:
    def sonido(self): return "Miau"

class Pato:
    def sonido(self): return "Cuac"

def hacer_sonar(*animales):     # función POLIMÓRFICA: no conoce los tipos
    for animal in animales:
        print(animal.sonido())  # funciona con cualquier objeto que tenga 'sonido'

hacer_sonar(Perro(), Gato(), Pato())
# Las tres clases NO comparten una base común; basta con que todas tengan 'sonido'.