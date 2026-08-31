import pandas as pd

detecciones = pd.DataFrame({
    "Objeto" : ["Persona","Coche","Bici","Perro"],
    "Confianza" : [0.92,0.81,0.88,0.76]
})

metadatos = pd.DataFrame({
    "Objeto" : ["Persona","Coche","Bici"],
    "Categoria" : ["Humano","Vehiculo","Vehiculo"]
})

mergeDatos = pd.merge(detecciones, metadatos, on="Objeto", how="left")
print(mergeDatos)

print(mergeDatos.groupby("Categoria")["Confianza"].mean())