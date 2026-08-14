# 📖 Lectura 2: Estrategias de Pivot en Quicksort

**Curso:** Algoritmos y Estructuras de Datos — Universidad de Talca  
**Unidad 3:** Ordenamiento  
**Lectura complementaria a la Clase 5**

---

## La decisión más importante de Quicksort

Si le preguntaras a un desarrollador experimentado cuál es el aspecto más crítico de implementar Quicksort correctamente, la respuesta casi siempre sería: **la elección del pivot**.

La razón es simple: la complejidad de Quicksort depende directamente de qué tan bien el pivot divide el arreglo en dos partes.

---

## ¿Por qué el pivot importa tanto?

Recuerda la ecuación de recurrencia de Quicksort cuando el pivot divide en proporción `k:(n-k-1)`:

$$T(n) = T(k) + T(n-k-1) + O(n)$$

Dos extremos:

**Partición perfecta (k = n/2):**
$$T(n) = 2T(n/2) + O(n) \Rightarrow O(n \log n)$$

**Partición degenerada (k = 0 siempre):**
$$T(n) = T(0) + T(n-1) + O(n) = T(n-1) + O(n) \Rightarrow O(n^2)$$

La diferencia no es pequeña: para n = 1.000.000, la diferencia entre O(n log n) y O(n²) es la diferencia entre 0.02 segundos y 16 minutos.

---

## Estrategia 1: Primer o último elemento

La estrategia más simple: elegir `arr[0]` o `arr[n-1]` como pivot.

**Ventaja:** Cero costo adicional.

**Desventaja crítica:** El peor caso ocurre en entradas muy comunes:
- Arreglo ya ordenado ascendentemente → O(n²)
- Arreglo ya ordenado descendentemente → O(n²)
- Arreglo con todos los elementos iguales → O(n²)

```
Arreglo: [1, 2, 3, 4, 5, 6, 7]
Pivot = 7

Partición: [1, 2, 3, 4, 5, 6] | [7] | []
                                   ↑
                         pivot en posición final
                         pero: subproblema de tamaño n-1
```

Este antipatrón es tan común (los datos del mundo real tienden a llegar parcialmente ordenados) que en la práctica esta estrategia es inaceptable para uso general.

---

## Estrategia 2: Elemento del medio

Elegir `arr[n/2]` como pivot.

**Ventaja:** Funciona bien en arreglos ya ordenados.

**Desventaja:** Fácilmente atacable con una entrada "adversarial" cuidadosamente construida.

---

## Estrategia 3: Pivot aleatorio

Elegir un índice aleatorio en `[inicio, fin]` y usar ese elemento como pivot.

```python
def pivot_aleatorio(arr, inicio, fin):
    idx = random.randint(inicio, fin)
    arr[idx], arr[lo] = arr[lo], arr[idx]  # mover al frente: la partición toma arr[lo]
    return arr[fin]
```

**Ventaja:** El peor caso sigue existiendo teóricamente, pero requeriría que el generador de números aleatorios conspire contra nosotros en **cada una** de las n llamadas recursivas. La probabilidad de esto es astronomicamente pequeña.

**El análisis formal:**  
Para una permutación aleatoria del pivot, la probabilidad de elegir el pivot que produce la peor partición es 1/n. La esperanza matemática del costo es:

$$E[T(n)] = \frac{1}{n} \sum_{k=0}^{n-1} (E[T(k)] + E[T(n-k-1)]) + O(n) = O(n \log n)$$

**Desventaja:** Llama a `random.randint()` en cada nivel de recursión, lo cual tiene un costo no despreciable en implementaciones de alto rendimiento.

---

## Estrategia 4: Mediana de tres

Elegir como pivot la **mediana** de tres candidatos: `arr[inicio]`, `arr[mid]`, `arr[fin]`.

```python
def mediana_de_tres(arr, inicio, fin):
    mid = (inicio + fin) // 2
    # Ordenar los tres candidatos in-place
    if arr[inicio] > arr[mid]:
        arr[inicio], arr[mid] = arr[mid], arr[inicio]
    if arr[inicio] > arr[fin]:
        arr[inicio], arr[fin] = arr[fin], arr[inicio]
    if arr[mid] > arr[fin]:
        arr[mid], arr[fin] = arr[fin], arr[mid]
    # arr[mid] es la mediana; ponerla en arr[lo], que es de donde toma el pivote
    arr[mid], arr[fin] = arr[fin], arr[mid]
    return arr[fin]
```

**Ventaja 1 — Elimina casos degenerados comunes:**  
La mediana de tres elementos nunca es el mínimo ni el máximo del arreglo completo, pero tiende a estar cerca del centro. Para arreglos ya ordenados, la mediana de {arr[0], arr[mid], arr[fin]} siempre es `arr[mid]`, lo que produce una partición perfecta.

**Ventaja 2 — Mejora empírica real:**  
La mediana de tres reduce el número de comparaciones aproximadamente en un 5-10% respecto al pivot aleatorio para datos en distribución uniforme.

**Desventaja:** El peor caso teórico sigue siendo O(n²), aunque requiere una entrada adversarial más sofisticada.

---

## Estrategia 5: Mediana de medianas (algoritmo de selección lineal)

Para garantizar matemáticamente O(n log n) en el peor caso, existe una estrategia llamada **mediana de medianas** (también conocida como el algoritmo de Blum-Floyd-Pratt-Rivest-Tarjan, 1973).

La idea es:
1. Dividir el arreglo en grupos de 5 elementos
2. Encontrar la mediana de cada grupo (Insertion Sort en grupos de 5)
3. Encontrar recursivamente la mediana de esas medianas
4. Usar esa mediana-de-medianas como pivot

El resultado es que el pivot siempre queda entre el percentil 30 y el 70 del arreglo, garantizando particiones con al menos 30%-70% de balance.

**El costo:** La selección del pivot toma O(n), pero con una constante grande. En la práctica, Quicksort con mediana-de-medianas es **más lento** que Quicksort con mediana-de-tres, aunque tiene mejores garantías teóricas.

Por esta razón, mediana-de-medianas es más relevante para el **algoritmo de selección** (encontrar el k-ésimo elemento) que para Quicksort en producción.

---

## La solución industrial: Introsort

Los diseñadores de C++ STL enfrentaron en los años 90 el dilema: Quicksort es rápido en promedio pero puede degradarse a O(n²). Merge Sort es O(n log n) garantizado pero usa O(n) memoria extra.

La solución fue **Introsort** (David Musser, 1997):

```
introsort(arr, profundidad_maxima):
    si len(arr) <= 16:
        insertion_sort(arr)  # Insertion Sort es mejor para n pequeño
    sino si profundidad_actual > profundidad_maxima:
        heapsort(arr)         # Cambiar a Heapsort si Quicksort se profundiza demasiado
    sino:
        pivot = mediana_de_tres(arr)
        particionar y llamar recursivamente
```

`profundidad_maxima` se define típicamente como `2 * log2(n)`.

**Resultado:** Introsort tiene el rendimiento promedio de Quicksort Y la garantía de peor caso O(n log n) de Heapsort. Es lo mejor de ambos mundos.

`std::sort()` de C++ usa Introsort. `Arrays.sort()` de Java para primitivos usa **Dual-Pivot Quicksort** (dos pivots, tres particiones).

---

## Dual-Pivot Quicksort

Vladimir Yaroslavskiy propuso en 2009 una variante con dos pivots `p1 < p2`:

```
Partición produce tres partes:
[elementos < p1] | [p1 <= elementos <= p2] | [elementos > p2]
```

El análisis muestra que Dual-Pivot hace en promedio **~1.9n log n comparaciones** vs las ~2.19n log n del Quicksort clásico. La mejora es real y medible en benchmarks.

Java adoptó esta implementación en Java 7 y la mantiene hoy.

---

## Resumen comparativo

| Estrategia | Implementación | Peor caso | Promedio | Usado en |
|-----------|---------------|-----------|----------|---------|
| Primer/último elemento | Trivial | O(n²) frecuente | O(n log n) | Ejercicios académicos únicamente |
| Elemento del medio | Trivial | O(n²) para ciertos inputs | O(n log n) | Educativo |
| Pivot aleatorio | `random.randint` | O(n²) improbable | O(n log n) | Cuando se desconfía del input |
| Mediana de 3 | 3 comparaciones extra | O(n²) muy raro | ~5-10% mejor que aleatorio | C++ (Introsort), Python (Timsort usa merge pero QS en variantes) |
| Dual-Pivot | 2 pivots, 3 particiones | O(n²) muy raro | ~1.9n log n | Java `Arrays.sort()` |
| Mediana de medianas | O(n) extra | **O(n log n) garantizado** | O(n log n) mayor constante | Algoritmo de selección, análisis teórico |
| Introsort | QS + Heapsort | **O(n log n) garantizado** | ~Quicksort | C++ `std::sort()` |

---

## Para reflexionar

1. Si la mediana de tres es mejor que el pivot aleatorio, ¿por qué algunas implementaciones siguen prefiriendo el pivot aleatorio?

2. Introsort garantiza O(n log n) en el peor caso. ¿Por qué los libros de texto siguen presentando Quicksort como un algoritmo O(n log n) en promedio con peor caso O(n²), en vez de hablar directamente de Introsort?

3. La elección del pivot en producción (Dual-Pivot en Java, Mediana-3 en C++) fue determinada empíricamente con benchmarks, no solo teóricamente. ¿Qué dice esto sobre la relación entre teoría y práctica en algoritmos?

---

## Referencias

- Musser, D.R. (1997). "Introspective Sorting and Selection Algorithms". *Software: Practice and Experience*, 27(8), 983–993.
- Yaroslavskiy, V. (2009). "Dual-Pivot Quicksort". OpenJDK mailing list. http://cr.openjdk.java.net/~martin/webrevs/openjdk7/timsort/raw_files/new/src/share/classes/java/util/DualPivotQuicksort.java
- Blum, M., Floyd, R., Pratt, V., Rivest, R., Tarjan, R. (1973). "Time bounds for selection". *Journal of Computer and System Sciences*, 7(4), 448–461.
- Sedgewick, R. (1977). "Quicksort". *PhD Thesis*. Stanford University.
