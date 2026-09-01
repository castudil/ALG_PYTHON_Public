# Lectura 4 — La partición tricotómica de Dijkstra

**Semana 10 · Unidad 3 — Quicksort**
Lectura de trabajo autónomo. *No se dicta en cátedra y no entra en la Prueba de Unidad 3.*

---

## Por qué existe

La partición de dos punteros que vimos en clase reparte bien los duplicados, pero **los
sigue reprocesando**. Si el arreglo tiene un millón de elementos y solo tres valores
distintos, Quicksort vuelve a particionar una y otra vez segmentos donde ya está todo
igual al pivote.

> Si sé que `arr[k]` es igual al pivote, ¿tiene sentido volver a ordenar esa posición en
> las llamadas recursivas?

No: ya está en su lugar definitivo, igual que el pivote. Esa observación es toda la idea.

## La bandera nacional holandesa

Edsger Dijkstra planteó el problema de ordenar en una sola pasada un arreglo de tres
colores. Aplicado a Quicksort, la partición produce **tres zonas** en vez de dos:

```
        < pivote        == pivote        sin revisar        > pivote
   +--------------+-----------------+-----------------+--------------+
   |              |                 |                 |              |
   +--------------+-----------------+-----------------+--------------+
   lo           lt-1  lt          i-1  i             gt  gt+1        hi
```

Tres punteros mantienen el invariante:

| Rango | Contenido |
|-------|-----------|
| `arr[lo .. lt-1]` | **menores** que el pivote |
| `arr[lt .. i-1]` | **iguales** al pivote |
| `arr[i .. gt]` | **aún sin clasificar** |
| `arr[gt+1 .. hi]` | **mayores** que el pivote |

En cada paso se mira `arr[i]`:

- **menor** → `swap(arr[lt], arr[i])`, avanzan `lt` e `i`
- **mayor** → `swap(arr[i], arr[gt])`, retrocede `gt`. **`i` no avanza**: lo que llegó
  desde la derecha todavía no se ha revisado.
- **igual** → solo avanza `i`

Al terminar, **toda la zona central ya está en su posición definitiva** y la recursión se
aplica únicamente a `[lo, lt-1]` y `[gt+1, hi]`.

## El código

```python
def particionar_tres_vias(arr, lo, hi):
    """
    Partición tricotómica de Dijkstra (bandera nacional holandesa).

    Retorna:
        tuple[int, int]: (lt, gt) tal que arr[lt..gt] son todos iguales al pivote

    Complejidad:
        Temporal: O(hi - lo) — una sola pasada
        Espacial: O(1)
    """
    pivote = arr[lo]
    lt = lo         # frontera izquierda de la zona de iguales
    i = lo + 1      # elemento en revisión
    gt = hi         # frontera derecha de la zona sin revisar

    while i <= gt:
        if arr[i] < pivote:
            arr[lt], arr[i] = arr[i], arr[lt]
            lt += 1
            i += 1
        elif arr[i] > pivote:
            arr[i], arr[gt] = arr[gt], arr[i]
            gt -= 1          # i NO avanza: lo que llegó no se ha revisado
        else:
            i += 1

    return lt, gt


def quicksort_tres_vias(arr, lo=0, hi=None):
    """Quicksort tricotómico. O(n) cuando hay pocas claves distintas."""
    if hi is None:
        hi = len(arr) - 1
    if lo < hi:
        lt, gt = particionar_tres_vias(arr, lo, hi)
        quicksort_tres_vias(arr, lo, lt - 1)     # solo los menores
        quicksort_tres_vias(arr, gt + 1, hi)     # solo los mayores
    return arr
```

## Traza sobre un ejemplo pequeño

Arreglo `[2, 1, 2, 3, 2, 0, 2]`, pivote `2` (el primer elemento):

```
  paso   lt   i  gt   arreglo              qué pasa
  ----------------------------------------------------------------
     0    0   1   6   [2, 1, 2, 3, 2, 0, 2]  arr[1]=1 < 2 -> swap(lt,i), lt+, i+
     1    1   2   6   [1, 2, 2, 3, 2, 0, 2]  arr[2]=2 == 2 -> i+
     2    1   3   6   [1, 2, 2, 3, 2, 0, 2]  arr[3]=3 > 2 -> swap(i,gt), gt-
     3    1   3   5   [1, 2, 2, 2, 2, 0, 3]  arr[3]=2 == 2 -> i+
     4    1   4   5   [1, 2, 2, 2, 2, 0, 3]  arr[4]=2 == 2 -> i+
     5    1   5   5   [1, 2, 2, 2, 2, 0, 3]  arr[5]=0 < 2 -> swap(lt,i), lt+, i+
     6    2   6   5   [1, 0, 2, 2, 2, 2, 3]  i > gt -> fin
```

Resultado: `lt = 2`, `gt = 5`. Las posiciones 2 a 5 contienen todas el pivote y **ya no se
vuelven a tocar**. La recursión solo trabaja sobre `[0, 1]` y `[6, 6]`.

## El resultado que importa

Con un número **constante** de claves distintas, Quicksort tricotómico pasa de
$O(n \log n)$ a $O(n)$. Es la variante que usa `java.util.Arrays.sort` para tipos
primitivos desde hace años, y la razón por la que ordenar un arreglo de banderas, notas o
categorías es tan rápido en la práctica.

## Para probarlo tú

En el laboratorio de esta semana, la **Parte 2B es opcional** y te guía para implementar
esta partición y medir la diferencia contra la versión de dos punteros sobre arreglos con
2, 5, 20 y 1000 claves distintas. La mejora aparece justamente donde la teoría la predice.

## Referencias

- Dijkstra, E. W. (1976). *A Discipline of Programming*. Prentice-Hall. Capítulo 14.
- Cormen et al. (CLRS), 4ª ed., cap. 7, problema 7-1 (partición de Hoare) y 7-2
  (Quicksort con claves repetidas).
- Sedgewick, R. & Wayne, K. *Algorithms*, 4ª ed., sección 2.3 — *Entropy-optimal sorting*.
