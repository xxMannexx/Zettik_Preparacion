class BufferFotogramas:
    """Buffer de fotogramas: iterable (Día 3) y context manager (Día 4)."""

    def __init__(self, fuente):
        self.fuente = fuente
        self.fotogramas = []
        self.abierto = False

    # Protocolo de context manager (Día 4):
    def __enter__(self):
        self.abierto = True
        print(f"  [buffer] sesión abierta sobre {self.fuente}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.abierto = False
        print(f"  [buffer] sesión cerrada, {len(self.fotogramas)} fotogramas liberados")
        return False

    def capturar(self, fotograma):
        if not self.abierto:
            raise RuntimeError("buffer no abierto")  # excepción (Día 4)
        self.fotogramas.append(fotograma)

    # Protocolo de iteración (Día 3) y modelo de datos (Concepto E):
    def __iter__(self):
        return iter(self.fotogramas)

    def __len__(self):
        return len(self.fotogramas)

    def __getitem__(self, i):
        return self.fotogramas[i]

    def __repr__(self):
        return f"BufferFotogramas({self.fuente!r}, {len(self.fotogramas)} fotogramas)"


# Uso: gestionado con 'with' (libera siempre), iterable con 'for', indexable con []
with BufferFotogramas("/dev/video0") as buffer:
    for i in range(3):
        buffer.capturar(f"fotograma_{i}")
    print(f"  capturados: {len(buffer)}; primero: {buffer[0]}")  # len() y []
    for f in buffer:  # iterable
        print(f"    procesando {f}")
    print(f"  {buffer!r}")  # __repr__
# Al salir del with, la sesión se cierra automáticamente (Día 4)
