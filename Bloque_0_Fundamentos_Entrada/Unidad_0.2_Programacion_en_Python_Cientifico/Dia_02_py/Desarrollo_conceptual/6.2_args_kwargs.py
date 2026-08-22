def inspeccionar(*args,**kwargs):
    print("Posicionales (tupla): ", args )
    print("Palabras clave (diccionario): ", kwargs )
    
inspeccionar(1,2,3,4,5,modo="rapido", nivel=3)