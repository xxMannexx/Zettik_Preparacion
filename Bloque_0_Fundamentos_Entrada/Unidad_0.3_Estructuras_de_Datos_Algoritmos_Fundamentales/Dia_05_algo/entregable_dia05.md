# Entregable Día 5 — Árboles Binarios de Búsqueda

## 1. Objetivo

Implementar un Árbol Binario de Búsqueda (ABB) con inserción, búsqueda, eliminación y recorridos; verificar que el recorrido en-orden produce los valores ordenados; medir la búsqueda eficiente frente a una lista; demostrar la degeneración por inserción ordenada; comparar ABB contra tabla hash; y aplicar el árbol a un índice cronológico de eventos de VizionarIA.

El archivo ejecutable asociado es:

```text
demo_arboles.py
```

---

## 2. Modelo de nodo

La estructura parte de un nodo enlazado con dos referencias:

```python
class NodoArbol:
    __slots__ = ("dato", "izquierdo", "derecho")

    def __init__(self, dato):
        self.dato = dato
        self.izquierdo = None
        self.derecho = None
```

Regla del ABB:

```text
menor  -> izquierda
mayor  -> derecha
igual  -> no se duplica
```

---

## 3. Inserción

La inserción se implementa recursivamente. Cada llamada recibe la raíz de un subárbol y devuelve la raíz actualizada de ese mismo subárbol.

```python
def _insertar(self, nodo, valor):
    if nodo is None:
        return NodoArbol(valor)

    if valor < nodo.dato:
        nodo.izquierdo = self._insertar(nodo.izquierdo, valor)
    elif valor > nodo.dato:
        nodo.derecho = self._insertar(nodo.derecho, valor)

    return nodo
```

La idea usada durante la clase fue:

```text
None -> crear nodo
menor -> bajar por izquierda
mayor -> bajar por derecha
```

---

## 4. Búsqueda

La búsqueda usa un único camino desde la raíz:

```python
def buscar(self, dato):
    nodo = self.raiz

    while nodo is not None:
        if nodo.dato == dato:
            return True
        elif nodo.dato < dato:
            nodo = nodo.derecho
        else:
            nodo = nodo.izquierdo

    return False
```

En un ABB con altura logarítmica, el coste de búsqueda es `O(log n)`. En un árbol degenerado puede llegar a `O(n)`.

---

## 5. Eliminación

Se manejan los tres casos.

### Caso 1 — hoja

Si no tiene hijos, el nodo se reemplaza por `None`.

### Caso 2 — un hijo

Si solo tiene hijo izquierdo:

```python
return nodo.izquierdo
```

Si solo tiene hijo derecho:

```python
return nodo.derecho
```

El `return` permite que el padre actualice su referencia y el nodo eliminado quede desconectado.

### Caso 3 — dos hijos

Se usa el sucesor en-orden: el mínimo del subárbol derecho.

```python
sucesor = nodo.derecho

while sucesor.izquierdo is not None:
    sucesor = sucesor.izquierdo

nodo.dato = sucesor.dato
nodo.derecho = self._eliminar(nodo.derecho, sucesor.dato)
```

Primero se copia el dato del sucesor al nodo actual y después se elimina la copia original del sucesor.

---

## 6. Recorridos

### En-orden

```text
izquierda -> nodo -> derecha
```

En un ABB produce los valores en orden ascendente.

### Pre-orden

```text
nodo -> izquierda -> derecha
```

### Post-orden

```text
izquierda -> derecha -> nodo
```

La implementación utiliza recursión; las llamadas pendientes quedan en la pila hasta llegar a `None` y comenzar el retorno.

---

## 7. Verificación funcional

El script verifica con `assert`:

- árbol vacío;
- inserción;
- búsqueda existente y no existente;
- recorrido en-orden;
- recorrido pre-orden;
- recorrido post-orden;
- eliminación de hoja;
- eliminación con un hijo;
- eliminación con dos hijos.

Resultado real:

```text
PASS: vacío, inserción, búsqueda, 3 recorridos y 3 casos de eliminación
```

---

## 8. Búsqueda ABB frente a lista

Se construyen ABB con inserción aleatoria para obtener árboles razonablemente equilibrados en promedio y se comparan contra búsqueda lineal en una lista.

Resultados reales:

| n | Altura ABB | ABB | Lista | Ventaja |
|---:|---:|---:|---:|---:|
| 10,000 | 31 | 0.419 ms | 28.827 ms | 68.8x |
| 50,000 | 36 | 0.313 ms | 148.336 ms | 473.7x |
| 100,000 | 38 | 0.417 ms | 302.598 ms | 725.1x |

La lista crece linealmente con `n`, mientras que el ABB recorre solo un camino cuya longitud depende de la altura.

---

## 9. Degeneración

Insertar valores ya ordenados provoca que todos los nodos caigan hacia la misma rama:

```text
1
 \
  2
   \
    3
     \
      4
```

La estructura deja de comportarse como árbol eficiente y se vuelve equivalente a una lista enlazada.

Resultados reales:

| n | Altura aleatoria | Altura degenerada | Degradación |
|---:|---:|---:|---:|
| 1,000 | 19 | 999 | 109.6x |
| 2,000 | 26 | 1,999 | 230.3x |
| 4,000 | 24 | 3,999 | 723.6x |

Esto demuestra que un ABB normal no garantiza `O(log n)`. Los árboles auto-balanceados, como AVL y rojo-negro, existen para mantener la altura logarítmica.

---

## 10. Comparación ABB vs tabla hash

Medición real para `n = 100,000`:

```text
ABB=8.532 ms
dict=0.344 ms
dict≈24.8x más rápido en búsqueda pura
```

Pero la diferencia estructural es importante:

```text
ABB -> mantiene orden por clave y permite recorrido ordenado
hash -> O(1) promedio en búsqueda pura, pero no orden por clave
```

Ejemplo observado:

```text
ABB en-orden: [0, 1, 2, 3, 4, 5, 6, 7]
dict primeras claves: [20139, 86038, 37488, 7387, 60920, 41973, 88650, 6538]
```

En Python moderno el `dict` conserva orden de inserción, pero eso no significa orden numérico o lexicográfico por clave.

---

## 11. Aplicación a VizionarIA

Se construye un índice de eventos usando tuplas:

```text
(timestamp, id_objeto, clase)
```

Datos insertados:

```text
(120, "obj_17", "persona")
(105, "obj_52", "coche")
(135, "obj_31", "bicicleta")
(110, "obj_08", "persona")
(128, "obj_60", "señal")
```

El recorrido en-orden produce:

```text
(105, 'obj_52', 'coche')
(110, 'obj_08', 'persona')
(120, 'obj_17', 'persona')
(128, 'obj_60', 'señal')
(135, 'obj_31', 'bicicleta')
```

Resultado:

```text
PASS: recorrido cronológico correcto
```

---

## 12. Conclusión

El ABB generaliza el nodo enlazado: en lugar de una referencia `siguiente`, cada nodo puede tener referencias `izquierdo` y `derecho`.

La propiedad fundamental es:

```text
menores a la izquierda
mayores a la derecha
```

Esa propiedad permite buscar siguiendo un solo camino y obtener los datos ordenados mediante el recorrido en-orden.

La complejidad depende de la altura:

```text
altura ≈ log n -> búsqueda O(log n)
altura ≈ n     -> búsqueda O(n)
```

Por eso un ABB normal puede degenerar y un árbol auto-balanceado es necesario cuando se quiere garantizar `O(log n)`.

La comparación final queda:

```text
tabla hash -> O(1) promedio, búsqueda pura, sin orden por clave
árbol balanceado -> O(log n) garantizado, con orden
```

---

## 13. Evidencia de ejecución

```text
==============================================================================
DÍA 5 — ÁRBOLES BINARIOS DE BÚSQUEDA
==============================================================================

1. Verificación funcional
PASS: vacío, inserción, búsqueda, 3 recorridos y 3 casos de eliminación

2. ABB con inserción aleatoria vs lista
n=  10000 | altura= 31 | ABB=   0.419 ms | lista=   28.827 ms | ventaja=   68.8x
n=  50000 | altura= 36 | ABB=   0.313 ms | lista=  148.336 ms | ventaja=  473.7x
n= 100000 | altura= 38 | ABB=   0.417 ms | lista=  302.598 ms | ventaja=  725.1x

3. Degeneración por inserción ordenada
n= 1000 | altura_aleatoria= 19 | altura_degenerada= 999 | degradación= 109.6x
n= 2000 | altura_aleatoria= 26 | altura_degenerada=1999 | degradación= 230.3x
n= 4000 | altura_aleatoria= 24 | altura_degenerada=3999 | degradación= 723.6x

4. Dict vs ABB
ABB=8.532 ms | dict=0.344 ms | dict≈24.8x más rápido en búsqueda pura
ABB en-orden: [0, 1, 2, 3, 4, 5, 6, 7]
dict primeras claves: [20139, 86038, 37488, 7387, 60920, 41973, 88650, 6538]

5. Índice cronológico de eventos de VizionarIA
Eventos ordenados por tiempo:
(105, 'obj_52', 'coche')
(110, 'obj_08', 'persona')
(120, 'obj_17', 'persona')
(128, 'obj_60', 'señal')
(135, 'obj_31', 'bicicleta')
PASS: recorrido cronológico correcto

PASS FINAL
```

---

## 14. Comandos

```bash
cd ~/vixia/dia05_algo/lab
python demo_arboles.py

cd ~/vixia
git add dia05_algo/
git commit -m "feat(b0): U0.3 día 5 — árboles: ABB, O(log n), recorridos y degeneración"
```
