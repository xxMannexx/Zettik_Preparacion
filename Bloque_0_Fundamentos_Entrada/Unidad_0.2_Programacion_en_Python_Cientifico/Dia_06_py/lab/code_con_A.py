def doblar(x: int) -> int:
    return x * 2

print(doblar(5)) # 10
print(doblar("ab"))          # 'abab'  <- ¡funciona! Python NO impone la anotación 'int'
print(doblar.__annotations__)   # {'x': <class 'int'>, 'return': <class 'int'>}

## Las anotaciones on simple documentacion que el interprete almacena, pero no usa, su uso depende de herramientas fuera de para detectar usos incorrectos
print(doblar.__defaults__)
print(doblar.__kwdefaults__)

## SINTAXIS Y USO COMPLETO CON OPCIONALES

from typing import Optional

def saludar(nombre : str, veces : int = 1) -> str:  ## Anotamos parametros y retorno
    return f"Hola {nombre}!" * veces

def buscar(items : list[int], objetivo : int) -> Optional[int]: ## Generico y opcional
    """Devuelve el índice del objetivo, o None si no está."""
    for ind,obj in enumerate(items):
        if obj == objetivo:
            return ind
    return None       # None es válido: el retorno es Optional[int]

# Variables y estructuras:
puntuaciones: dict[str, float] = {"a": 0.9, "b": 0.7}
coordenadas: tuple[int,int] = (10, 20)
identificador: int | None = None                          # sintaxis moderna de Optional (3.10+)


