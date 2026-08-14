# 📖 Lectura 3: Quicksort en la Práctica — Librerías Reales

**Curso:** Algoritmos y Estructuras de Datos — Universidad de Talca  
**Unidad 3:** Ordenamiento  
**Lectura complementaria a la Clase 5**

---

## ¿Cómo ordena tu computador realmente?

Cuando escribes `sorted([3, 1, 4, 1, 5])` en Python, o `Arrays.sort(arr)` en Java, o `std::sort(v)` en C++, ¿qué algoritmo se ejecuta realmente? La respuesta es más interesante que simplemente "Quicksort" o "Merge Sort".

---

## Python: Timsort

### ¿Por qué no Quicksort?

Python podría haber usado Quicksort. Es rápido. Pero Python optó por un algoritmo diferente llamado **Timsort**, diseñado por Tim Peters en 2002. La razón principal fue la **estabilidad**.

Python garantiza que `sorted()` y `list.sort()` son **estables**: si dos elementos son iguales según el criterio de comparación, mantienen su orden relativo original. Esto es crítico para usos como:

```python
# Ordenar estudiantes primero por apellido, luego por nota
# Un sort estable permite hacer esto en dos pasos:
estudiantes.sort(key=lambda x: x.nota)         # primero por nota
estudiantes.sort(key=lambda x: x.apellido)      # luego por apellido
# El resultado final respeta ambos criterios porque el sort es estable
```

Quicksort no es estable sin modificaciones significativas.

### ¿Qué es Timsort?

Timsort es un híbrido de Merge Sort e Insertion Sort, diseñado para explotar el hecho de que los datos del mundo real rara vez son aleatorios — suelen tener **runs**: secuencias ya ordenadas.

El algoritmo:

1. **Detectar runs naturales:** Recorre el arreglo buscando secuencias ya ordenadas (ascendente o descendente). Un arreglo como `[1, 2, 5, 8, 3, 4, 7, 9]` tiene dos runs: `[1, 2, 5, 8]` y `[3, 4, 7, 9]`.

2. **Extender runs cortos:** Si un run es más corto que `minrun` (entre 32 y 64 elementos, calculado dinámicamente), se extiende usando Insertion Sort. Insertion Sort es O(n²) en general pero muy eficiente para insertar elementos en una secuencia ya casi ordenada.

3. **Merge de runs:** Los runs se fusionan usando Merge Sort, con optimizaciones para detectar cuando un run "domina" al otro (galloping mode).

### Rendimiento de Timsort

| Caso | Complejidad | Descripción |
|------|-------------|-------------|
| Mejor | O(n) | Datos ya ordenados (un solo run) |
| Promedio | O(n log n) | Datos aleatorios |
| Peor | O(n log n) | Siempre garantizado |
| Memoria | O(n) | Necesita arreglo auxiliar |

Para datos del mundo real (parcialmente ordenados), Timsort típicamente es más rápido que Quicksort puro.

### Timsort fuera de Python

- **Java:** Usa Timsort para `Arrays.sort()` de objetos (tipos de referencia) desde Java 7.
- **Android:** Usa Timsort en el framework.
- **Swift:** Usa una variante de Timsort.

---

## Java: Dual-Pivot Quicksort + Timsort

Java es interesante porque usa **algoritmos distintos** dependiendo del tipo:

### Para primitivos: Dual-Pivot Quicksort

`Arrays.sort(int[])`, `Arrays.sort(double[])`, etc. usan **Dual-Pivot Quicksort** (Vladimir Yaroslavskiy, 2009).

La idea es usar **dos pivots** en vez de uno:

```
Dado arr[inicio..fin] con pivots p1 <= p2:

Resultado de la partición:
[ elementos < p1 | p1 | p1 <= elem <= p2 | p2 | elementos > p2 ]
                                ↑                    ↑
                           subproblema 2       subproblema 3

Se crean 3 subproblemas en vez de 2
```

Con dos pivots y tres particiones, el análisis muestra que en promedio se necesitan ~1.9n ln n comparaciones, vs ~2.19n ln n con un pivot. En benchmarks con datos uniformes, es ~10% más rápido que el mejor Quicksort de un pivot.

**¿Por qué para primitivos y no para objetos?**  
Los primitivos en Java no tienen identidad de objeto — dos ints con valor 5 son indistinguibles. Por lo tanto, la estabilidad no importa y se puede usar el algoritmo más rápido.

### Para objetos: Timsort

`Arrays.sort(Object[])` y `Collections.sort()` usan Timsort porque los objetos pueden ser "iguales" según el comparador pero distintos en identidad, y el orden relativo puede importar al programador.

---

## C++: Introsort

`std::sort()` en la mayoría de implementaciones de la STL (libstdc++, libc++, MSVC) usa **Introsort**.

### La estructura de Introsort

```
introsort(arr, profundidad_maxima):
    mientras len(arr) > 16:
        si profundidad_actual > profundidad_maxima:
            heapsort(arr)  ← garantía de peor caso
            return
        pivot = mediana_de_tres(arr[0], arr[mid], arr[fin])
        particionar con pivot
        llamar recursivamente
        profundidad_actual++
    insertion_sort(arr)  ← para subproblemas pequeños
```

`profundidad_maxima` = 2 × ⌊log₂(n)⌋

### ¿Por qué este diseño?

- **Quicksort** para el caso promedio: rápido, cache-friendly, in-place
- **Heapsort** como fallback: garantiza O(n log n) si Quicksort "se pierde" (árbol muy profundo = señal de mal pivot)
- **Insertion Sort** para n pequeño: para subproblemas de tamaño ≤ 16, el overhead de Quicksort supera el beneficio

### Rendimiento garantizado

| Caso | Complejidad | Memoria |
|------|-------------|---------|
| Cualquier caso | O(n log n) | O(log n) |

El peor caso O(n log n) está garantizado matemáticamente: si la profundidad supera 2 log₂(n), Heapsort se activa y garantiza terminación en O(n log n).

---

## C: qsort()

La función `qsort()` de la librería estándar de C es una de las funciones más antiguas y ampliamente usadas del mundo.

```c
void qsort(void *base, size_t nmemb, size_t size,
           int (*compar)(const void *, const void *));
```

Hay una diferencia filosófica importante con C++: `qsort()` recibe un puntero de función para la comparación, lo cual hace imposible el inlining en tiempo de compilación. Esto le cuesta aproximadamente 3-5× de rendimiento respecto a `std::sort()`, que usa templates y permite inlining.

Por esta razón, en código C++ moderno **siempre** se prefiere `std::sort()` a `qsort()`.

---

## Rust: Pattern-defeating Quicksort (pdqsort)

Rust usa un algoritmo moderno llamado **pdqsort** (Pattern-defeating Quicksort, Orson Peters, 2021).

pdqsort combina:
- Pivot por mediana de tres (con variante de 9 elementos para n grande)
- Detección de patrones: si detecta que los datos tienen estructura (ya ordenados, muchos duplicados, etc.), cambia de estrategia
- Heapsort como fallback (como Introsort)
- Insertion Sort para n pequeño

pdqsort supera consistentemente a Introsort en benchmarks con datos reales, especialmente para datos con estructura.

---

## Tabla resumen: ¿Qué usa quién?

| Lenguaje/Entorno | Función | Algoritmo | Estable | Peor caso |
|-----------------|---------|-----------|---------|-----------|
| Python | `sorted()`, `list.sort()` | Timsort | ✅ Sí | O(n log n) |
| Java (primitivos) | `Arrays.sort(int[])` | Dual-Pivot Quicksort | ❌ No | O(n log n) promedio |
| Java (objetos) | `Arrays.sort(Object[])` | Timsort | ✅ Sí | O(n log n) |
| C++ | `std::sort()` | Introsort | ❌ No | O(n log n) |
| C++ | `std::stable_sort()` | Merge Sort adaptativo | ✅ Sí | O(n log n) |
| C | `qsort()` | Varía (típ. Quicksort) | ❌ No | O(n²) posible |
| Rust | `.sort()` | Timsort (merge-based) | ✅ Sí | O(n log n) |
| Rust | `.sort_unstable()` | pdqsort | ❌ No | O(n log n) |

---

## Lecciones para el programador

**1. No implementes tu propio sort de propósito general.**  
Las implementaciones en librerías estándar tienen décadas de optimización, pruebas exhaustivas y aprovechan características del hardware (SIMD, prefetching). Tu implementación de Quicksort será correcta pero probablemente 2-10× más lenta.

**2. Usa `sort()` por defecto; `stable_sort()` cuando necesites estabilidad.**  
En C++, `std::sort()` es más rápido que `std::stable_sort()` porque no necesita memoria extra. Usa `stable_sort()` solo cuando la estabilidad importe.

**3. El tipo de datos importa.**  
Si ordenas objetos con comparador personalizado y la estabilidad importa: usa `stable_sort()` o asegúrate de que tu lenguaje garantiza estabilidad.

**4. Para datos casi ordenados, Timsort/Merge Sort puede superar a Quicksort.**  
Si sabes que tus datos tendrán structure (ej: logs de sistema ordenados por tiempo, con pequeñas perturbaciones), considera algoritmos que exploten ese pattern.

---

## Para reflexionar

1. Rust tiene dos funciones: `.sort()` (estable, Timsort) y `.sort_unstable()` (inestable, pdqsort). ¿Por qué es un buen diseño ofrecer ambas explícitamente? ¿Qué problema resuelve esto que C++ no resuelve bien?

2. Java usa Dual-Pivot Quicksort para primitivos pero Timsort para objetos. Esta distinción existe en el lenguaje, no solo en la implementación. ¿Qué dice esto sobre el diseño de APIs y la relación entre semántica del lenguaje y rendimiento?

3. La función `qsort()` de C no puede garantizar rendimiento óptimo porque recibe la función de comparación como puntero (impide optimización en compilación). ¿Cómo resuelve C++ este problema con templates? ¿Y por qué Python, siendo interpretado, no sufre el mismo problema de la misma manera?

---

## Referencias

- Peters, T. (2002). "Timsort". Python source code and documentation. https://hg.python.org/cpython/file/tip/Objects/listsort.txt
- Yaroslavskiy, V. (2009). "Dual-Pivot Quicksort". OpenJDK proposal.
- Peters, O. (2021). "Pattern-defeating Quicksort". https://github.com/orlp/pdqsort
- Musser, D.R. (1997). "Introspective Sorting and Selection Algorithms". *Software: Practice and Experience*, 27(8).
- ISO/IEC 14882 (C++ Standard), Section 25.4: Sorting and related operations.
