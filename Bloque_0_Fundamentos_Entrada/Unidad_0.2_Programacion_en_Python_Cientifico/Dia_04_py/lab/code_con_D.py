# class ConfiguracionError(Exception):
#     pass
#
#
# def cargar_config(texto):
#     try:
#         return int(texto)
#     ## Puede lanzar ValueError
#     except ValueError as e:
# # Transformar el error de bajo nivel en uno de dominio, SIN perder la causa:
#         raise ConfiguracionError(f"configuracion invalida: {texto!r}") from e
#
# cargar_config("hola")

## Relanzar una excepcion

import logging
def operacion_critica():
    try:
        return 10 / 0
    except ZeroDivisionError:
        logging.error("fallo en operación crítica")   # registrar antes de propagar
        raise                                          # re-lanza la MISMA excepción (sin perderla)
# La excepción se registra y luego se propaga al llamador para que decida.
operacion_critica()