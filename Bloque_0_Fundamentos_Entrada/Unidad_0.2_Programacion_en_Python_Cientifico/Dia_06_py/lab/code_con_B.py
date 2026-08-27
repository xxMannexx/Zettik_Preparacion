def area_rectangulo(ancho : float, alto: float) -> float:
    return ancho * alto

resultado: float = area_rectangulo("10", 20)
print(resultado)

## Al ejecutar: mypy code_con_B.py da como resultado:
## code_con_B.py:4: error: Argument 1 to "area_rectangulo" has incompatible type "str"; expected "float"  [arg-type]
##Found 1 error in 1 file (checked 1 source file)

## No es que falle en ejecucion se esta usando un flujo de tipado gradual donde se ve donde no esta siendo coherente la anotacion con el uso

