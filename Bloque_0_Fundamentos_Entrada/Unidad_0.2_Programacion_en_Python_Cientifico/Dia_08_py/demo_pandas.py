import pandas as pd


def seccion(titulo: str) -> None:
    print(f"\n{'=' * 72}\n{titulo}\n{'=' * 72}")


# ---------------------------------------------------------------------
# 1. DataFrame heterogéneo de detecciones + inspección
# ---------------------------------------------------------------------

seccion("1. DataFrame de detecciones: estructura y dtypes")

detecciones = pd.DataFrame({
    "Objeto": ["Persona", "Coche", "Persona", "Bici", "Perro", "Coche"],
    "Confianza": [0.92, float("nan"), 0.84, 0.76, 0.88, 0.91],
    "Fotograma": [1, 2, 3, 4, 5, 6],
    "Activa": [True, True, True, True, True, True],
}, index=["Med1", "Med2", "Med3", "Med4", "Med5", "Med6"])

print(detecciones)
print("\ndtypes:\n", detecciones.dtypes)
print("shape:", detecciones.shape)
print("index:", detecciones.index.tolist())
print("columns:", detecciones.columns.tolist())


# ---------------------------------------------------------------------
# 2. Alineación por etiqueta entre dos Series
# ---------------------------------------------------------------------

seccion("2. Series: alineación por etiqueta")

serie_A = pd.Series(
    [10, 20, 30],
    index=["cam1", "cam2", "cam3"],
    dtype="int16",
)

serie_B = pd.Series(
    [100, 200, 300],
    index=["cam3", "cam1", "cam4"],
    dtype="int16",
)

suma_series = serie_A + serie_B
multiplicacion_series = serie_A * serie_B

print("Serie A:\n", serie_A)
print("\nSerie B:\n", serie_B)
print("\nA + B:\n", suma_series)
print("\nA * B:\n", multiplicacion_series)

assert suma_series.isna().sum() == 2
assert pd.isna(suma_series.loc["cam2"])
assert pd.isna(suma_series.loc["cam4"])


# ---------------------------------------------------------------------
# 3. Selección con loc, iloc y filtrado booleano
# ---------------------------------------------------------------------

seccion("3. Selección: loc, iloc y booleano")

sensores = pd.DataFrame({
    "Sensor": ["S1", "S2", "S3"],
    "Temperatura": [24.5, 27.1, 23.8],
    "Lecturas": [120, 95, 143],
    "Activo": [True, False, True],
}, index=["Med1", "Med2", "Med3"])

print("Temperatura Med2 con loc:", sensores.loc["Med2", "Temperatura"])
print("La misma celda con iloc:", sensores.iloc[1, 1])
print("\nColumnas Sensor y Temperatura:\n", sensores[["Sensor", "Temperatura"]])

sensores_filtrados = sensores[
    sensores["Activo"] & (sensores["Temperatura"] > 24)
]
print("\nActivos con temperatura > 24:\n", sensores_filtrados)


# ---------------------------------------------------------------------
# 4. NaN: isna, propagación, dropna y fillna
# ---------------------------------------------------------------------

seccion("4. Datos faltantes: detección, propagación y limpieza")

print("Mapa de NaN antes de limpiar:\n", detecciones.isna())

propagacion = detecciones["Confianza"] + 0.10
print("\nPropagación de NaN al sumar 0.10:\n", propagacion)
assert pd.isna(propagacion.loc["Med2"])

sin_faltantes = detecciones.dropna(subset=["Confianza"])
print("\nVista eliminando filas con Confianza NaN:\n", sin_faltantes)

media_confianza = detecciones["Confianza"].mean()
confianza_imputada = detecciones["Confianza"].fillna(media_confianza)

# La asignación se realiza explícitamente con .loc.
detecciones.loc[:, "Confianza"] = confianza_imputada

print("\nMedia usada para imputar:", media_confianza)
print("\nDetecciones después de fillna:\n", detecciones)
print("¿Queda algún NaN en Confianza?:", detecciones["Confianza"].isna().any())

assert not detecciones["Confianza"].isna().any()


# ---------------------------------------------------------------------
# 5. Filtrado + GroupBy con varias agregaciones
# ---------------------------------------------------------------------

seccion("5. Filtrado y GroupBy")

fiables = detecciones[detecciones["Confianza"] >= 0.80].copy()

resumen_objeto = fiables.groupby("Objeto")["Confianza"].agg([
    "count",
    "mean",
    "max",
])

print("Detecciones fiables:\n", fiables)
print("\nResumen por Objeto:\n", resumen_objeto)


# ---------------------------------------------------------------------
# 6. Merge left con metadatos
# ---------------------------------------------------------------------

seccion("6. Merge left con metadatos")

metadatos = pd.DataFrame({
    "Objeto": ["Persona", "Coche", "Bici"],
    "Categoria": ["Humano", "Vehiculo", "Vehiculo"],
})

combinados = pd.merge(
    fiables,
    metadatos,
    on="Objeto",
    how="left",
)

print(combinados)

# Perro no tiene metadatos, pero debe conservarse por ser merge left.
assert len(combinados) == len(fiables)
assert "Perro" in combinados["Objeto"].tolist()
assert combinados.loc[combinados["Objeto"] == "Perro", "Categoria"].isna().all()


# ---------------------------------------------------------------------
# 7. GroupBy final por categoría
# ---------------------------------------------------------------------

seccion("7. Análisis final por Categoria")

resumen_categoria = combinados.groupby("Categoria")["Confianza"].agg([
    "count",
    "mean",
    "max",
])

print(resumen_categoria)

print("\nConfianza media por Categoria:\n",
      combinados.groupby("Categoria")["Confianza"].mean())

print("\nTodas las verificaciones del Día 8 pasaron.")