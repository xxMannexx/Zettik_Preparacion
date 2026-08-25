class AppError(Exception):   ##Creamos la clase padre dada de excepcion
    ## Logica de el error
    pass


class ErrorEntrada(AppError):  ## SubClase de AppError
    pass

try:
    raise ErrorEntrada("Entrada invalida")
except AppError as e:                   ## Captura la subclase obviamente la abarca el padre
    print(f"Error de la App: {e}")