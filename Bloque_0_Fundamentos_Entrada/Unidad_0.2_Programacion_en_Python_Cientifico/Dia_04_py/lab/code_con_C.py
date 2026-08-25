try:
    resultado = 10 / 0
except ArithmeticError as e:
    print(f"Error aritmetico: {type(e).__name__}")

    ## Error arimetico de subclase ZeroDivisionError

