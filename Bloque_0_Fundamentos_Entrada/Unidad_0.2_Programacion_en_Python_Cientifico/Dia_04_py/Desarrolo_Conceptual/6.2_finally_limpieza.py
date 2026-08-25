## finally se ejecuta siempre es ideal para liberar recursos

def leer():
    archivo = None
    try:
        archivo = open("texto.txt", "w")
        archivo.write("texto")
        return "ok"
    finally:
        if archivo: archivo.close()
        print("Limpieza lista")

print(leer())