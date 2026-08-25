# MANUAL: código repetitivo para una clase que solo agrupa datos
class DeteccionManual:
    def __init__(self, objeto, confianza, x, y):
        self.objeto = objeto
        self.confianza = confianza
        self.x = x
        self.y = y
    def __repr__(self):
        return f"DeteccionManual(objeto={self.objeto!r}, confianza={self.confianza}, x={self.x}, y={self.y})"
    def __eq__(self, otro):
        if not isinstance(otro, DeteccionManual):
            return NotImplemented
        return (self.objeto, self.confianza, self.x, self.y) == (otro.objeto, otro.confianza, otro.x, otro.y)


## Dataclass: generador de metodos automaticamente

from dataclasses import dataclass

@dataclass
class Deteccion:
    objeto: str         # anotación de tipo (Día 6)
    confianza: float
    x : int = 0
    y : int = 0         # valor por omisión


d1 = Deteccion("Persona",0.9,5,10)
d2 = Deteccion("Persona",0.9,5,10)
print(d1)       # Deteccion(objeto='persona', confianza=0.9, x=5, y=10)  (__repr__ generado)
print(d1 == d2)
# True  (__eq__ generado)

## Opciones utiles
from dataclasses import dataclass, field


@dataclass(frozen=True, order=True)  # inmutable y comparable
class Punto:
    x: int
    y: int


@dataclass
class Acumulador:
    valores: list = field(default_factory=list)  # valor por omisión mutable SEGURO
    # field(default_factory=list) crea una lista NUEVA por instancia,
    # evitando el defecto del valor por omisión mutable compartido (Día 1, Concepto A de hoy).
