"""
ordenamiento.py — Módulo de Algoritmos de Ordenamiento Elemental
Curso: Algoritmos y Estructuras de Datos
Universidad de Talca | PhD. César Astudillo

Clases disponibles:
  - OrdenamientoTDA   : Tipo de Dato Abstracto (interfaz común)
  - SelectionSort     : Ordenamiento por selección O(n²)
  - KnuthShuffle      : Barajado uniforme de Knuth/Fisher-Yates O(n)

Funciones utilitarias:
  - is_sorted(a)      : Verifica si una lista está ordenada
  - contar_inversiones(a) : Cuenta pares (i,j) donde a[i] > a[j] con i < j
"""

from abc import ABC, abstractmethod
from typing import List, Any
import random


# ─────────────────────────────────────────────────────────────────────────────
# TIPO DE DATO ABSTRACTO
# ─────────────────────────────────────────────────────────────────────────────

class OrdenamientoTDA(ABC):
    """
    Interfaz abstracta para algoritmos de ordenamiento.

    Define el contrato que todo algoritmo de ordenamiento debe cumplir.
    Permite comparar y sustituir implementaciones sin cambiar el código cliente.
    """

    @abstractmethod
    def ordenar(self, lista: List[Any]) -> List[Any]:
        """
        Ordena la lista in-place y la retorna.

        Parámetros:
            lista (List[Any]): Lista de elementos comparables.

        Retorna:
            List[Any]: La misma lista ordenada de menor a mayor.

        Complejidad:
            Depende de la implementación concreta.
        """
        pass

    @abstractmethod
    def comparaciones(self) -> int:
        """
        Retorna el número de comparaciones realizadas en la última llamada a ordenar().

        Retorna:
            int: Total de comparaciones (modelo de costo estándar).
        """
        pass

    @abstractmethod
    def swaps(self) -> int:
        """
        Retorna el número de intercambios realizados en la última llamada a ordenar().

        Retorna:
            int: Total de swaps (intercambios de elementos).
        """
        pass

    def nombre(self) -> str:
        """Retorna el nombre del algoritmo."""
        return self.__class__.__name__


# ─────────────────────────────────────────────────────────────────────────────
# SELECTION SORT
# ─────────────────────────────────────────────────────────────────────────────

class SelectionSort(OrdenamientoTDA):
    """
    Ordenamiento por Selección (Selection Sort).

    Idea central: en cada pasada i, encuentra el mínimo de a[i..n-1]
    y lo intercambia con a[i]. Tras i pasadas, a[0..i-1] está ordenado.

    Invariante:
        - Antes de la pasada i: a[0..i-1] es el prefijo ordenado (definitivo).
        - a[i..n-1] son los elementos aún no ordenados.

    Complejidad:
        Temporal: O(n²) en TODOS los casos (mejor, peor y promedio).
                  Siempre hace exactamente n*(n-1)/2 comparaciones.
        Espacial: O(1) — ordenamiento in-place, sin memoria auxiliar.

    Característica notable:
        Hace el MÍNIMO número de swaps posible: a lo más n-1 intercambios.
        Útil cuando escribir a memoria es muy costoso (ej. memoria flash).
    """

    def __init__(self):
        self.__comparaciones = 0
        self.__swaps = 0

    def ordenar(self, lista: List[Any]) -> List[Any]:
        """
        Ordena lista in-place usando Selection Sort.

        Parámetros:
            lista (List[Any]): Lista mutable de elementos comparables.

        Retorna:
            List[Any]: La misma lista ordenada (modificada in-place).

        Complejidad:
            Temporal: O(n²) — siempre, independiente de la entrada.
            Espacial: O(1) — solo variables auxiliares de índice.

        Ejemplo:
            >>> s = SelectionSort()
            >>> s.ordenar([5, 3, 1, 4, 2])
            [1, 2, 3, 4, 5]
            >>> s.comparaciones()
            10
        """
        self.__comparaciones = 0
        self.__swaps = 0
        n = len(lista)

        for i in range(n - 1):
            # Paso 1: Encontrar el índice del mínimo en a[i..n-1]
            idx_min = i
            for j in range(i + 1, n):
                self.__comparaciones += 1          # ← contamos cada comparación
                if lista[j] < lista[idx_min]:
                    idx_min = j

            # Paso 2: Intercambiar el mínimo con la posición i
            if idx_min != i:
                lista[i], lista[idx_min] = lista[idx_min], lista[i]
                self.__swaps += 1                  # ← contamos el swap

        return lista

    def ordenar_verbose(self, lista: List[Any]) -> List[Any]:
        """
        Versión didáctica: imprime cada pasada del algoritmo.

        Útil para entender la invariante paso a paso en clases.

        Parámetros:
            lista (List[Any]): Lista a ordenar.

        Retorna:
            List[Any]: Lista ordenada.
        """
        self.__comparaciones = 0
        self.__swaps = 0
        n = len(lista)

        print(f"Selection Sort — inicio: {lista}")
        print(f"{'Pasada':>7} | {'Array':^40} | {'idx_min':>7} | {'swap'}")
        print("─" * 65)

        for i in range(n - 1):
            idx_min = i
            for j in range(i + 1, n):
                self.__comparaciones += 1
                if lista[j] < lista[idx_min]:
                    idx_min = j

            swap_str = f"{lista[i]} ↔ {lista[idx_min]}" if idx_min != i else "—"

            if idx_min != i:
                lista[i], lista[idx_min] = lista[idx_min], lista[i]
                self.__swaps += 1

            # Marcar el prefijo ordenado con corchetes
            prefijo = str(lista[:i+1])
            resto = str(lista[i+1:])
            estado = f"{prefijo} {resto}"
            print(f"{i:>7} | {estado:^40} | {idx_min:>7} | {swap_str}")

        print("─" * 65)
        print(f"Resultado: {lista}")
        print(f"Total comparaciones: {self.__comparaciones} | Total swaps: {self.__swaps}")
        return lista

    def comparaciones(self) -> int:
        """Retorna comparaciones de la última llamada a ordenar()."""
        return self.__comparaciones

    def swaps(self) -> int:
        """Retorna swaps de la última llamada a ordenar()."""
        return self.__swaps

    def comparaciones_teoricas(self, n: int) -> int:
        """
        Calcula el número exacto de comparaciones para n elementos.

        Fórmula: n*(n-1)/2  (siempre, independiente de la entrada)

        Parámetros:
            n (int): Tamaño de la lista.

        Retorna:
            int: Número exacto de comparaciones.
        """
        return n * (n - 1) // 2

    def __repr__(self) -> str:
        return (f"SelectionSort("
                f"comparaciones={self.__comparaciones}, "
                f"swaps={self.__swaps})")


# ─────────────────────────────────────────────────────────────────────────────
# KNUTH SHUFFLE (Fisher-Yates)
# ─────────────────────────────────────────────────────────────────────────────

class KnuthShuffle:
    """
    Algoritmo de Barajado de Knuth (variante de Fisher-Yates).

    Genera una permutación aleatoria UNIFORME de los elementos de una lista.
    Esto significa que cada una de las n! permutaciones tiene la misma
    probabilidad de ocurrir (1/n!).

    Idea central: para cada posición i (de 0 a n-1), elegir un índice
    aleatorio j en [i, n-1] y hacer swap(a[i], a[j]).

    Invariante:
        - Después de procesar posición i: a[0..i] es una permutación
          aleatoria uniforme de i+1 elementos seleccionados de la lista.

    Complejidad:
        Temporal: O(n) — exactamente n-1 swaps.
        Espacial: O(1) — in-place, sin arreglo auxiliar.

    ¿Por qué es correcto?
        En la pasada i, hay (n-i) posibles posiciones para el elemento.
        Cada una se elige con probabilidad 1/(n-i), lo que garantiza
        uniformidad por inducción.

    Error común (Naive Shuffle):
        for i in range(n):
            j = random.randint(0, n-1)  # ← j en [0, n-1] en lugar de [i, n-1]
        Esto genera n^n permutaciones, pero solo n! son distintas.
        Como n^n no es divisible por n!, la distribución NO es uniforme.
    """

    def __init__(self, semilla: int = None):
        """
        Constructor.

        Parámetros:
            semilla (int, opcional): Semilla para el generador de números
                aleatorios. Usar para reproducibilidad en pruebas.
        """
        self.__swaps = 0
        if semilla is not None:
            random.seed(semilla)

    def barajar(self, lista: List[Any]) -> List[Any]:
        """
        Baraja lista in-place usando el algoritmo de Knuth.

        Parámetros:
            lista (List[Any]): Lista mutable a barajar.

        Retorna:
            List[Any]: La misma lista barajada (modificada in-place).

        Complejidad:
            Temporal: O(n) — exactamente n-1 iteraciones con 1 swap c/u.
            Espacial: O(1) — in-place.

        Ejemplo:
            >>> k = KnuthShuffle(semilla=42)
            >>> k.barajar([1, 2, 3, 4, 5])
            [2, 5, 4, 1, 3]   # resultado varía con semilla
        """
        self.__swaps = 0
        n = len(lista)

        for i in range(n - 1):
            # Elegir j aleatorio en [i, n-1] — CRUCIAL: j >= i
            j = random.randint(i, n - 1)
            if j != i:
                lista[i], lista[j] = lista[j], lista[i]
                self.__swaps += 1

        return lista

    def barajar_verbose(self, lista: List[Any]) -> List[Any]:
        """
        Versión didáctica: imprime cada paso del barajado.

        Parámetros:
            lista (List[Any]): Lista a barajar.

        Retorna:
            List[Any]: Lista barajada.
        """
        self.__swaps = 0
        n = len(lista)

        print(f"Knuth Shuffle — inicio: {lista}")
        print(f"{'Paso':>5} | {'i':>3} | {'j (aleatorio)':>13} | {'swap':^15} | {'Array'}")
        print("─" * 65)

        for i in range(n - 1):
            j = random.randint(i, n - 1)
            swap_str = f"{lista[i]} ↔ {lista[j]}" if j != i else "— (mismo)"

            if j != i:
                lista[i], lista[j] = lista[j], lista[i]
                self.__swaps += 1

            print(f"{i:>5} | {i:>3} | {j:>13} | {swap_str:^15} | {lista}")

        print("─" * 65)
        print(f"Resultado: {lista}")
        print(f"Total swaps realizados: {self.__swaps}")
        return lista

    def swaps(self) -> int:
        """Retorna swaps de la última llamada a barajar()."""
        return self.__swaps

    def nombre(self) -> str:
        """Retorna el nombre del algoritmo."""
        return "KnuthShuffle"

    def __repr__(self) -> str:
        return f"KnuthShuffle(swaps={self.__swaps})"


# ─────────────────────────────────────────────────────────────────────────────
# FUNCIONES UTILITARIAS
# ─────────────────────────────────────────────────────────────────────────────

def is_sorted(lista: List[Any]) -> bool:
    """
    Verifica si una lista está ordenada de menor a mayor.

    Parámetros:
        lista (List[Any]): Lista de elementos comparables.

    Retorna:
        bool: True si está ordenada, False en otro caso.

    Complejidad:
        Temporal: O(n) — recorre la lista una vez.
        Espacial: O(1).

    Ejemplo:
        >>> is_sorted([1, 2, 3, 4, 5])
        True
        >>> is_sorted([3, 1, 2])
        False
    """
    return all(lista[i] <= lista[i + 1] for i in range(len(lista) - 1))


def contar_inversiones(lista: List[Any]) -> int:
    """
    Cuenta el número de inversiones en la lista.

    Una inversión es un par (i, j) donde i < j pero lista[i] > lista[j].
    El número de inversiones mide "cuán desordenada" está la lista:
    - 0 inversiones = ya ordenada
    - n*(n-1)/2 inversiones = orden inverso (máximo desorden)

    Parámetros:
        lista (List[Any]): Lista de elementos comparables.

    Retorna:
        int: Número de pares en inversión.

    Complejidad:
        Temporal: O(n²) — algoritmo ingenuo de doble for.
        Espacial: O(1).

    Ejemplo:
        >>> contar_inversiones([2, 1, 3])
        1  # solo (2, 1) está invertido
        >>> contar_inversiones([3, 2, 1])
        3  # (3,2), (3,1), (2,1)
    """
    n = len(lista)
    inversiones = 0
    for i in range(n):
        for j in range(i + 1, n):
            if lista[i] > lista[j]:
                inversiones += 1
    return inversiones


def generar_lista_aleatoria(n: int, rango: tuple = (1, 100)) -> List[int]:
    """
    Genera una lista de n enteros aleatorios en el rango [rango[0], rango[1]].

    Parámetros:
        n (int): Número de elementos.
        rango (tuple): Rango (min, max) de los valores.

    Retorna:
        List[int]: Lista de enteros aleatorios.
    """
    return [random.randint(rango[0], rango[1]) for _ in range(n)]


def generar_lista_casi_ordenada(n: int, intercambios: int = 3) -> List[int]:
    """
    Genera una lista casi ordenada haciendo k intercambios aleatorios.

    Útil para demostrar que Selection Sort NO se beneficia de datos
    casi ordenados (a diferencia de Insertion Sort).

    Parámetros:
        n (int): Número de elementos.
        intercambios (int): Número de intercambios aleatorios a aplicar.

    Retorna:
        List[int]: Lista [1..n] con algunos intercambios.
    """
    lista = list(range(1, n + 1))
    for _ in range(intercambios):
        i, j = random.sample(range(n), 2)
        lista[i], lista[j] = lista[j], lista[i]
    return lista
