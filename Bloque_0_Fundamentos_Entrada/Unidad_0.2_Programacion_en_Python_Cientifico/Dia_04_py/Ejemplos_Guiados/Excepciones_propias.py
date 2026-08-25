## Creamos la clase padre


class ProcesamientoError(Exception):
    """Base de los errores del procesamiento"""

class FormatoError(ProcesamientoError):
    """El formato del dato es invalido"""

class RangoError(ProcesamientoError):
    """El valor esta fuera de rango"""
    def __init__(self, valor,minimo,maximo):
        self.valor = valor
        self.minimo = minimo
        self.maximo = maximo
        super().__init__(f"{valor} fuera de [{minimo},{maximo}]")


## Uso
def procesar(valor,minimo=0,maximo=100):
    if not isinstance(valor,(int,float)):
        raise FormatoError(f"Se esperaba un numero, no {type(valor).__name__}")
    if not (minimo <= valor <= maximo):
        raise RangoError(valor,minimo,maximo)
    return valor

## Captura especifica
try:
    procesar(123)
except RangoError as e:
    print(f"rango: {e} (valor: {e.valor})")


## Captura general de TODA la familia con la base:
for entrada in ["texto", 150, 50]:
    try:
        print(f"procesado: {procesar(entrada)}")
    except ProcesamientoError as e:           # captura FormatoError y RangoError
        print(f"error ({type(e).__name__}): {e}")
