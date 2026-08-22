mensaje = "global"

def f():
    mensaje = "local"
    return mensaje

print(f(), mensaje)