"""
filas.py — Librería del curso Estructuras de Datos y Algoritmos
Unidad 2: Filas (Queues)

Cómo importar:
    from filas import FilaTDA, FilaDeque, FilaEnlazada

Ejemplo mínimo:
    f = FilaDeque()
    f.enqueue(10)
    f.enqueue(20)
    print(f.dequeue())   # 10  ← FIFO: primero en entrar, primero en salir
    print(f.front())     # 20
    print(f.size())      # 1
"""
from abc import ABC, abstractmethod  # ABC para definir clases abstractas e interfaces
from collections import deque        # deque: doble cola eficiente de la librería estándar
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
        Complejidad: O(1) amortizado (deque) / O(1) estricto (lista enlazada)
        Ejemplo: f.enqueue("tarea_1")
        """
        ...

    @abstractmethod
    def dequeue(self) -> Any:
        """
        Elimina y retorna el elemento del frente de la fila.

        Retorno: elemento del frente
        Lanza: IndexError si la fila está vacía
        Complejidad: O(1) amortizado (deque) / O(1) estricto (lista enlazada)
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


class FilaDeque(FilaTDA):
    """
    Fila implementada con collections.deque.

    collections.deque es un arreglo de doble extremo (Doubly-Ended Queue)
    optimizado para inserciones y eliminaciones en O(1) amortizado en
    ambos extremos — ideal para implementar filas eficientemente.

    Convención interna:
        - El FRENTE de la fila está en el índice [0] (izquierda) del deque.
        - El FINAL  de la fila está en el índice [-1] (derecha) del deque.
        - enqueue → appendright (insertar a la derecha)
        - dequeue → popleft   (extraer de la izquierda)

    Complejidad:
        enqueue → O(1) amortizado
        dequeue → O(1) amortizado
        front   → O(1) estricto
        size    → O(1) estricto

    ¿Por qué NO usar list.pop(0)?
        list.pop(0) es O(n) porque desplaza todos los elementos.
        deque.popleft() es O(1) porque usa un puntero al nodo de cabeza.
    """

    def __init__(self) -> None:
        # __datos es un deque privado. El frente está a la izquierda (índice 0)
        # y el final está a la derecha (índice -1).
        self.__datos: deque = deque()

    def enqueue(self, item: Any) -> None:
        # Insertar al final (derecha del deque) — O(1) amortizado
        self.__datos.append(item)

    def dequeue(self) -> Any:
        if self.is_empty():
            raise IndexError("dequeue de fila vacía")
        # Extraer del frente (izquierda del deque) — O(1) amortizado
        return self.__datos.popleft()

    def front(self) -> Any:
        if self.is_empty():
            raise IndexError("front de fila vacía")
        # Ver el frente sin eliminarlo — O(1)
        return self.__datos[0]

    def is_empty(self) -> bool:
        return len(self.__datos) == 0

    def size(self) -> int:
        return len(self.__datos)

    def __repr__(self) -> str:
        if self.is_empty():
            return "FilaDeque(vacía)"
        items = list(self.__datos)
        return "FilaDeque(frente → " + " → ".join(str(x) for x in items) + " ← final)"


class _Nodo:
    """Nodo interno para FilaEnlazada. No usar directamente."""

    def __init__(self, dato: Any, siguiente: '_Nodo | None' = None) -> None:
        self.dato = dato
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
        valor = self.__frente.dato  # type: ignore[union-attr]
        self.__frente = self.__frente.siguiente  # type: ignore[union-attr]
        if self.__frente is None:
            # La fila quedó vacía: limpiar también __final
            self.__final = None
        self.__tam -= 1
        return valor

    def front(self) -> Any:
        if self.is_empty():
            raise IndexError("front de fila vacía")
        return self.__frente.dato  # type: ignore[union-attr]

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
            items.append(str(nodo.dato))
            nodo = nodo.siguiente
        return "FilaEnlazada(frente → " + " → ".join(items) + " ← final)"


# Alias: FilaArreglo → FilaDeque (para consistencia con la nomenclatura del curso)
FilaArreglo = FilaDeque
