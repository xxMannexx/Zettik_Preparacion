import logging

## Configuaracion (solo una vez al inico del programa)

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s", # formato estructurado
)

logger = logging.getLogger(__name__) ## Solo un logger por modulo

def procesar(fotograma:str) -> None:
    logger.debug("Entrando a procesar(%s)", fotograma)  # DEBUG: no se muestra (umbral INFO)
    logger.info("procesando(%s)", fotograma)            # INFO: se muestra
    if not fotograma:
        logger.error("No se puede procesar(%s)", fotograma, "Esta vacio")       # ERROR: se muestra
        return
    logger.info("fotograma procesado(%s)", fotograma)

procesar("frame_001") # (el mensaje DEBUG no aparece, por el umbral; cambiar a level=DEBUG lo mostraría)


## Depuracion

def calcular(datos:list[int]) -> int:
    total = 0
    for x in datos:
        breakpoint()
        total += x
    return total
# En la sesión de pdb: p x (imprime x), p total, n (siguiente línea), c (continuar), q (salir)

calcular([10,20,30])