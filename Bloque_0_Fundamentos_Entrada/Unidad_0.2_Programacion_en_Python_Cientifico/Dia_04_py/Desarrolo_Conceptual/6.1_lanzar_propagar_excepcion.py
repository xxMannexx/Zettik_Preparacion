## raise lanza, la excepcion se propaga hasta un manejador si no lo hay para el flujo

def validar(edad):
    if edad < 0:
        raise ValueError(f"Edad invalida: {edad}")  ## Obtiene la excepcion "propia"
    return edad

try:
    validar(-18)
except ValueError as e:                   ##Atrapa la excepcion y la muestra
    print(f"Capturado {e}")

