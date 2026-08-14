"""
unionfind.py
============
Librería de estructuras Union-Find para el curso de Estructuras de Datos.
Unidad 2 — Tipos de Datos Abstractos.

Uso básico
----------
    from unionfind import WeightedQuickUnion

    uf = WeightedQuickUnion(10)   # 10 objetos: 0..9
    uf.union(3, 4)
    uf.union(4, 8)
    print(uf.connected(3, 8))     # True
    print(uf.count())             # número de componentes

Clases disponibles
------------------
    WeightedQuickUnion   — implementación de producción (recomendada)

Nota
----
Los detalles de implementación son internos a esta librería.
Como usuario, solo necesitas conocer la API documentada aquí.
"""

from abc import ABC, abstractmethod


# ══════════════════════════════════════════════════════════════════
#  Interfaz pública (TDA)
# ══════════════════════════════════════════════════════════════════

class UnionFind(ABC):
    """
    Tipo de Dato Abstracto: Union-Find (Conjuntos Disjuntos).

    Resuelve el problema de conectividad dinámica sobre N objetos
    identificados con enteros del 0 al N-1.

    Esta clase define el CONTRATO que toda implementación debe cumplir.
    No instancies esta clase directamente; usa WeightedQuickUnion.
    """

    @abstractmethod
    def union(self, p: int, q: int) -> None:
        """
        Conecta el objeto p con el objeto q.

        Si p y q ya están conectados, no hace nada.

        Parámetros
        ----------
        p : int   identificador del primer objeto  (0 <= p < N)
        q : int   identificador del segundo objeto (0 <= q < N)

        Complejidad
        -----------
        WeightedQuickUnion: O(log N) amortizado
        """

    @abstractmethod
    def find(self, p: int) -> int:
        """
        Retorna el identificador del componente al que pertenece p.

        Dos objetos pertenecen al mismo componente si y solo si
        sus identificadores de componente son iguales.

        Parámetros
        ----------
        p : int   identificador del objeto (0 <= p < N)

        Retorna
        -------
        int : identificador del componente de p

        Complejidad
        -----------
        WeightedQuickUnion: O(log N)
        """

    def connected(self, p: int, q: int) -> bool:
        """
        Retorna True si p y q pertenecen al mismo componente conectado.

        Equivalente a:  find(p) == find(q)

        Parámetros
        ----------
        p : int   identificador del primer objeto
        q : int   identificador del segundo objeto

        Retorna
        -------
        bool : True si están conectados, False si no

        Complejidad
        -----------
        Igual que find(): O(log N) en WeightedQuickUnion

        Ejemplo
        -------
        >>> uf = WeightedQuickUnion(5)
        >>> uf.union(0, 1)
        >>> uf.union(1, 2)
        >>> uf.connected(0, 2)
        True
        >>> uf.connected(0, 3)
        False
        """
        return self.find(p) == self.find(q)

    @abstractmethod
    def count(self) -> int:
        """
        Retorna el número actual de componentes conectados.

        Comienza en N (cada objeto es su propio componente).
        Disminuye en 1 con cada union() que conecta dos componentes distintos.

        Retorna
        -------
        int : número de componentes (1 <= count <= N)

        Ejemplo
        -------
        >>> uf = WeightedQuickUnion(5)
        >>> uf.count()
        5
        >>> uf.union(0, 1)
        >>> uf.count()
        4
        """

    @abstractmethod
    def component_size(self, p: int) -> int:
        """
        Retorna el número de objetos en el mismo componente que p.

        Parámetros
        ----------
        p : int   identificador del objeto

        Retorna
        -------
        int : tamaño del componente que contiene a p

        Ejemplo
        -------
        >>> uf = WeightedQuickUnion(5)
        >>> uf.union(0, 1)
        >>> uf.union(1, 2)
        >>> uf.component_size(0)
        3
        >>> uf.component_size(4)
        1
        """


# ══════════════════════════════════════════════════════════════════
#  Implementación (caja negra para el estudiante)
# ══════════════════════════════════════════════════════════════════

class WeightedQuickUnion(UnionFind):
    """
    Implementación de Union-Find con ponderación por tamaño.

    Garantiza que la profundidad máxima de los árboles internos
    sea O(log N), lo que hace que union() y find() sean O(log N).

    Parámetros
    ----------
    n : int   número de objetos (se identifican con 0, 1, ..., n-1)

    Ejemplo completo
    ----------------
    >>> uf = WeightedQuickUnion(10)
    >>> uf.count()
    10
    >>> uf.union(4, 3)
    >>> uf.union(3, 8)
    >>> uf.union(6, 5)
    >>> uf.connected(4, 8)
    True
    >>> uf.connected(4, 5)
    False
    >>> uf.component_size(4)
    3
    >>> uf.count()
    7
    """

    def __init__(self, n: int):
        if n <= 0:
            raise ValueError(f"n debe ser un entero positivo, se recibió {n}")
        self.__id    = list(range(n))
        self.__size  = [1] * n
        self.__count = n

    def find(self, p: int) -> int:
        self.__validar(p)
        return self.__root(p)

    def union(self, p: int, q: int) -> None:
        self.__validar(p)
        self.__validar(q)
        rp, rq = self.__root(p), self.__root(q)
        if rp == rq:
            return
        if self.__size[rp] < self.__size[rq]:
            self.__id[rp]    = rq
            self.__size[rq] += self.__size[rp]
        else:
            self.__id[rq]    = rp
            self.__size[rp] += self.__size[rq]
        self.__count -= 1

    def count(self) -> int:
        return self.__count

    def component_size(self, p: int) -> int:
        self.__validar(p)
        return self.__size[self.__root(p)]

    # ── Métodos privados (no forman parte de la API) ──────────
    def __root(self, p: int) -> int:
        while self.__id[p] != p:
            p = self.__id[p]
        return p

    def __validar(self, p: int) -> None:
        n = len(self.__id)
        if not (0 <= p < n):
            raise IndexError(
                f"Índice {p} fuera de rango para N={n}. "
                f"Los índices válidos son 0 a {n-1}."
            )

    def __repr__(self) -> str:
        return (f"WeightedQuickUnion(N={len(self.__id)}, "
                f"componentes={self.__count})")
