# 📖 Lectura 1: La Historia de Quicksort

**Curso:** Algoritmos y Estructuras de Datos — Universidad de Talca  
**Unidad 3:** Ordenamiento  
**Lectura complementaria a la Clase 5**

---

## El algoritmo más influyente de la historia de la computación

En 1959, un joven matemático británico de 25 años llamado **Charles Antony Richard Hoare** — conocido como Tony Hoare — fue enviado a Moscú como parte de un proyecto de intercambio académico para aprender ruso. Allí, mientras estudiaba traducción automática de idiomas, se encontró con un problema concreto: necesitaba ordenar palabras en un diccionario.

Su solución a ese problema cambiaría la historia de la computación.

---

## El problema que dio origen a Quicksort

El programa de traducción necesitaba ordenar una lista de palabras rusas para buscarlas eficientemente. Los algoritmos de ordenamiento que Hoare conocía — Bubble Sort, Selection Sort, Insertion Sort — eran O(n²), lo que los hacía inaceptablemente lentos para diccionarios grandes.

Hoare tuvo una intuición brillante:

> *"Si encuentro un elemento que ya está en su posición correcta, puedo ordenar el resto de forma independiente a ambos lados."*

Esta idea simple — encontrar un **pivot** y particionar el arreglo alrededor de él — es el corazón de Quicksort.

---

## La publicación y el nombre

Hoare publicó el algoritmo en 1962 en *The Computer Journal* bajo el título "Quicksort". El nombre no era modestia: el algoritmo era genuinamente rápido para los estándares de la época.

El paper original es notable por varias razones:

1. **Complejidad del análisis:** Hoare demostró matemáticamente que el caso promedio es O(n log n), lo cual requirió análisis probabilístico no trivial para la época.

2. **Recursión:** Quicksort fue uno de los primeros algoritmos prácticos en usar recursión, que en 1962 era una idea relativamente nueva en programación.

3. **In-place:** A diferencia de Merge Sort, Quicksort ordena sin usar arreglos auxiliares, lo cual era crítico cuando la RAM medía en kilobytes.

---

## Los dos esquemas de partición

El paper original de Hoare describe lo que hoy llamamos la **partición de Hoare** — con dos punteros que se mueven desde los extremos hacia el centro.

### Un esquema que verás en otros libros

Años después, **Nico Lomuto** (programador en los laboratorios DEC) describió una variante más simple, con un solo puntero que recorre el arreglo de izquierda a derecha y el pivote al final. Apareció en *Programming Pearls* de Jon Bentley (1986) y en los apuntes que se convirtieron en *Introduction to Algorithms* (CLRS), así que es la que encontrarás en buena parte de la bibliografía y en la mayoría de los tutoriales en línea.

**En este curso no la usamos.** Vale la pena saber que existe para que no te confundas al leer CLRS o buscar en internet, pero la razón de preferir el esquema de dos punteros es concreta:

| | Intercambios por llamada (promedio) |
|---|---|
| Un solo puntero (Lomuto) | ~n/2 |
| Dos punteros (Hoare) | ~n/6 |

Unas tres veces menos trabajo. La versión de un puntero es más corta de escribir, pero paga ese ahorro en cada ejecución.

> ⚠️ **Al buscar ayuda en línea:** si el código que encuentras toma el pivote del **último** elemento y usa un solo índice que avanza, es el esquema de Lomuto. El nuestro toma el pivote del **primer** elemento y mueve dos punteros en direcciones opuestas. No los mezcles: las llamadas recursivas son distintas.

---

## Quicksort en el mundo real

Quicksort no es solo teoría. Es uno de los algoritmos más usados en software de producción:

**C estándar (libc):** La función `qsort()` usa Quicksort (con optimizaciones). Toda la cadena de herramientas de Unix/Linux la usa.

**Java:** `Arrays.sort()` para tipos primitivos usa una variante llamada **Dual-Pivot Quicksort**, diseñada por Vladimir Yaroslavskiy (2009), que usa dos pivots en vez de uno. Es más rápida en promedio.

**C++ STL:** `std::sort()` usa **Introsort**, una combinación de Quicksort, Heapsort e Insertion Sort. Introsort empieza con Quicksort, pero si detecta que la recursión se está volviendo muy profunda (señal de peor caso), cambia a Heapsort para garantizar O(n log n).

**Python:** `sorted()` usa **Timsort** (Merge Sort + Insertion Sort), no Quicksort. La razón es que `sorted()` debe ser **estable** por especificación del lenguaje.

---

## Tony Hoare hoy

La historia tiene un final interesante. Tony Hoare no se quedó solo con Quicksort. Continuó siendo una figura central en la teoría de la computación:

- Inventó la **lógica de Hoare** (1969), el fundamento teórico de la verificación formal de programas.
- Diseñó **CSP (Communicating Sequential Processes)**, que influyó en el lenguaje Go.
- Recibió el **Premio Turing** en 1980.
- En 2009, en una conferencia, se disculpó públicamente por haber inventado el puntero nulo (null reference), al que llamó "mi error de mil millones de dólares".

---

## Para reflexionar

1. Quicksort tiene peor caso O(n²), pero en la práctica supera a Merge Sort que tiene O(n log n) garantizado. ¿Qué nos dice esto sobre el valor de la notación O-grande como única métrica de rendimiento?

2. Los diseñadores de Java, C++ y Python tomaron decisiones distintas sobre qué algoritmo de ordenamiento usar en su librería estándar. ¿Qué prioridades distintas revelan esas decisiones?

3. Hoare diseñó Quicksort para un problema de traducción en 1959. ¿Qué problemas actuales podrían motivar el diseño de nuevos algoritmos de ordenamiento?

---

## Referencias

- Hoare, C.A.R. (1962). "Quicksort". *The Computer Journal*, 5(1), 10–16.
- Bentley, J. (2000). *Programming Pearls* (2ª ed.). Addison-Wesley.
- Knuth, D.E. (1998). *The Art of Computer Programming, Vol. 3: Sorting and Searching* (2ª ed.). Addison-Wesley. Sección 5.2.2.
- Sedgewick, R. (1977). "Quicksort is optimal". Lecture Notes. Princeton University.
