class Conexion():
    def __enter__(self):
        print("Conectado"); return self
    def __exit__(self, *args):
        print("Desconectado"); return False

try:
    with Conexion() :
        raise ValueError("Fallo")
except ValueError:
    print("Manejado")         ### "desconectado" se imprime ANTES, pese al fallo, garantiza la liberacion aunque fallo evitancdo corrupciones