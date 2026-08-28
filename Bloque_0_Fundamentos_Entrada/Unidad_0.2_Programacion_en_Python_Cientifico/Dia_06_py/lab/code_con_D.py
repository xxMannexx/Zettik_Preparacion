def area_rectangulo(ancho : float, alto: float) -> float:
    if ancho < 0 or alto < 0:
        raise ValueError("Las dimensiones no pueden ser negativas")
    return ancho * alto

