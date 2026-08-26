from dataclasses import dataclass

def seccion(titulo):
    print(f"\n{'=' * 72}\n{titulo}\n{'=' * 72}")

seccion("1. Instancia vs clase")

class SesionVision:
    sistema = "VizionarIA"

    def __init__(self, nombre):
        self.nombre = nombre
        self.detecciones = []

sesion_a = SesionVision("camara_frontal")
sesion_b = SesionVision("camara_trasera")
sesion_a.detecciones.append("persona")

print("sesion_a.__dict__:", sesion_a.__dict__)
print("sesion_b.__dict__:", sesion_b.__dict__)
print("Atributo de clase:", SesionVision.__dict__["sistema"])
print("Compartido por ambas:", sesion_a.sistema, sesion_b.sistema)
print("Listas independientes:", sesion_a.detecciones, sesion_b.detecciones)

seccion("2. Método de instancia, de clase y estático")

class Deteccion:
    fuente = "modelo_base"

    def __init__(self, objeto, confianza):
        if not self.confianza_valida(confianza):
            raise ValueError("confianza debe estar entre 0 y 1")
        self.objeto = objeto
        self.confianza = confianza

    def describir(self):
        return f"{self.objeto}: {self.confianza:.2f}"

    @classmethod
    def desde_porcentaje(cls, objeto, porcentaje):
        return cls(objeto, porcentaje / 100)

    @staticmethod
    def confianza_valida(confianza):
        return 0 <= confianza <= 1

d = Deteccion("persona", 0.92)
d2 = Deteccion.desde_porcentaje("coche", 87)

print("Instancia:", d.describir())
print("Fábrica @classmethod:", d2.describir())
print("Utilidad @staticmethod:", Deteccion.confianza_valida(0.75))
print("obj.m():", d.describir())
print("Clase.m(obj):", Deteccion.describir(d))

seccion("3. Herencia, super(), sobrescritura y MRO")

class Detector:
    def __init__(self, nombre):
        self.nombre = nombre

    def detectar(self):
        return f"{self.nombre}: detección genérica"

class DetectorPersona(Detector):
    def __init__(self, nombre, reconocimiento_facial=False):
        super().__init__(nombre)
        self.reconocimiento_facial = reconocimiento_facial

    def detectar(self):
        base = super().detectar()
        return f"{base} -> persona"

    def reconocer_rostro(self):
        if not self.reconocimiento_facial:
            return "reconocimiento facial desactivado"
        return "rostro procesado"

detector_persona = DetectorPersona("detector_personas", True)
print(detector_persona.detectar())
print(detector_persona.reconocer_rostro())
print("MRO:", [clase.__name__ for clase in DetectorPersona.__mro__])

seccion("4. Polimorfismo por duck typing")

class FiltroUmbral:
    def procesar(self, dato):
        objeto, confianza = dato
        return dato if confianza >= 0.70 else None

class Formateador:
    def procesar(self, dato):
        if dato is None:
            return "descartado"
        objeto, confianza = dato
        return f"{objeto} ({confianza:.0%})"

def ejecutar(procesadores, dato):
    resultado = dato
    for procesador in procesadores:
        resultado = procesador.procesar(resultado)
    return resultado

pipeline = [FiltroUmbral(), Formateador()]
print(ejecutar(pipeline, ("persona", 0.91)))
print(ejecutar(pipeline, ("objeto_dudoso", 0.42)))

seccion("5. Modelo de datos y dataclass")

class RegionManual:
    def __init__(self, x, y, ancho, alto):
        if ancho < 0 or alto < 0:
            raise ValueError("ancho y alto no pueden ser negativos")
        self.x = x
        self.y = y
        self.ancho = ancho
        self.alto = alto

    def __repr__(self):
        return f"RegionManual(x={self.x}, y={self.y}, ancho={self.ancho}, alto={self.alto})"

    def __eq__(self, otro):
        if not isinstance(otro, RegionManual):
            return NotImplemented
        return (self.x, self.y, self.ancho, self.alto) == (otro.x, otro.y, otro.ancho, otro.alto)

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.ancho
        yield self.alto

@dataclass
class Region:
    x: int
    y: int
    ancho: int
    alto: int

    def __post_init__(self):
        if self.ancho < 0 or self.alto < 0:
            raise ValueError("ancho y alto no pueden ser negativos")

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.ancho
        yield self.alto

manual_1 = RegionManual(10, 20, 100, 80)
manual_2 = RegionManual(10, 20, 100, 80)
data_1 = Region(10, 20, 100, 80)
data_2 = Region(10, 20, 100, 80)

print("Manual repr:", manual_1)
print("Manual eq:", manual_1 == manual_2)
print("Manual iterable:", list(manual_1))
print("Dataclass repr:", data_1)
print("Dataclass eq:", data_1 == data_2)
print("Dataclass iterable:", list(data_1))
