"""
filas.py — Librería del curso Estructuras de Datos y Algoritmos
Unidad 2: Filas (Queues)

Cómo importar:
    from filas import FilaTDA, FilaArreglo, FilaEnlazada

Ejemplo mínimo:
    f = FilaArreglo()
    f.enqueue(10)
    f.enqueue(20)
    print(f.dequeue())   # 10  ← FIFO: primero en entrar, primero en salir
    print(f.front())     # 20
    print(f.size())      # 1

Las dos implementaciones se construyen desde cero, al estilo de Sedgewick & Wayne
(Algorithms, 4ª ed., §1.3):
    FilaArreglo  → arreglo circular que se redimensiona (ResizingArrayQueue)
    FilaEnlazada → lista enlazada con dos punteros (Queue)
Ninguna usa collections.deque ni los métodos append/pop/insert de list.
"""
from abc import ABC, abstractmethod  # ABC para definir clases abstractas e interfaces
from typing import Any               # Any para indicar tipo genérico


class FilaTDA(ABC):
    """
    TDA Fila (Queue) — interfaz abstracta.

    Una Fila es una estructura FIFO (First In, First Out): el primer
    elemento en entrar es el primero en salir. A diferencia de la Pila,
    los elementos se insertan por un extremo (final) y se extraen por
    el otro (frente).

    Analogía: una cola del banco, de la impresora, de un proceso del SO.

    Invariante: size() >= 0 en todo momento.
    """

    @abstractmethod
    def enqueue(self, item: Any) -> None:
        """
        Inserta item al final de la fila.

        Parámetros:
            item — elemento a insertar (cualquier tipo)
        Retorno: None
        Complejidad: O(1) amortizado (arreglo) / O(1) estricto (lista enlazada)
        Ejemplo: f.enqueue("tarea_1")
        """
        ...

    @abstractmethod
    def dequeue(self) -> Any:
        """
        Elimina y retorna el elemento del frente de la fila.

        Retorno: elemento del frente
        Lanza: IndexError si la fila está vacía
        Complejidad: O(1) amortizado (arreglo) / O(1) estricto (lista enlazada)
        """
        ...

    @abstractmethod
    def front(self) -> Any:
        """
        Retorna el elemento del frente SIN eliminarlo.

        Retorno: elemento del frente
        Lanza: IndexError si la fila está vacía
        Complejidad: O(1) ambas implementaciones
        """
        ...

    @abstractmethod
    def is_empty(self) -> bool:
        """Retorna True si la fila no tiene elementos. O(1)."""
        ...

    @abstractmethod
    def size(self) -> int:
        """Retorna el número de elementos en la fila. O(1)."""
        ...

    def __len__(self) -> int:
        """Soporte para len(fila). Llama a size()."""
        return self.size()

    @abstractmethod
    def __repr__(self) -> str:
        """Representación textual para debugging."""
        ...


class FilaArreglo(FilaTDA):
    """
    Fila implementada con un arreglo circular que se redimensiona.

    El arreglo es una lista de Python de largo fijo, creada con [None] * capacidad,
    que se usa SOLO por índice (a[i] = x, x = a[i]): nunca append, pop ni insert.
    Así cada costo queda a la vista, igual que con un arreglo en C o Java.

    Estado interno:
        __arreglo — las casillas; las libres valen None
        __frente  — índice del elemento que sale en el próximo dequeue
        __n       — cantidad de elementos
    La próxima casilla libre (donde entra el próximo enqueue) se calcula:
        (__frente + __n) % capacidad

    ¿Por qué circular?
        list.pop(0) es O(n) porque corre todos los elementos una casilla.
        Aquí dequeue no corre nada: solo avanza __frente. Cuando un índice
        llega al final del arreglo, vuelve a 0 gracias al módulo (%).

        capacidad 8, __frente = 6, __n = 4
        índice:   0    1    2    3    4    5    6    7
                [ C ][ D ][ ·  ][ ·  ][ ·  ][ ·  ][ A ][ B ]
                            ▲ libre                 ▲ frente
        Orden FIFO: A, B, C, D.

    Redimensionamiento:
        arreglo lleno       (n == capacidad)      → duplicar la capacidad
        arreglo a un cuarto (n == capacidad // 4) → reducir a la mitad
        Al copiar, el frente vuelve al índice 0.

    Complejidad:
        enqueue → O(1) amortizado (O(n) solo en la operación que duplica)
        dequeue → O(1) amortizado (O(n) solo en la operación que reduce)
        front   → O(1) estricto
        size    → O(1) estricto
    """

    def __init__(self) -> None:
        self.__arreglo: list = [None] * 2
        self.__frente: int = 0
        self.__n: int = 0

    def __redimensionar(self, capacidad: int) -> None:
        # Copia los n elementos en orden FIFO a un arreglo nuevo, desde el índice 0 — O(n)
        nuevo = [None] * capacidad
        for i in range(self.__n):
            nuevo[i] = self.__arreglo[(self.__frente + i) % len(self.__arreglo)]
        self.__arreglo = nuevo
        self.__frente = 0

    def enqueue(self, item: Any) -> None:
        if self.__n == len(self.__arreglo):
            self.__redimensionar(2 * len(self.__arreglo))
        libre = (self.__frente + self.__n) % len(self.__arreglo)
        self.__arreglo[libre] = item
        self.__n += 1

    def dequeue(self) -> Any:
        if self.is_empty():
            raise IndexError("dequeue de fila vacía")
        item = self.__arreglo[self.__frente]
        # Soltar la referencia: el arreglo no debe retener un item que ya salió
        self.__arreglo[self.__frente] = None
        self.__frente = (self.__frente + 1) % len(self.__arreglo)
        self.__n -= 1
        if 0 < self.__n == len(self.__arreglo) // 4:
            self.__redimensionar(len(self.__arreglo) // 2)
        return item

    def front(self) -> Any:
        if self.is_empty():
            raise IndexError("front de fila vacía")
        return self.__arreglo[self.__frente]

    def is_empty(self) -> bool:
        return self.__n == 0

    def size(self) -> int:
        return self.__n

    def _casillas(self) -> tuple[list, int]:
        """Copia del arreglo interno y el índice del frente. Solo para visualizar en clase."""
        return [x for x in self.__arreglo], self.__frente

    def __repr__(self) -> str:
        if self.is_empty():
            return "FilaArreglo(vacía)"
        items = [self.__arreglo[(self.__frente + i) % len(self.__arreglo)] for i in range(self.__n)]
        return "FilaArreglo(frente → " + " → ".join(str(x) for x in items) + " ← final)"


class _Nodo:
    """Nodo interno para FilaEnlazada: guarda un item y la referencia al siguiente nodo."""

    def __init__(self, item: Any, siguiente: '_Nodo | None' = None) -> None:
        self.item = item
        self.siguiente = siguiente


class FilaEnlazada(FilaTDA):
    """
    Fila implementada con lista enlazada simple con dos punteros.

    Diferencia clave respecto a PilaEnlazada:
        La pila solo necesita un puntero (__tope).
        La fila necesita DOS punteros:
            __frente → nodo desde donde se extrae (dequeue)
            __final  → nodo desde donde se inserta (enqueue)
        Sin __final, enqueue sería O(n) (habría que recorrer toda la lista).

    Diagrama:
        __frente                     __final
           |                            |
           v                            v
        [A|→] → [B|→] → [C|→] → [D|None]

        dequeue() retorna A, __frente avanza a B.
        enqueue(E) crea nodo E y __final.siguiente = E, __final = E.

    Complejidad:
        enqueue → O(1) estricto
        dequeue → O(1) estricto
        front   → O(1) estricto
        size    → O(1) estricto (contador mantenido)
    """

    def __init__(self) -> None:
        # __frente: puntero al nodo que se extrae (dequeue) — izquierda lógica
        self.__frente: _Nodo | None = None
        # __final: puntero al nodo donde se inserta (enqueue) — derecha lógica
        self.__final: _Nodo | None = None
        # __tam: contador de elementos para size() en O(1)
        self.__tam: int = 0

    def enqueue(self, item: Any) -> None:
        nuevo = _Nodo(item)
        if self.is_empty():
            # Primer elemento: __frente y __final apuntan al mismo nodo
            self.__frente = nuevo
            self.__final = nuevo
        else:
            # Caso general: añadir al final y avanzar __final
            self.__final.siguiente = nuevo  # type: ignore[union-attr]
            self.__final = nuevo
        self.__tam += 1

    def dequeue(self) -> Any:
        if self.is_empty():
            raise IndexError("dequeue de fila vacía")
        item = self.__frente.item  # type: ignore[union-attr]
        self.__frente = self.__frente.siguiente  # type: ignore[union-attr]
        if self.__frente is None:
            # La fila quedó vacía: limpiar también __final
            self.__final = None
        self.__tam -= 1
        return item

    def front(self) -> Any:
        if self.is_empty():
            raise IndexError("front de fila vacía")
        return self.__frente.item  # type: ignore[union-attr]

    def is_empty(self) -> bool:
        return self.__frente is None

    def size(self) -> int:
        return self.__tam

    def __repr__(self) -> str:
        if self.is_empty():
            return "FilaEnlazada(vacía)"
        items = []
        nodo = self.__frente
        while nodo is not None:
            items.append(str(nodo.item))
            nodo = nodo.siguiente
        return "FilaEnlazada(frente → " + " → ".join(items) + " ← final)"
