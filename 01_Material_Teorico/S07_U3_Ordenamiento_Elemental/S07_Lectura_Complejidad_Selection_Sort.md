# Análisis de la Complejidad del Algoritmo Selection Sort

El algoritmo de **Ordenamiento por Selección (Selection Sort)** es conocido por su simplicidad. Sin embargo, esa simplicidad tiene un costo en términos de eficiencia. A continuación, desglosamos de dónde proviene su complejidad tanto temporal como espacial.

---

## 1. Complejidad Temporal: $O(n^2)$

La complejidad del Selection Sort se deriva de su estructura de **bucles anidados**. Para entenderlo, analicemos qué sucede en un arreglo de tamaño $n$:

### A. El Bucle Externo
El algoritmo recorre el arreglo buscando el elemento más pequeño para colocarlo en la primera posición, luego el segundo más pequeño para la segunda, y así sucesivamente. 
* Este bucle se ejecuta **$n - 1$ veces**.

### B. El Bucle Interno (La búsqueda del mínimo)
Dentro de cada iteración del bucle externo, el algoritmo debe encontrar el valor mínimo en la parte del arreglo que aún no ha sido ordenada.
* En la **1ª iteración**, busca entre $n$ elementos (compara $n-1$ veces).
* En la **2ª iteración**, busca entre $n-1$ elementos (compara $n-2$ veces).
* En la **última iteración**, solo compara los últimos 2 elementos.



### C. La Sumatoria Matemática
El número total de comparaciones es la suma de una progresión aritmética:
$$Total = (n-1) + (n-2) + (n-3) + \dots + 1$$

La fórmula para esta suma es:
$$\frac{(n-1) \times n}{2} = \frac{n^2 - n}{2}$$

En la notación **Big O**, eliminamos las constantes y los términos de menor orden (el $-n$ y el $/2$), lo que nos deja con una complejidad de:
**$O(n^2)$**

### Comparación de Casos:
A diferencia de otros algoritmos como el Bubble Sort (que puede terminar antes si el arreglo está ordenado) o el Insertion Sort:
* **Peor caso:** $O(n^2)$
* **Mejor caso:** $O(n^2)$
* **Caso promedio:** $O(n^2)$

**¿Por qué siempre es $O(n^2)$?** Porque el algoritmo no tiene forma de saber si el resto del arreglo ya está ordenado; siempre debe recorrer toda la parte no ordenada para confirmar cuál es el elemento mínimo.



---

## 2. Complejidad Espacial: $O(1)$

Selection Sort es un algoritmo **in-place** (en el sitio). 

* **Memoria adicional:** No requiere crear una copia del arreglo ni estructuras de datos auxiliares (como listas adicionales o árboles).
* **Variables auxiliares:** Solo utiliza una cantidad mínima de memoria extra para variables temporales:
    1. Una variable para almacenar el índice del valor mínimo actual.
    2. Una variable temporal para realizar el intercambio (*swap*).
    
Como el espacio requerido no depende del tamaño del arreglo de entrada ($n$), decimos que su complejidad de espacio es **constante**: **$O(1)$**.

---

## Resumen Técnico

| Atributo | Complejidad |
| :--- | :--- |
| **Peor tiempo de ejecución** | $O(n^2)$ |
| **Mejor tiempo de ejecución** | $O(n^2)$ |
| **Tiempo promedio** | $O(n^2)$ |
| **Espacio adicional (peor caso)** | $O(1)$ auxiliar |

### Conclusión
Selection Sort es eficiente para arreglos muy pequeños o en sistemas donde la memoria es extremadamente limitada (debido a su $O(1)$ espacial), pero es altamente ineficiente para grandes volúmenes de datos comparado con algoritmos como **Merge Sort** o **Quick Sort** ($O(n \log n)$).