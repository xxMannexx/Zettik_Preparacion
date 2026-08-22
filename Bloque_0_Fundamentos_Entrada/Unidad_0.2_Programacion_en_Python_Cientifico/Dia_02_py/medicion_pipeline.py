import functools, time


def cronometrar(funcion):
    @functools.wraps(funcion)
    def envoltura(*args, **kwargs):
        inicio = time.perf_counter()
        resultado = funcion(*args, **kwargs)
        ms = (time.perf_counter() - inicio) * 1000
        print(f"[perf] {funcion.__name__}: {ms:.3f} ms")
        return resultado

    return envoltura


@cronometrar
def detectar_objetos(num_pixeles):
    # simula el coste de procesar una imagen
    return sum(i * i for i in range(num_pixeles))


@cronometrar
def normalizar(valores):
    m = max(valores) if valores else 1
    return [v / m for v in valores]


print(detectar_objetos(500_000))  # imprime su latencia
print(normalizar([0.5, 0.8, 1.0, 0.3]))  # imprime su latencia
