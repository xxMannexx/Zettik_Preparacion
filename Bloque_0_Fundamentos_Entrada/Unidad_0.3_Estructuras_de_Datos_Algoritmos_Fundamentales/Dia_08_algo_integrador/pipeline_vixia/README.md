# Pipeline Algorítmico de VizionarIA — U0.3

Proyecto integrador del Día 8/8 de la Unidad 0.3:
Estructuras de Datos y Algoritmos Fundamentales.

## Objetivo

Procesar un dataset de detecciones de VizionarIA mediante
un pipeline que seleccione la estructura de datos adecuada
para cada patrón de operaciones.

## Arquitectura

Dataset
→ Fase 1: indexación hash
→ Fase 2: selección por confianza
→ Fase 3: cronología mediante ABB
→ Fase 4: relaciones espaciales mediante grafo
→ Fase 5: integración, complejidad y robustez

## Fase 1 — Tabla hash

Se utilizan `dict` y `set`.

- `por_id`: acceso a detecciones por identificador.
- `por_clase`: agrupación por clase.
- `vistos`: deduplicación.

Construcción: O(n).
Consulta promedio por id: O(1).

## Fase 2 — Ordenación + búsqueda binaria

Las detecciones se ordenan por confianza con `sorted`
(Timsort) y se localiza el primer elemento que supera el
umbral mediante búsqueda binaria.

Ordenación: O(n log n).
Búsqueda: O(log n).
Total: O(n log n).

## Fase 3 — Árbol binario de búsqueda

Las detecciones se indexan por `timestamp`.

- búsqueda por timestamp;
- recorrido en-orden para cronología;
- máximo para obtener el evento más reciente.

Inserción/búsqueda esperada: O(log n) con árbol equilibrado.
Recorrido completo: O(n).

La inserción se mezcla para mitigar la degeneración del ABB.

## Fase 4 — Grafo espacial

Cada detección es un vértice.

Existe una arista cuando dos detecciones están a una
distancia euclídea menor al umbral.

Construcción ingenua: O(V²).

BFS obtiene objetos alcanzables por número de saltos.
DFS iterativo obtiene componentes conexas.

BFS/DFS: O(V + E).

## Complejidad total

La fase dominante es la construcción ingenua del grafo:

O(V²)

porque el resto de las fases cuesta O(n log n) o menos.

## Robustez

El pipeline aplica:

- límite máximo de tamaño de entrada;
- hash de Python para los índices;
- Timsort en lugar de quicksort vulnerable a entradas adversas;
- inserción mezclada para mitigar degeneración del ABB;
- conjunto de visitados en grafos;
- DFS iterativo para evitar desbordamiento de la pila.

## Reproducibilidad

El dataset de demostración utiliza una semilla fija.

## Ejecutar

Desde `Dia_08_algo_integrador`:

```bash
pytest -v
python -m pipeline_vixia.dataset_demo
python -m pipeline_vixia.benchmark