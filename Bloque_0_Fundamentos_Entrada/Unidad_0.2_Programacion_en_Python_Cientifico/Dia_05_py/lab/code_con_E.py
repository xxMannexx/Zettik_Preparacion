class RegionInteres:
    """Una región rectangular en una imagen (modelo de datos integrado)."""

    def __init__(self, x, y, ancho, alto):
        self.x, self.y, self.ancho, self.alto = x, y, ancho, alto

    def __repr__(self):  # representación oficial (depuración)
        return f"RegionInteres({self.x}, {self.y}, {self.ancho}, {self.alto})"

    def __eq__(self, otro):  # igualdad con ==
        if not isinstance(otro, RegionInteres):
            return NotImplemented
        return (self.x, self.y, self.ancho, self.alto) == (otro.x, otro.y, otro.ancho, otro.alto)

    def __hash__(self):  # permite usarla en conjuntos / claves
        return hash((self.x, self.y, self.ancho, self.alto))

    def __len__(self):  # len() devuelve el área
        return self.ancho * self.alto

    def __contains__(self, punto):  # 'punto in region'
        px, py = punto
        return self.x <= px < self.x + self.ancho and self.y <= py < self.y + self.alto


r1 = RegionInteres(0, 0, 10, 20)
r2 = RegionInteres(0, 0, 10, 21)
print(repr(r1))  # RegionInteres(0, 0, 10, 20)  (vía __repr__)
print(r1 == r2)  # True  (vía __eq__)
print(len(r1))  # 200  (vía __len__: el área)
print((5, 5) in r1)  # True  (vía __contains__)
print({r1, r2})  # un conjunto con UNA región (iguales y con mismo hash)
