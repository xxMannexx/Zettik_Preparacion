# Entregable Día 05 — OOP, herencia, polimorfismo y modelo de datos

## 1. Instancia vs clase

La clase `SesionVision` contiene un atributo de clase (`sistema`) y atributos de instancia (`nombre` y `detecciones`).

```python
class SesionVision:
    sistema = "VizionarIA"

    def __init__(self, nombre):
        self.nombre = nombre
        self.detecciones = []
```

`__dict__` permite comprobar dónde vive cada dato. `sesion_a.__dict__` y `sesion_b.__dict__` contienen datos independientes de cada instancia. En cambio, `SesionVision.__dict__["sistema"]` pertenece al espacio de nombres de la clase y es compartido.

Además, al agregar un elemento a `sesion_a.detecciones`, la lista de `sesion_b` permanece vacía, demostrando que los datos de instancia son independientes.

## 2. Los tres métodos

La clase `Deteccion` demuestra los tres tipos:

```python
def describir(self):
    ...

@classmethod
def desde_porcentaje(cls, objeto, porcentaje):
    ...

@staticmethod
def confianza_valida(confianza):
    ...
```

`describir` es de instancia porque usa `self`.

`desde_porcentaje` es de clase porque recibe `cls` y actúa como fábrica alternativa.

`confianza_valida` es estático porque no necesita ni la instancia ni la clase.

También se verifica que:

```python
d.describir()
Deteccion.describir(d)
```

son llamadas equivalentes respecto a la vinculación de `self`.

## 3. Herencia y MRO

`DetectorPersona` hereda de `Detector`, reutiliza la inicialización mediante `super()` y sobrescribe `detectar()`.

```python
class DetectorPersona(Detector):
    def __init__(self, nombre, reconocimiento_facial=False):
        super().__init__(nombre)
```

El método sobrescrito puede extender la versión heredada:

```python
def detectar(self):
    base = super().detectar()
    return f"{base} -> persona"
```

El MRO se inspecciona con:

```python
DetectorPersona.__mro__
```

Ese orden determina dónde busca Python los métodos y a qué implementación avanza `super()`.

## 4. Polimorfismo por duck typing

`FiltroUmbral` y `Formateador` no heredan de una base común, pero ambos implementan `procesar()`.

La función:

```python
def ejecutar(procesadores, dato):
    resultado = dato
    for procesador in procesadores:
        resultado = procesador.procesar(resultado)
    return resultado
```

funciona con ambos porque Python no exige una clase base concreta: exige el comportamiento esperado.

Eso es duck typing.

## 5. Modelo de datos y `@dataclass`

`RegionManual` implementa manualmente:

- `__init__`
- `__repr__`
- `__eq__`
- `__iter__`

Con `__iter__`, la región puede recorrerse o convertirse a lista.

La misma estructura se reescribe con:

```python
@dataclass
class Region:
    x: int
    y: int
    ancho: int
    alto: int
```

`@dataclass` genera automáticamente `__init__`, `__repr__` y `__eq__` a partir de los atributos declarados. Solo se añade manualmente `__iter__` y `__post_init__` para validación.

El contraste muestra que una dataclass elimina código repetitivo sin impedir agregar comportamiento propio.

## Conclusión

El día integra clases, instancias, métodos, herencia, MRO, duck typing y métodos especiales.

Las clases permiten modelar estado y comportamiento; la herencia reutiliza y especializa; el polimorfismo desacopla el código del tipo concreto; y el modelo de datos permite que objetos propios funcionen con la sintaxis normal de Python.

`@dataclass` reduce el código repetitivo cuando una clase existe principalmente para representar datos.

## Script

El código completo ejecutable está en `demo_oop.py`.
