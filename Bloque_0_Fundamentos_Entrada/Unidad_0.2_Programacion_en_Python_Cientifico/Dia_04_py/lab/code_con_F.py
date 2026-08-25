class GestorArchivo:
    def __init__(self, nombreArchivo, modo):
        self.nombreArchivo = nombreArchivo
        self.modo = modo
        self.archivo = None
    def __enter__(self):
        ##Obtenemos
        self.archivo = open(self.nombreArchivo, self.modo)

        return self.archivo  ## # lo que 'as' vincula
    def __exit__(self, exc_type, exc_val, exc_tb):
        ## Liberamos el archivo
        self.archivo.close()
        return False ## Garantiza que se propague cualquier excepcion

with GestorArchivo("archivo.txt", "w") as archivo:
    archivo.write("contenido")


## Forma basada en generador
from contextlib import contextmanager


@contextmanager
def gestor_recurso(nombre):
    print(f"  adquiriendo {nombre}")  # código ANTES del yield = __enter__
    recurso = f"<{nombre}>"
    try:
        yield recurso  # lo que 'with ... as' vincula; suspende aquí
    finally:
        print(f"  liberando {nombre}")  # código DESPUÉS del yield = __exit__ (garantizado)


with gestor_recurso("conexión") as r:
    print(f"  usando {r}")
# adquiriendo conexión / usando <conexión> / liberando conexión
