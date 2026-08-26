from dataclasses import dataclass


@dataclass
class Termostato:
    temperatura_objetivo: int = 21

    def subir(self, grados: int):
        # Calculamos la nueva temperatura tentativa
        nueva_temp = self.temperatura_objetivo + grados
        if nueva_temp > 30:
            raise ValueError(f"No se puede subir a {nueva_temp}°C. El límite máximo es 30°C.")

        self.temperatura_objetivo = nueva_temp
        print(f"Aumento exitoso. Nueva temperatura: {self.temperatura_objetivo}°C")

    def bajar(self, grados: int):
        # Calculamos la nueva temperatura tentativa
        nueva_temp = self.temperatura_objetivo - grados
        if nueva_temp < 10:
            raise ValueError(f"No se puede bajar a {nueva_temp}°C. El límite mínimo es 10°C.")

        self.temperatura_objetivo = nueva_temp
        print(f"Disminución exitosa. Nueva temperatura: {self.temperatura_objetivo}°C")


# --- Demostración del funcionamiento ---
temp = Termostato()  # Inicia en 21°C

# 1. Intento válido
temp.subir(5)  # Sube a 26°C

# 2. Intento inválido (Exceder el máximo)
try:
    temp.subir(10)  # Intentaría ir a 36°C (Lanza excepción)
except ValueError as e:
    print(f"Error detectado: {e}")

# 3. Intento inválido (Bajar del mínimo)
try:
    temp.bajar(20)  # Intentaría ir a 6°C (Lanza excepción)
except ValueError as e:
    print(f"Error detectado: {e}")

# La temperatura se mantiene a salvo en un rango válido
print(f"Temperatura final del termostato: {temp.temperatura_objetivo}°C")


