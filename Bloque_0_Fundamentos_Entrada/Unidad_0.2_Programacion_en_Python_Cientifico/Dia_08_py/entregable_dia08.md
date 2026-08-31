# Entregable Día 08 — Pandas: Series, DataFrame, GroupBy y Merge

## Objetivo

Este entregable demuestra el análisis de datos tabulares con Pandas sobre datos inspirados en detecciones y sensores.

El código se construyó principalmente a partir de las siete transferencias realizadas durante la sesión: construcción de DataFrames, alineación entre Series, selección, limpieza de valores faltantes, `groupby`, `merge` e integración completa.

Se hicieron únicamente ajustes mínimos para que el resultado cumpla literalmente la especificación del Día 8: evidencia explícita de `dropna`, propagación de `NaN`, asignación mediante `.loc` y verificaciones ejecutables.

## 1. DataFrame de detecciones e inspección de tipos

El registro principal se representa con un `DataFrame`:

```python
detecciones = pd.DataFrame({
    "Objeto": ["Persona", "Coche", "Persona", "Bici", "Perro", "Coche"],
    "Confianza": [0.92, float("nan"), 0.84, 0.76, 0.88, 0.91],
    "Fotograma": [1, 2, 3, 4, 5, 6],
    "Activa": [True, True, True, True, True, True],
}, index=["Med1", "Med2", "Med3", "Med4", "Med5", "Med6"])
```

El `DataFrame` permite heterogeneidad entre columnas: texto, flotantes, enteros y booleanos.

La estructura se inspecciona con:

```python
print(detecciones.dtypes)
print(detecciones.shape)
print(detecciones.index.tolist())
print(detecciones.columns.tolist())
```

Cada columna conserva un tipo apropiado y todas comparten el mismo índice de filas.

## 2. Alineación por etiqueta entre dos Series

Se construyen dos `Series` cuyos índices solo se solapan parcialmente:

```python
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
```

Las operaciones se realizan por etiqueta y no por posición:

```python
suma_series = serie_A + serie_B
multiplicacion_series = serie_A * serie_B
```

`cam1` y `cam3` encuentran pareja.

`cam2` solo aparece en la primera `Series` y `cam4` solo aparece en la segunda.

Por ello aparecen `NaN` observables en esas etiquetas.

El script verifica explícitamente:

```python
assert suma_series.isna().sum() == 2
assert pd.isna(suma_series.loc["cam2"])
assert pd.isna(suma_series.loc["cam4"])
```

## 3. Selección con `.loc`, `.iloc` y filtrado booleano

Sobre un DataFrame de sensores se comprueban los tres mecanismos de selección.

Por etiqueta:

```python
sensores.loc["Med2", "Temperatura"]
```

Por posición:

```python
sensores.iloc[1, 1]
```

Selección de varias columnas:

```python
sensores[["Sensor", "Temperatura"]]
```

Filtrado booleano con dos condiciones:

```python
sensores_filtrados = sensores[
    sensores["Activo"] & (sensores["Temperatura"] > 24)
]
```

`.loc` expresa etiquetas, `.iloc` expresa posiciones y la máscara booleana conserva únicamente las filas que satisfacen la condición.

## 4. Manejo de `NaN`

Primero se detectan los valores faltantes:

```python
detecciones.isna()
```

Después se demuestra su propagación en una operación elemento a elemento:

```python
propagacion = detecciones["Confianza"] + 0.10
```

La fila cuya confianza era `NaN` continúa siendo `NaN`.

También se demuestra la eliminación:

```python
sin_faltantes = detecciones.dropna(subset=["Confianza"])
```

La media se calcula sobre los valores presentes:

```python
media_confianza = detecciones["Confianza"].mean()
```

La imputación se realiza con `fillna`:

```python
confianza_imputada = detecciones["Confianza"].fillna(media_confianza)
```

La asignación al DataFrame se hace explícitamente mediante `.loc`:

```python
detecciones.loc[:, "Confianza"] = confianza_imputada
```

Finalmente se verifica que no queden faltantes:

```python
assert not detecciones["Confianza"].isna().any()
```

## 5. Filtrado y `groupby` con varias agregaciones

Después de limpiar los datos se conservan las detecciones con confianza mayor o igual a `0.80`:

```python
fiables = detecciones[detecciones["Confianza"] >= 0.80].copy()
```

Se aplica el patrón dividir–aplicar–combinar:

```python
resumen_objeto = fiables.groupby("Objeto")["Confianza"].agg([
    "count",
    "mean",
    "max",
])
```

`groupby("Objeto")` divide las filas según la clase.

`agg` aplica varias estadísticas a la columna `Confianza`.

Pandas combina el resultado en una nueva tabla indexada por los valores de `Objeto`.

## 6. `merge left` con metadatos

La tabla de metadatos contiene categorías para Persona, Coche y Bici:

```python
metadatos = pd.DataFrame({
    "Objeto": ["Persona", "Coche", "Bici"],
    "Categoria": ["Humano", "Vehiculo", "Vehiculo"],
})
```

El análisis requiere conservar todas las detecciones fiables aunque no exista una fila correspondiente en metadatos.

Por ello se usa:

```python
combinados = pd.merge(
    fiables,
    metadatos,
    on="Objeto",
    how="left",
)
```

`Perro` no tiene metadatos, pero permanece en el resultado y recibe `NaN` en `Categoria`.

La conservación se verifica:

```python
assert len(combinados) == len(fiables)
assert "Perro" in combinados["Objeto"].tolist()
assert combinados.loc[
    combinados["Objeto"] == "Perro",
    "Categoria"
].isna().all()
```

Esto demuestra la diferencia práctica entre conservar el lado izquierdo y descartar claves no coincidentes.

## 7. `groupby` final por categoría

Sobre el resultado enriquecido se calculan varias agregaciones:

```python
resumen_categoria = combinados.groupby("Categoria")["Confianza"].agg([
    "count",
    "mean",
    "max",
])
```

También se obtiene directamente la confianza media:

```python
combinados.groupby("Categoria")["Confianza"].mean()
```

Con ello el flujo completo queda:

```text
DataFrame
→ inspección
→ alineación por etiqueta
→ selección
→ detección de NaN
→ propagación
→ eliminación / imputación
→ filtrado
→ groupby
→ merge left
→ groupby final
```

## 8. Criterios de éxito verificados

El entregable demuestra un DataFrame heterogéneo con inspección de `dtypes`.

La alineación por etiqueta produce `NaN` observables.

Se usan `.loc`, `.iloc` y filtrado booleano.

Se demuestran `isna`, `dropna`, `fillna` y la propagación de `NaN`.

Las asignaciones se realizan mediante `.loc`, sin indexación encadenada.

El `groupby` calcula `count`, `mean` y `max`.

El `merge left` conserva las detecciones sin metadatos.

El análisis final usa `groupby` por `Categoria`.

El script contiene `assert` que convierten las propiedades importantes en verificaciones ejecutables.

## 9. Ejecución

Ejecutar desde el entorno virtual del Día 8:

```bash
python demo_pandas.py
```

La ejecución debe finalizar mostrando:

```text
Todas las verificaciones del Día 8 pasaron.
```

## 10. Git

Desde la raíz correspondiente del repositorio:

```bash
git add dia08_py/
git commit -m "feat(b0): U0.2 día 8 — Pandas: Series, DataFrame, groupby y merge"
```

## Conclusión

Pandas extiende el modelo de arrays trabajado con NumPy hacia datos tabulares etiquetados y heterogéneos por columna.

La alineación por índice evita asumir correspondencia posicional.

La selección permite expresar acceso por etiqueta, posición o condición.

Los datos faltantes deben detectarse y manejarse explícitamente.

`groupby` permite obtener estadísticas por categoría mediante dividir–aplicar–combinar.

`merge` permite relacionar tablas mediante claves compartidas, y `how="left"` conserva el conjunto principal aunque falten metadatos.

El resultado integra los seis fenómenos centrales del Día 8 en un pipeline ejecutable.
