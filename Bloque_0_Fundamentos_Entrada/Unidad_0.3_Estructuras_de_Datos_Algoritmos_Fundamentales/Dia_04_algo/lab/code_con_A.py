def hash_simple(clave : str, m : int) -> int:
    """Funcion hash didactica: suma los codigos de los caracteres, modulo m."""
    total  = 0
    for c in clave:
        total += ord(c)
    return total % m

m = 1000
print(hash_simple('Ana', m))
print(hash_simple('Ana', m))
print(hash_simple('Luis', m))