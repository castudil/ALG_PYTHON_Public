# 📖 Lectura 2: Propiedades del Heap — Más Allá del Código

**Curso:** Algoritmos y Estructuras de Datos — Universidad de Talca  
**Unidad 3:** Ordenamiento  
**Lectura complementaria a la Clase 6 — Binary Heap**

---

## ¿Por qué el heap NO es un árbol de búsqueda?

Esta pregunta confunde a muchos estudiantes que acaban de aprender árboles binarios de búsqueda (BST).

En un **BST**, la propiedad es: nodo izquierdo < raíz < nodo derecho. Esto permite buscar cualquier elemento en O(log n) recorriendo el árbol hacia izquierda o derecha.

En un **heap**, la propiedad es: padre ≥ hijos (o padre ≤ hijos para min-heap). Esta propiedad **solo habla de la relación vertical** entre padre e hijo. No dice nada sobre la relación entre nodos en diferentes ramas.

```
BST:            HEAP:
    5               9
   / \             / \
  3   7           7   8
 / \   \         / \   \
1   4   8       3   6   5

En el BST: 3 < 5 < 7 < 8 (se puede buscar)
En el heap: 7 y 8 son ambos menores que 9, pero no hay relación entre 7 y 8
```

Consecuencias prácticas:

- **Buscar un elemento específico en un heap es O(n)** — hay que revisar todos.
- El heap sacrifica la capacidad de búsqueda para ganar eficiencia en insert/delMax.
- La operación `contains(x)` en un heap no tiene ventaja sobre una búsqueda lineal.

---

## La invariante del heap expresada rigurosamente

La propiedad heap-order para un max-heap se define formalmente así:

> Para todo nodo en posición k (con 1 ≤ k ≤ n), si el hijo izquierdo existe (posición 2k ≤ n), entonces heap[k] ≥ heap[2k]. Si el hijo derecho existe (posición 2k+1 ≤ n), entonces heap[k] ≥ heap[2k+1].

Esta definición es local: solo habla de la relación entre un nodo y sus hijos inmediatos. Pero por transitividad, la raíz es mayor o igual que todos los elementos del heap.

**¿Por qué usar una propiedad local?** Porque es fácil de restaurar. Cuando insertamos o eliminamos, solo rompemos la propiedad en un lugar. `swim` y `sink` restauran la propiedad recorriendo un único camino del árbol (raíz a hoja o viceversa), ignorando todos los demás nodos.

---

## ¿Cuántos arreglos distintos representan el mismo heap?

Dado un conjunto de n elementos distintos, ¿cuántos arreglos distintos satisfacen la propiedad heap-order?

Para n = 3 elementos {1, 2, 3}: solo la raíz debe ser 3 (el máximo). Los dos hijos son 1 y 2 en algún orden → hay 2 heaps válidos: `[_, 3, 2, 1]` y `[_, 3, 1, 2]`.

Para n elementos, el número de heaps válidos es `n! / (producto de tamaños de subárboles)`. Para n = 10, hay miles de representaciones distintas.

Esto ilustra que el heap **no está completamente ordenado** — solo impone una estructura parcial de orden (*partial order*). Esta estructura parcial es suficiente para las operaciones que necesitamos, y es más fácil de mantener que un orden total.

---

## ¿Por qué la indexación empieza en 1?

La representación del heap en arreglo usa **indexación 1-based**: heap[0] no se usa, la raíz está en heap[1].

La razón es puramente aritmética. Con indexación 1-based:
- Padre de k: `k // 2`
- Hijos de k: `2k` y `2k+1`

Con indexación 0-based, las fórmulas son:
- Padre de k: `(k - 1) // 2`
- Hijos de k: `2k + 1` y `2k + 2`

Las fórmulas 0-based son ligeramente más complejas y más propensas a errores de implementación (off-by-one). Por eso Sedgewick y la mayoría de los textos clásicos usan 1-based.

En código Python real de producción, a veces se usa 0-based (la librería `heapq` de Python lo hace) para evitar desperdiciar una posición del arreglo. La disyuntiva es pureza del código vs claridad pedagógica.

---

## El costo real de swim y sink

### swim

En `swim`, en cada nivel solo hacemos **una comparación** (heap[k] > heap[k//2]) y un posible intercambio. La propiedad heap asegura que no hay que revisar "vecinos" — solo el camino directo hacia la raíz.

Número máximo de comparaciones: ⌊log₂ n⌋ (la altura del árbol).  
Número promedio de comparaciones (sobre inserciones aleatorias): ~log₂ n (casi siempre el elemento no llega a la raíz).

### sink

En `sink`, en cada nivel hacemos **dos comparaciones**: primero comparar los dos hijos para saber cuál es mayor, luego comparar el mayor con el nodo actual. Son 2 comparaciones por nivel.

Número máximo de comparaciones: 2⌊log₂ n⌋.  
Número promedio: Sedgewick demuestra que el promedio es ~2 log₂ n.

Esto explica por qué `delMax` es ligeramente más costoso que `insert`.

---

## ¿Por qué heapify con sink es O(n)?

La demostración intuitiva:

Hay aproximadamente n/2 hojas que no hacen ningún intercambio.  
Hay aproximadamente n/4 nodos en el penúltimo nivel, cada uno con sink de altura ≤ 1.  
Hay aproximadamente n/8 nodos con sink de altura ≤ 2.  
...  
Solo 1 nodo (la raíz) puede tener sink de altura ≤ ⌊log₂ n⌋.

El número total de intercambios es:

```
T(n) ≤ (n/4)·1 + (n/8)·2 + (n/16)·3 + ...
     = n · Σ k/2^(k+1)  (para k = 1, 2, 3, ...)
     = n · 1
     = n
```

La serie `Σ k/2^(k+1)` converge a 1, lo que nos da que `T(n) ≤ n`. Por eso heapify con sink es O(n).

En contraste, heapify con swim es O(n log n) porque los elementos cerca de la raíz pueden necesitar swim de altura O(log n), y hay O(n) de ellos en los niveles superiores.

---

## La conexión con partial orders y teoría de conjuntos

El heap implementa un *partial order* (orden parcial). En matemáticas, un orden parcial es una relación binaria que es:

1. **Reflexiva:** a ≥ a
2. **Antisimétrica:** si a ≥ b y b ≥ a, entonces a = b
3. **Transitiva:** si a ≥ b y b ≥ c, entonces a ≥ c

La diferencia con un *total order* (orden total, como en un arreglo ordenado) es que en un orden parcial, no todos los pares de elementos son comparables. En el heap, los nodos en distintas ramas no son necesariamente comparables.

El teorema de Dilworth, de la teoría de órdenes parciales, garantiza que cualquier orden parcial puede extenderse a un orden total — lo cual es exactamente lo que hace `heapsort`: convierte el orden parcial del heap en el orden total de un arreglo ordenado.

---

## Para reflexionar

1. El heap permite `max()` en O(1). ¿Qué operación adicional no puede hacer eficientemente? ¿Cómo afecta esto a las aplicaciones donde necesitas tanto el máximo como el mínimo?

2. La operación `decreaseKey(k, nuevo_valor)` (reducir la prioridad de un elemento en posición k) es crucial para Dijkstra. ¿Cómo la implementarías en un binary heap? ¿Cuál sería su complejidad?

3. Si tienes dos heaps de tamaños m y n, ¿cómo los fusionarías en un único heap? ¿Cuál sería la complejidad? (Pista: piensa en heapify).

---

## Referencias

- Sedgewick, R. & Wayne, K. (2011). *Algorithms*, 4ª ed. Addison-Wesley. Sección 2.4.
- Cormen et al. *Introduction to Algorithms* (CLRS), 4ª ed. Cap. 6.
- Knuth, D.E. (1998). *The Art of Computer Programming*, Vol. 3. Sección 5.2.3.
