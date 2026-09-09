# Entregable Día 3 — Listas enlazadas: nodos, referencias y compromiso inverso al array

## 1. Objetivo

Implementar y verificar una lista enlazada simple y una lista doblemente enlazada, y demostrar con mediciones el compromiso inverso frente al array dinámico: la lista enlazada favorece inserciones/eliminaciones en puntos conocidos, mientras que el array favorece el acceso por índice.

Archivo ejecutable asociado: `demo_enlazadas.py`.

---

## 2. Idea central

Una lista enlazada está formada por nodos dispersos en memoria. Cada nodo conserva un dato y una referencia al siguiente nodo. La estructura no depende de contigüidad, sino de la cadena de referencias.

Esto produce el compromiso principal del día:

- **Array dinámico:** acceso por índice `O(1)`, inserción intermedia o al principio `O(n)`.
- **Lista enlazada:** acceso por posición `O(n)`, inserción/eliminación en punto conocido `O(1)`.

El matiz importante es que el **reajuste** de referencias puede ser `O(1)`, pero **localizar** un punto arbitrario sigue siendo `O(n)`.

---

## 3. Lista enlazada simple

La implementación usa:

```python
class Nodo:
    __slots__ = ("dato", "siguiente")
```

Cada nodo almacena el dato y la referencia `siguiente`. `__slots__` evita atributos dinámicos adicionales y reduce la memoria por nodo.

La clase `ListaEnlazada` mantiene:

- `cabeza`;
- `cola`;
- `_tamano`.

Operaciones implementadas:

| Operación | Complejidad | Razón |
|---|---:|---|
| `insertar_principio` | `O(1)` | cambia un número constante de referencias |
| `insertar_final` | `O(1)` | se conserva referencia a `cola` |
| recorrer | `O(n)` | sigue nodo por nodo |
| buscar | `O(n)` | puede recorrer toda la lista |
| obtener por posición | `O(n)` | no existe acceso aleatorio |
| eliminar por valor | `O(n)` | localizar domina; reajustar es `O(1)` |

---

## 4. Casos límite verificados

La ejecución incluye aserciones para:

- lista vacía;
- búsqueda y eliminación en lista vacía;
- lista de un solo nodo;
- eliminación de la cabeza;
- transición a lista vacía;
- inserción al principio y al final;
- búsqueda de un valor;
- acceso por posición;
- eliminación de un valor intermedio.

Si cualquiera de estas propiedades falla, el programa termina por `AssertionError`.

---

## 5. Inversión de la lista

La función `invertir()` reutiliza los mismos nodos y solo mantiene tres referencias temporales:

```text
anterior
actual
siguiente
```

Por tanto:

- tiempo: `O(n)`;
- espacio adicional: `O(1)`.

No se crean nodos nuevos.

---

## 6. Lista doblemente enlazada

`NodoDoble` almacena:

```text
dato
siguiente
anterior
```

La segunda referencia permite:

- recorrer de cabeza a cola;
- recorrer de cola a cabeza;
- eliminar un nodo conocido en `O(1)` sin tener que buscar su predecesor.

La verificación crea `1 ⇄ 2 ⇄ 3 ⇄ 4`, comprueba ambos recorridos, elimina directamente el nodo `3` y vuelve a comprobar ambas direcciones.

---

## 7. Detección de ciclos — Floyd

Se implementa el algoritmo de Floyd con dos referencias:

- `lento`: avanza un nodo;
- `rapido`: avanza dos nodos.

Si ambos llegan a referenciar el mismo nodo, existe un ciclo.

Complejidad:

- tiempo: `O(n)`;
- espacio: `O(1)`.

Se verifican dos casos:

1. lista normal → `False`;
2. `a → b → c → a` → `True`.

---

## 8. Medición 1 — Inserción al principio

Hipótesis:

- lista enlazada: cada inserción al principio es `O(1)`, por lo que insertar `n` elementos cuesta `O(n)` total;
- array dinámico con `insert(0, x)`: cada inserción desplaza elementos, por lo que repetirla `n` veces tiende a `O(n²)` total.

Resultados de esta ejecución:

| n | Lista enlazada | Array `list.insert(0)` | Array / enlazada |
|---:|---:|---:|---:|
| 5,000 | 2.446 ms | 3.193 ms | 1.31× |
| 10,000 | 10.910 ms | 13.531 ms | 1.24× |
| 20,000 | 13.982 ms | 43.302 ms | 3.10× |

Interpretación: el array paga desplazamientos crecientes; la lista enlazada solo reajusta la cabeza. La diferencia aumenta con el tamaño de entrada, aunque los tiempos concretos dependen del hardware y del estado del sistema.

---

## 9. Medición 2 — Acceso por posición

Hipótesis:

- array: `arr[i]` calcula la posición directamente → `O(1)`;
- lista enlazada: `obtener(i)` debe seguir las referencias desde la cabeza → `O(n)`.

Resultados de esta ejecución:

| n | Lista enlazada | Array | Enlazada / array |
|---:|---:|---:|---:|
| 10,000 | 20.041 ms | 0.007 ms | 3059.26× |
| 50,000 | 103.770 ms | 0.006 ms | 18024.96× |
| 100,000 | 217.525 ms | 0.005 ms | 41896.19× |

Interpretación: el acceso del array permanece prácticamente constante, mientras que el recorrido enlazado aumenta con la posición y el tamaño de la estructura.

---

## 10. Comparación final

| Operación / propiedad | Array dinámico (`list`) | Lista enlazada |
|---|---:|---:|
| Acceso por índice | `O(1)` | `O(n)` |
| Búsqueda por valor | `O(n)` | `O(n)` |
| Insertar al principio | `O(n)` | `O(1)` |
| Insertar al final | `O(1)` amortizado | `O(1)` con cola |
| Insertar en medio, punto conocido | `O(n)` | `O(1)` |
| Eliminar al principio | `O(n)` | `O(1)` |
| Eliminar nodo conocido | `O(n)` por desplazamiento | `O(1)` con referencias adecuadas |
| Memoria por elemento | menor | mayor por las referencias |
| Localidad de caché | alta | menor |
| Acceso aleatorio | sí | no |

---

## 11. Regla de elección

Usaría **array dinámico** cuando predomina:

- acceso frecuente por índice;
- iteración intensiva;
- operaciones principalmente al final;
- mejor localidad de caché.

Usaría **lista enlazada** cuando predomina:

- inserción/eliminación en puntos ya conocidos;
- cambios frecuentes de forma;
- no se necesita acceso aleatorio.

Para una cola FIFO en Python, `deque` es normalmente la opción práctica porque ofrece operaciones `O(1)` en ambos extremos.

---

## 12. Evidencia de ejecución

Salida real obtenida al ejecutar `python demo_enlazadas.py`:

```text
======================================================================
DÍA 3 — LISTAS ENLAZADAS: COMPROMISO INVERSO AL ARRAY
======================================================================
PASS: casos límite, inversión, lista doble y Floyd

Inserción al principio: lista enlazada vs array
n=  5000 | enlazada=   2.446 ms | array=   3.193 ms | array/enlazada=   1.31x
n= 10000 | enlazada=  10.910 ms | array=  13.531 ms | array/enlazada=   1.24x
n= 20000 | enlazada=  13.982 ms | array=  43.302 ms | array/enlazada=   3.10x

Acceso por posición: lista enlazada vs array
n= 10000 | enlazada=  20.041 ms | array=   0.007 ms | enlazada/array=3059.26x
n= 50000 | enlazada= 103.770 ms | array=   0.006 ms | enlazada/array=18024.96x
n=100000 | enlazada= 217.525 ms | array=   0.005 ms | enlazada/array=41896.19x

PASS FINAL
```

La línea `PASS FINAL` solo aparece después de superar todas las aserciones y las verificaciones de casos límite, inversión, lista doble y detección de ciclos.

---

## 13. Limitaciones

Las mediciones de tiempo no sustituyen el análisis asintótico. Los valores absolutos dependen del hardware, del intérprete y de la carga del sistema. Se usan para confirmar la tendencia predicha por el análisis, no para redefinir la clase Big-O.

La eliminación por valor en la lista simple sigue siendo `O(n)` porque antes del reajuste debe localizarse el nodo. `O(1)` aplica cuando el punto de modificación ya es conocido.

---

## 14. Conclusión

Array y lista enlazada resuelven prioridades diferentes. La contigüidad del array permite acceso directo `O(1)`, pero obliga a desplazar elementos en inserciones internas. La lista enlazada evita esos desplazamientos mediante referencias, logrando reajustes `O(1)` en puntos conocidos, pero pierde el acceso aleatorio y necesita recorridos `O(n)`.

La elección correcta depende del patrón de operaciones, no de considerar una estructura universalmente superior.

---

## 15. Comandos de validación y versión

```bash
cd ~/vixia/dia03_algo/lab
python demo_enlazadas.py

cd ~/vixia
git add dia03_algo/
git commit -m "feat(b0): U0.3 día 3 — listas enlazadas: nodos, simple, doble y el compromiso inverso"
```
