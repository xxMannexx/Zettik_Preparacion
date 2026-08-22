import functools

def registrar(f):
    @functools.wraps(f)
    def envoltura(*args, **kwargs):
        print(f"Llamando a {f.__name__}")
        return f(*args, **kwargs)
    return envoltura

@registrar
def multiplicar(valor1, valor2):
    return valor1 * valor2

print(multiplicar(10,20))
print(multiplicar.__name__)