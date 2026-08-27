## Protocol

## Creamos la interfaz estructural (que deben tener para ser "dibujables")
from typing import Protocol

class Dibujable(Protocol):
    def dibujar(self) -> str: pass

## Creamos una funcion polimorfica que acepta cualquier objeto con dibujar -> str

def renderizar(figura: Dibujable) -> None: pass


## Creamos la clase de donde saldra el objeto a usar con la funcion polimorfica, solo debe cumplir la estructura
class Circulo:
    def dibujar(self) -> str: return "Circulo"

renderizar(Circulo()) ## Es valido circulo tiene la misma estructura que un objeto dibujable


## la ABC, la alternativa nominal.

from abc import ABC, abstractmethod

class Detector(ABC):         # interfaz que EXIGE herencia
    @abstractmethod
    def detectar(self,fotograma: str) -> list[str]:  # método abstracto: las subclases DEBEN implementarlo
        pass

class DetectorPersonas(Detector):               # DEBE heredar de Detector
    def detectar(self,fotograma: str) -> list[str]:        # implementa el método abstracto
        return ["Persona"]

d = DetectorPersonas()                         # válido: implementa detectar()

# class Incompleto(Detector): pass
# Incompleto()  ->  TypeError: Can't instantiate abstract class Incompleto
#                   with abstract method detectar  (la ABC IMPIDE instanciarla)
