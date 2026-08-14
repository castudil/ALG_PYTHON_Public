# 📖 Lectura 3: Priority Queues en el Mundo Real

**Curso:** Algoritmos y Estructuras de Datos — Universidad de Talca  
**Unidad 3:** Ordenamiento  
**Lectura complementaria a las Clases 6 y 7**

---

## La estructura más ubicua que no ves

La priority queue es posiblemente la estructura de datos más usada en software de sistemas, y al mismo tiempo la más invisible para el usuario final. Cada vez que tu sistema operativo decide qué proceso ejecutar, cada vez que tu GPS calcula una ruta, y cada vez que Netflix decide en qué orden encodear los frames de un video, hay una priority queue trabajando silenciosamente.

---

## Algoritmo de Dijkstra y la min-priority queue

El algoritmo de Dijkstra para caminos mínimos en grafos es el uso más famoso de la priority queue en algoritmos.

La idea central de Dijkstra es: "el próximo nodo a procesar es siempre el nodo no visitado más cercano al origen". Esto es exactamente la semántica de `delMin()` de una priority queue.

```python
# Dijkstra simplificado
def dijkstra(grafo, origen):
    distancias = {nodo: float('inf') for nodo in grafo}
    distancias[origen] = 0
    pq = MinHeap()
    pq.insert((0, origen))   # (distancia, nodo)

    while not pq.isEmpty():
        dist, u = pq.delMin()   # siempre el más cercano
        for v, peso in grafo[u]:
            nueva_dist = dist + peso
            if nueva_dist < distancias[v]:
                distancias[v] = nueva_dist
                pq.insert((nueva_dist, v))   # puede insertarse varias veces

    return distancias
```

Con un binary heap, Dijkstra corre en O((V + E) log V). Para un grafo con millones de nodos y aristas (como las rutas de Google Maps), esto es la diferencia entre una respuesta en milisegundos y una que tarde minutos.

---

## El algoritmo de Prim y los árboles de expansión mínima

El algoritmo de Prim para árboles de expansión mínima (MST) es estructuralmente idéntico a Dijkstra, con la diferencia de que la prioridad es el peso de la arista que conecta al árbol, no la distancia acumulada.

MST tiene aplicaciones directas en diseño de redes: la red de fibra óptica más barata que conecta n ciudades, el árbol de distribución eléctrica de mínimo costo, el cableado mínimo de un circuito impreso.

---

## Compresión Huffman

La codificación Huffman asigna códigos binarios más cortos a los caracteres más frecuentes. El algoritmo de construcción del árbol de Huffman usa una min-priority queue:

```
Frecuencias: a=5, b=2, c=1, d=3, e=4

Paso 1: PQ = [(1,c), (2,b), (3,d), (4,e), (5,a)]

Iteración 1: extraer los dos mínimos (c=1, b=2), crear nodo cb=3
             PQ = [(3,d), (3,cb), (4,e), (5,a)]

Iteración 2: extraer (d=3, cb=3), crear nodo dcb=6
             PQ = [(4,e), (5,a), (6,dcb)]
...
```

Cada `delMin` cuesta O(log n) y hacemos n-1 iteraciones → O(n log n) total para construir el árbol Huffman. Sin priority queue, sería O(n²).

Los formatos de compresión como ZIP, GZIP y DEFLATE (usado en HTTP/1.1) usan variantes de Huffman como parte de su pipeline de compresión.

---

## Planificadores de sistemas operativos

El scheduler de un sistema operativo decide qué proceso o hilo ejecutar en cada momento. Los schedulers modernos usan priority queues con múltiples niveles de prioridad.

**Linux CFS (Completely Fair Scheduler):** Usa un árbol rojo-negro (una variante de BST balanceado), pero su interfaz es equivalente a una priority queue: "dame el proceso con menor tiempo de CPU acumulado". El árbol rojo-negro se prefiere sobre el heap porque permite recorrer los procesos en orden, algo que el scheduler necesita para ajustar prioridades dinámicamente.

**Real-time schedulers:** Los schedulers de tiempo real (para sistemas embebidos, controladores industriales, sistemas de aviónica) usan heaps simples porque las garantías de tiempo de O(log n) por operación son predecibles y verificables formalmente.

---

## `heapq` de Python: la priority queue de la librería estándar

Python incluye el módulo `heapq` que implementa un min-heap sobre listas ordinarias con indexación 0-based.

```python
import heapq

# Crear una priority queue (min-heap)
pq = []
heapq.heappush(pq, 5)
heapq.heappush(pq, 2)
heapq.heappush(pq, 8)
heapq.heappush(pq, 1)

print(heapq.heappop(pq))   # → 1 (el mínimo)
print(heapq.heappop(pq))   # → 2

# Convertir lista existente en heap en O(n) (heapify)
datos = [5, 3, 8, 1, 7, 2, 9]
heapq.heapify(datos)
print(datos)   # → [1, 3, 2, 5, 7, 8, 9] (representación 0-based del heap)

# nlargest y nsmallest con heap internamente
print(heapq.nlargest(3, datos))   # → [9, 8, 7]
print(heapq.nsmallest(3, datos))  # → [1, 2, 3]
```

**Detalle 0-based de `heapq`:** Para el nodo en posición `k` (0-based):
- Padre: `(k - 1) // 2`
- Hijo izquierdo: `2*k + 1`
- Hijo derecho: `2*k + 2`

**Priority queue con elementos compuestos:** Para prioridades con datos adjuntos, se usan tuplas. Python compara tuplas lexicográficamente:

```python
# (prioridad, dato) — se ordena por prioridad primero
heapq.heappush(pq, (3, 'tarea C'))
heapq.heappush(pq, (1, 'tarea A'))
heapq.heappush(pq, (2, 'tarea B'))
heapq.heappop(pq)  # → (1, 'tarea A')
```

**`queue.PriorityQueue` vs `heapq`:** Python también tiene `queue.PriorityQueue`, que es thread-safe (usa locks internamente). Para uso en un solo hilo, `heapq` es más rápida. Para programas con múltiples hilos, `PriorityQueue` evita condiciones de carrera.

---

## K elementos más grandes/pequeños: `nlargest` y `nsmallest`

Un caso de uso clásico: dado un stream de millones de datos, encontrar los K más grandes.

La solución naïve: guardar todos, ordenar, tomar los K primeros → O(n log n).  
La solución con heap: mantener un min-heap de tamaño K.

```python
def top_k(stream, k):
    """
    Retorna los k elementos más grandes del stream.
    Complejidad: O(n log k) — mucho mejor que O(n log n) si k << n
    """
    import heapq
    heap = []
    for x in stream:
        if len(heap) < k:
            heapq.heappush(heap, x)
        elif x > heap[0]:     # heap[0] = mínimo del heap
            heapq.heapreplace(heap, x)  # pop + push en O(log k)
    return sorted(heap, reverse=True)

# Ejemplo: top 5 de 1,000,000 elementos
import random
datos = [random.randint(0, 10**9) for _ in range(10**6)]
print(top_k(datos, 5))  # O(n log 5) ≈ O(n), no O(n log n)
```

Esta técnica se usa en sistemas de análisis de logs (top-K URLs más visitadas), motores de búsqueda (top-K documentos más relevantes), y sistemas de recomendación (top-K ítems para recomendar).

---

## Heapsort en la práctica: dónde se usa realmente

Heapsort puro rara vez se usa solo, pero es componente de algoritmos híbridos importantes.

**Introsort** (introspective sort, David Musser, 1997): es el algoritmo usado en C++ `std::sort`. Combina:
- Quicksort (rápido en la práctica, O(n log n) promedio)
- Heapsort (fallback cuando la recursión de Quicksort supera 2·log₂n niveles, señal de peor caso)
- Insertion Sort (para subarreglos pequeños, < 16 elementos)

El resultado: rápido como Quicksort normalmente, pero con garantía O(n log n) como Heapsort.

**PDQsort** (pattern-defeating quicksort, 2021): la evolución de Introsort usada en Rust y otras implementaciones modernas. Agrega detección de patrones (datos casi ordenados, muchos duplicados) para elegir la estrategia óptima.

---

## Para reflexionar

1. `heapq` de Python implementa un **min-heap**. Para usarlo como max-heap (Priority Queue que extrae el máximo), una técnica común es insertar valores negados: `heapq.heappush(pq, -valor)`. ¿Qué limitaciones tiene esta técnica? ¿Cuándo falla?

2. Dijkstra con binary heap corre en O((V + E) log V). Con un Fibonacci heap correría en O(E + V log V). Para un grafo disperso (E ≈ V), ambas son O(V log V). Para un grafo denso (E ≈ V²), el Fibonacci heap gana. ¿Cuándo en la práctica los grafos son tan densos como para que valga la pena usar Fibonacci heap?

3. El módulo `heapq` de Python no tiene una operación `decreaseKey` (cambiar la prioridad de un elemento existente). Esta limitación hace que la implementación de Dijkstra con `heapq` inserte duplicados (el mismo nodo con distintas prioridades). ¿Por qué esta limitación existe y cómo afecta al rendimiento en grafos con muchas aristas?

---

## Referencias

- Van Rossum, G. et al. Documentación de `heapq`. Python 3 Standard Library. https://docs.python.org/3/library/heapq.html
- Musser, D. (1997). "Introspective Sorting and Selection Algorithms". *Software: Practice and Experience*, 27(8), 983–993.
- Cormen et al. *Introduction to Algorithms* (CLRS), 4ª ed. Caps. 6 y 24 (Dijkstra).
- Sedgewick, R. & Wayne, K. (2011). *Algorithms*, 4ª ed. Secciones 2.4, 4.3 y 4.4.
