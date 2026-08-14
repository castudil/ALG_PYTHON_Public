# 📖 Lectura 1: La Historia del Heap y las Priority Queues

**Curso:** Algoritmos y Estructuras de Datos — Universidad de Talca  
**Unidad 3:** Ordenamiento  
**Lectura complementaria a las Clases 6 y 7**

---

## El problema que nadie había resuelto bien

Antes de 1964, ordenar una lista tenía soluciones razonables. Pero el problema de mantener una colección dinámica donde siempre se puede extraer el mínimo (o máximo) eficientemente no tenía una buena respuesta.

Las opciones disponibles eran incómodas: un arreglo desordenado permite insertar en O(1) pero extraer el máximo cuesta O(n). Un arreglo ordenado permite extraer en O(1) pero insertar cuesta O(n). Para colas de prioridad en simulaciones de eventos, donde se insertan y extraen millones de elementos, ninguna de las dos era viable.

En 1964, un investigador llamado **J.W.J. Williams** publicó un paper de dos páginas que resolvió el problema de una vez. Lo tituló *"Algorithm 232: Heapsort"*.

---

## J.W.J. Williams y el heap

Williams trabajaba en el Computer Laboratory de la Universidad de Cambridge cuando diseñó la estructura de datos que llamó *heap* (montículo). La idea central era representar un árbol binario completo dentro de un arreglo ordinario, usando las relaciones aritméticas entre índices para navegar el árbol sin punteros.

El aporte de Williams fue doble:

1. La **estructura de datos heap** como representación implícita de un árbol binario completo en un arreglo.
2. **Heapsort** como algoritmo de ordenamiento que usa esa estructura.

Lo notable es que Williams casi no tuvo que escribir. El paper completo ocupó menos de dos páginas, incluyendo el pseudocódigo. La idea era tan elegante que se explicaba sola.

---

## Robert Floyd y el heapify lineal

Ese mismo año, 1964, **Robert W. Floyd** publicó una mejora crucial. Mientras Williams construía el heap insertando elementos uno a uno (O(n log n)), Floyd observó que podía construirse en O(n) aplicando la operación *sink* desde abajo hacia arriba.

Floyd publicó su técnica como *"Algorithm 245: Treesort 3"* — el nombre "Treesort 3" porque existían versiones anteriores menos eficientes.

La contribución de Floyd es a veces subestimada porque viene inmediatamente después de Williams, pero es fundamental: gracias a Floyd, la fase de construcción del heap cuesta O(n) en vez de O(n log n), lo que hace que Heapsort sea competitivo en la práctica.

Floyd también es conocido por el **algoritmo de Floyd-Warshall** para caminos mínimos en grafos, y por el **algoritmo de detección de ciclos de Floyd** (la tortuga y la liebre). Murió en 2001, siendo uno de los pioneros de la teoría de algoritmos.

---

## El heap y las simulaciones de eventos

La motivación real detrás de las priority queues no era el ordenamiento: era la **simulación de eventos discretos**.

En los años 60, los científicos comenzaban a simular sistemas complejos (colas en bancos, tráfico aéreo, circuitos electrónicos) en computadora. La técnica estándar era mantener una lista de eventos futuros ordenada por tiempo de ocurrencia, extrayendo siempre el evento más próximo y posiblemente insertando nuevos eventos como consecuencia.

Sin el heap, esta cola de eventos era O(n) por operación — inviable para simulaciones con millones de eventos. Con el heap, cada operación costaba O(log n), haciendo la simulación práctica.

Hoy, las priority queues siguen siendo la estructura de datos central en:

- **Simuladores de eventos discretos** (Cisco, Airbus, NASA los usan para modelar redes y sistemas)
- **Algoritmos de grafos:** Dijkstra y Prim son, en esencia, simulaciones donde el "siguiente evento" es el nodo más cercano o la arista de menor peso
- **Planificadores de sistemas operativos** (el scheduler de Linux usa una variante de heap para procesos en tiempo real)
- **Compresión Huffman** (la construcción del árbol usa una min-priority queue)

---

## El d-ary heap y las variantes modernas

El heap binario de Williams usa árboles con 2 hijos por nodo. Pero se puede generalizar: un **d-ary heap** tiene d hijos por nodo.

Para d = 4 (4-ary heap), el árbol es más ancho y bajo. Esto reduce la altura de O(log₂ n) a O(log₄ n), lo que significa menos intercambios en *sink*. La desventaja es que *sink* compara d hijos en cada nivel (más comparaciones por nivel).

La elección óptima de d depende del patrón de uso:

- Si se hacen muchos más `insert` que `delMax` → d grande es mejor (menos altura)
- Si `delMax` domina → d pequeño es mejor (menos comparaciones en *sink*)

En la práctica, los sistemas de bases de datos y planificadores suelen usar 4-ary o 8-ary heaps por motivos de caché: cuando d = 4, los d hijos de un nodo caben en la misma línea de caché que el padre, reduciendo los *cache misses*.

---

## El Fibonacci Heap: la frontera teórica

En 1984, **Michael Fredman** y **Robert Tarjan** diseñaron el *Fibonacci heap*, una estructura de datos con operaciones amortizadas aún más eficientes:

| Operación | Binary Heap | Fibonacci Heap |
|-----------|:-----------:|:--------------:|
| insert | O(log n) | **O(1) amortizado** |
| delMin | O(log n) | O(log n) amortizado |
| decreaseKey | O(log n) | **O(1) amortizado** |
| merge | O(n) | **O(1)** |

La operación `decreaseKey` (reducir la prioridad de un elemento existente) es crucial para Dijkstra. Con un Fibonacci heap, Dijkstra corre en O(E + V log V) en vez de O((E + V) log V) — una mejora significativa en grafos densos.

Sin embargo, el Fibonacci heap es notoriamente complicado de implementar y tiene constantes ocultas grandes. En benchmarks reales, el binary heap simple suele ganar hasta para grafos de millones de nodos, porque la constante de Fibonacci heap compensa la mejor asíntota.

---

## Para reflexionar

1. Williams publicó el heap en 1964. El problema de la priority queue existía antes. ¿Qué sugiere esto sobre la relación entre "tener un problema" y "diseñar la solución correcta"?

2. El Fibonacci heap es asintóticamente superior al binary heap para varias operaciones, pero el binary heap se usa más en la práctica. ¿Qué dice esto sobre el valor de la complejidad asintótica como única métrica de evaluación?

3. Las priority queues son esenciales en simulaciones, grafos y sistemas operativos. Piensa en un sistema que usas cotidianamente (tu teléfono, tu navegador, un servicio de streaming). ¿Dónde podría estar usando una priority queue?

---

## Referencias

- Williams, J.W.J. (1964). "Algorithm 232: Heapsort". *Communications of the ACM*, 7(6), 347–348.
- Floyd, R.W. (1964). "Algorithm 245: Treesort 3". *Communications of the ACM*, 7(12), 701.
- Fredman, M.L. & Tarjan, R.E. (1987). "Fibonacci Heaps and Their Uses in Improved Network Optimization Algorithms". *Journal of the ACM*, 34(3), 596–615.
- Sedgewick, R. & Wayne, K. (2011). *Algorithms*, 4ª ed. Addison-Wesley. Sección 2.4.
- Knuth, D.E. (1998). *The Art of Computer Programming*, Vol. 3, Sección 5.2.3.
