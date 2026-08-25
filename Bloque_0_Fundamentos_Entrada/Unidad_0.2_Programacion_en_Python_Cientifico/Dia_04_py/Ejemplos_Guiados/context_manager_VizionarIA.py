from contextlib import contextmanager

## Forma 1; basada en clase (control completo)
class SesionCamara():
    def __init__(self,dispositivo):
        self.dispositivo = dispositivo
    def __enter__(self):
        print(f"[camara {self.dispositivo}] abierta")
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"[camara {self.dispositivo}] ha sido liberada") ##Garantizado
        return False
    def captura(self):
        return ("fotograma")

## Forma 2 basado en un generador concisa
@contextmanager
def sesion_camara(dispositivo):
    print(f"[camara {dispositivo}] abierta")
    try:
        yield dispositivo
    finally:
        print(f"[camara {dispositivo}] ha sido liberada]")

print("Uso normal (Clase)")
with SesionCamara("/dev/video0") as camara:
    print("capturado: ", camara.captura())

print("Con error (generador)): la cámara se libera pese al fallo")
try:
    with SesionCamara("/dev/video0") as cam:
        raise RuntimeError("Fallo la captura")
except RuntimeError:
    print("Error manejado")
