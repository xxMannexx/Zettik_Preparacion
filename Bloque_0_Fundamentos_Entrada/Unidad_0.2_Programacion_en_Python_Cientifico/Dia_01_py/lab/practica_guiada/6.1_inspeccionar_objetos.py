for obj in [42, "texto", [1,2], (3,4), {"k": "v"}]:
    ## Su objetivo es mostrar de forma limpia y alineada tres propiedades clave de cualquier objeto: su representación textual, su tipo de datos y su dirección de memoria.
    print(f"Valor = {obj!r:15} Tipo = {type(obj).__name__:8} id = {id(obj)}")

