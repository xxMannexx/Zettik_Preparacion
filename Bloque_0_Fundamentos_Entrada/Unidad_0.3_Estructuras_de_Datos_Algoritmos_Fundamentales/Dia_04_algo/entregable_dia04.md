# Entregable Día 4 — Tablas hash: acceso O(1) promedio, colisiones y encadenamiento

## 1. Objetivo

Implementar una tabla hash propia con encadenamiento, integrando el array del Día 2 y las listas enlazadas del Día 3, y demostrar mediante mediciones tanto su comportamiento `O(1)` promedio como su peor caso bajo colisiones deliberadas.

Archivo ejecutable asociado: `demo_hash.py`.

---

## 2. Estructura implementada

La tabla está formada por un array de cubetas. Cada cubeta guarda la cabeza de una lista enlazada de objetos `Par`:

```text
tabla
├── cubeta 0 → Par → Par → None
├── cubeta 1 → None
├── cubeta 2 → Par → None
└── ...
```

Cada `Par` contiene:

```python
__slots__ = ("clave", "valor", "siguiente")
```

La función de índice es:

```python
hash(clave) % capacidad
```

El hash transforma una clave arbitraria en un entero y el módulo la reduce al rango válido del array.

---

## 3. Operaciones

| Operación | Promedio | Peor caso | Mecanismo |
|---|---:|---:|---|
| insertar | `O(1)` | `O(n)` | localizar cubeta y recorrer su cadena si hay colisiones |
| buscar | `O(1)` | `O(n)` | hash + acceso a cubeta + búsqueda dentro de la cadena |
| eliminar | `O(1)` | `O(n)` | localizar cubeta y reajustar referencias |
| actualizar clave existente | `O(1)` | `O(n)` | encontrar la clave y reemplazar su valor |
| redimensionar | — | `O(n)` puntual | rehash de todos los elementos |

El `O(1)` es promedio, no garantizado: depende de que las claves estén bien distribuidas y las cubetas permanezcan cortas.

---

## 4. Encadenamiento y colisiones

Las colisiones son inevitables porque existen más claves posibles que posiciones disponibles. Dos claves distintas pueden cumplir:

```text
hash(k1) % m == hash(k2) % m
```

El encadenamiento resuelve esto almacenando todos los pares que caen en la misma cubeta dentro de una lista enlazada.

La inserción de una clave nueva se hace al principio:

```python
nuevo.siguiente = self._cubetas[i]
self._cubetas[i] = nuevo
```

Si la clave ya existe, no se crea un nodo duplicado; se actualiza su valor.

---

## 5. Factor de carga y redimensionamiento

El factor de carga es:

```text
alpha = n / m
```

donde `n` es el número de elementos y `m` el número de cubetas.

La implementación redimensiona cuando una inserción nueva haría que `alpha` supere `0.75`.

Al duplicar la capacidad cambia `m`, así que no basta con copiar los nodos a la misma posición: se debe recalcular el índice de cada clave. Ese proceso es el **rehash**.

El rehash cuesta `O(n)` de forma puntual, pero sucede de manera ocasional, por lo que la inserción conserva coste amortizado constante.

---

## 6. Verificación funcional

El script verifica con `assert`:

- inserción;
- búsqueda;
- actualización de una clave existente sin aumentar el tamaño;
- eliminación;
- redimensionamiento conservando los valores;
- factor de carga después del crecimiento;
- rechazo de listas como claves no hashables.

Resultado:

```text
PASS: inserción, búsqueda, actualización, eliminación, rehash y hashables
```

---

## 7. Medición — tabla hash frente a lista

Hipótesis:

- búsqueda por clave en la tabla hash: `O(1)` promedio;
- pertenencia en una lista: `O(n)`.

Resultados de la ejecución:

| n | Tabla hash | Lista | Ventaja |
|---:|---:|---:|---:|
| 10,000 | 0.039 ms | 17.378 ms | 449.0× |
| 50,000 | 0.045 ms | 107.100 ms | 2383.7× |
| 100,000 | 0.040 ms | 185.380 ms | 4613.9× |

La diferencia crece con `n`, confirmando que no se trata solo de una constante distinta, sino de clases de crecimiento diferentes.

---

## 8. Medición — efecto del factor de carga

Para aislar el efecto de `alpha`, esta prueba desactiva temporalmente el redimensionamiento y mantiene `n = 20 000`, variando la cantidad de cubetas.

| Cubetas `m` | `alpha = n/m` | Longitud máxima | Media en cubetas ocupadas |
|---:|---:|---:|---:|
| 40,000 | 0.50 | 1 | 1.00 |
| 20,000 | 1.00 | 1 | 1.00 |
| 5,000 | 4.00 | 4 | 4.00 |
| 1,000 | 20.00 | 20 | 20.00 |

Interpretación: al aumentar `alpha`, más elementos comparten cubeta. En general, cadenas más largas aumentan el trabajo necesario dentro de cada cubeta. El redimensionamiento existe precisamente para mantener este factor acotado.

---

## 9. Peor caso — hash flooding

Se crea una clase didáctica cuya función hash devuelve siempre cero:

```python
def __hash__(self):
    return 0
```

Así, todas las claves terminan en la misma cubeta.

Resultados:

| n | Inserción normal | Inserción con colisiones | Degradación |
|---:|---:|---:|---:|
| 1,000 | 0.527 ms | 60.533 ms | 114.8× |
| 2,000 | 1.378 ms | 173.932 ms | 126.2× |
| 4,000 | 2.375 ms | 681.658 ms | 287.1× |

Con una única cadena que crece hasta longitud `n`, cada nueva inserción puede recorrer cada vez más elementos. Una secuencia de `n` inserciones puede degradarse hacia `O(n²)` total.

Esto reproduce el mecanismo de **hash flooding**: un atacante que controla claves y puede provocar colisiones fuerza el peor caso de la tabla hash y puede agotar CPU.

La aleatorización del hash dificulta que el atacante prediga las colisiones; no elimina matemáticamente el peor caso.

---

## 10. Claves hashables

Una clave debe tener un hash estable mientras esté almacenada.

Funciona:

```python
d[(1, 2)] = "válido"
```

No funciona:

```python
d[[1, 2]] = "inválido"
```

La tupla es inmutable y, si sus componentes son hashables, su hash es estable. La lista es mutable y Python la rechaza como clave con `TypeError`.

---

## 11. Aplicación a VizionarIA

La demostración usa:

```python
seguimientos = {}
vistos_frame = set()
```

`seguimientos` persiste entre frames y asocia:

```text
id_objeto → información del seguimiento
```

`vistos_frame` se usa para comprobar si un identificador ya apareció dentro del frame actual.

Ejemplo:

```text
obj_17 → persona, 0.93
obj_52 → coche, 0.88
obj_17 → persona, 0.91
```

La segunda aparición de `obj_17` actualiza su información en el diccionario y el `set` permite reconocer que el ID ya había aparecido en ese frame.

Ambas operaciones son `O(1)` promedio.

---

## 12. Conclusión

La tabla hash convierte el acceso por índice numérico del array en acceso por una clave arbitraria mediante `hash(clave) % m`.

Su eficiencia depende de tres condiciones:

1. distribución razonable de las claves;
2. factor de carga acotado;
3. manejo correcto de colisiones.

Con esas condiciones, insertar, buscar y eliminar son `O(1)` promedio. Si las colisiones se concentran, la tabla puede degenerar hasta `O(n)` por operación. Esto convierte el peor caso en una cuestión tanto de rendimiento como de seguridad.

La estructura integra directamente:

```text
array del Día 2
+
listas enlazadas del Día 3
=
tabla hash con encadenamiento
```

---

## 13. Evidencia completa de ejecución

```text
============================================================================
DÍA 4 — TABLAS HASH: O(1) PROMEDIO, COLISIONES Y ENCADENAMIENTO
============================================================================

1. Verificación funcional
PASS: inserción, búsqueda, actualización, eliminación, rehash y hashables

2. Búsqueda: tabla hash O(1) promedio vs lista O(n)
n=  10000 | hash=   0.039 ms | lista=  17.378 ms | ventaja=   449.0x
n=  50000 | hash=   0.045 ms | lista= 107.100 ms | ventaja=  2383.7x
n= 100000 | hash=   0.040 ms | lista= 185.380 ms | ventaja=  4613.9x

3. Efecto del factor de carga en la longitud de las cubetas
m= 40000 | alpha= 0.50 | max_cubeta=   1 | media_cubetas_ocupadas=  1.00
m= 20000 | alpha= 1.00 | max_cubeta=   1 | media_cubetas_ocupadas=  1.00
m=  5000 | alpha= 4.00 | max_cubeta=   4 | media_cubetas_ocupadas=  4.00
m=  1000 | alpha=20.00 | max_cubeta=  20 | media_cubetas_ocupadas= 20.00

4. Peor caso: hash flooding con __hash__ constante
n= 1000 | normal=   0.527 ms | colisiones=   60.533 ms | degradación=   114.8x
n= 2000 | normal=   1.378 ms | colisiones=  173.932 ms | degradación=   126.2x
n= 4000 | normal=   2.375 ms | colisiones=  681.658 ms | degradación=   287.1x

5. Índice de seguimientos de VizionarIA con dict y set
seguimientos={'obj_17': {'clase': 'persona', 'confianza': 0.91}, 'obj_52': {'clase': 'coche', 'confianza': 0.88}}
vistos_frame=['obj_17', 'obj_52']
duplicados_frame=['obj_17']
PASS: acceso/actualización por ID y deduplicación por frame

PASS FINAL
```

---

## 14. Comandos de validación y versión

```bash
cd ~/vixia/dia04_algo/lab
python demo_hash.py

cd ~/vixia
git add dia04_algo/
git commit -m "feat(b0): U0.3 día 4 — tablas hash: O(1) promedio, encadenamiento y hash flooding"
```
