class Punto:
    def __init__(self, x,y):
        self.x, self.y = x,y

    def distancia_al_origen(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

## Creamos el objeto
p = Punto(3,4)
print(p.distancia_al_origen()) ## Accedemos desde el objeto python liga automatico self

## Equivale a:

print(Punto.distancia_al_origen(p))


## Los tres tipos de metodos

class Temperatura:

    escala_por_defecto = "Celsius"   ## Atributo de clase

    def __init__(self, grados):
        self.grados = grados

    def describir(self):            # MÉTODO DE INSTANCIA: opera sobre self
        return f'"{self.grados}° {Temperatura.escala_por_defecto}'

    @classmethod
    def desde_farenheit(cls,f):     # MÉTODO DE CLASE: fábrica alternativa
        return cls((f - 32) * 5 / 9)        # 'cls' es la clase; crea una instancia

    @staticmethod
    def es_valida(grados):                  # MÉTODO ESTÁTICO: sin self ni cls
        return -273.15 <= grados            # función relacionada, sin estado

t1 = Temperatura(25)
print(t1.describir())                         # 25° Celsius
t2 = Temperatura.desde_fahrenheit(98.6)       # fábrica: crea desde Fahrenheit
print(round(t2.grados, 1))                    # 37.0
print(Temperatura.es_valida(-300))            # False



