# Fusión de dos arreglos ordenados

> Nota construida en clase. Es el problema que motiva Merge Sort: antes de dividir hay que
> saber **fusionar**, y esta es la pieza sobre la que se apoya todo el algoritmo.

## El problema

Dados **2 arreglos ORDENADOS**, producir un único arreglo ordenado con todos sus elementos.

Por ejemplo:

```text
1 3 4 8 9
2 5 6 7 10

Resultado:
1 2 3 4 5 6 7 8 9 10
```

**¿Cómo defino un algoritmo para esto?**

## La idea

Comenzamos con los dos subarreglos en el índice 0. Dependiendo de cuál es menor, copiamos ese
elemento y luego avanzamos el índice para ese subarreglo. Repetimos el proceso hasta recorrer
ambos subarreglos completamente.

```text
 i                          j
[1 3 4 8 9]                [2 5 6 7 10]        salida: []

 1 < 2  ->  copio 1, avanzo i
   i                        j
[1 3 4 8 9]                [2 5 6 7 10]        salida: [1]

 3 > 2  ->  copio 2, avanzo j
   i                          j
[1 3 4 8 9]                [2 5 6 7 10]        salida: [1 2]

 ... y así hasta agotar ambos
```

## ¿Qué complejidad tiene?

**Complejidad lineal, $O(n)$**, donde $n$ es la cantidad total de elementos en ambos
subarreglos.

La razón es que cada iteración copia exactamente un elemento a la salida y avanza uno de los
dos índices. Como ningún índice retrocede, en total se hacen $n$ iteraciones.

## Por qué esto importa

Merge Sort es exactamente esta operación aplicada recursivamente:

1. Dividir el arreglo por la mitad.
2. Ordenar cada mitad (recursivamente).
3. **Fusionar** las dos mitades ya ordenadas — este algoritmo.

El costo total sale de combinar el $O(n)$ de cada fusión con los $\log n$ niveles de división:

$$T(n) = 2\,T(n/2) + \Theta(n) = \Theta(n \log n)$$

> 💡 Nota que la fusión necesita un arreglo auxiliar: no se puede hacer in-place en tiempo
> lineal. Ese es el costo espacial $\Theta(n)$ de Merge Sort, y la razón por la que Quicksort
> lo supera en uso de memoria.
