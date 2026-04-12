"""
pilas.py — Librería del curso Estructuras de Datos y Algoritmos
Unidad 2: Pilas (Stacks)

Cómo importar:
    from pilas import PilaTDA, PilaArreglo, PilaEnlazada

Ejemplo mínimo:
    p = PilaArreglo()
    p.push(10)
    p.push(20)
    print(p.pop())   # 20
    print(p.peek())  # 10
    print(p.size())  # 1
"""
from abc import ABC, abstractmethod
from typing import Any

class PilaTDA(ABC):
    """
    TDA Pila (Stack) — interfaz abstracta.

    Una Pila es una estructura LIFO (Last In, First Out): el último
    elemento en entrar es el primero en salir.

    Invariante: size() >= 0 en todo momento.
    """
    @abstractmethod
    def push(self, item: Any) -> None:
        """
        Inserta item en el tope de la pila.
        Parámetros: item — elemento a insertar (cualquier tipo)
        Retorno: None
        Complejidad: O(1) amortizado (arreglo) / O(1) estricto (lista enlazada)
        Ejemplo: p.push(42)
        """
        ...

    @abstractmethod
    def pop(self) -> Any:
        """
        Elimina y retorna el elemento del tope.
        Retorno: elemento del tope
        Lanza: IndexError si la pila está vacía
        Complejidad: O(1) amortizado (arreglo) / O(1) estricto (lista enlazada)
        """
        ...

    @abstractmethod
    def peek(self) -> Any:
        """
        Retorna el elemento del tope SIN eliminarlo.
        Retorno: elemento del tope
        Lanza: IndexError si la pila está vacía
        Complejidad: O(1) ambas implementaciones
        """
        ...

    @abstractmethod
    def is_empty(self) -> bool:
        """Retorna True si la pila no tiene elementos. O(1)."""
        ...

    @abstractmethod
    def size(self) -> int:
        """Retorna el número de elementos en la pila. O(1)."""
        ...

    def __len__(self) -> int:
        """Soporte para len(pila). Llama a size()."""
        return self.size()

    @abstractmethod
    def __repr__(self) -> str:
        """Representación textual para debugging."""
        ...


class PilaArreglo(PilaTDA):
    """
    Pila implementada con arreglo dinámico (lista Python).

    Estructura interna: lista Python donde el índice -1 (último) es el tope.
    El arreglo crece y se contrae automáticamente.

    Invariante: __datos[-1] es el tope cuando not is_empty()

    Complejidad:
        push  → O(1) amortizado
        pop   → O(1) amortizado
        peek  → O(1)
        size  → O(1)
    """
    def __init__(self) -> None:
        self.__datos: list = []

    def push(self, item: Any) -> None:
        self.__datos.append(item)

    def pop(self) -> Any:
        if self.is_empty():
            raise IndexError("pop de pila vacía")
        return self.__datos.pop()

    def peek(self) -> Any:
        if self.is_empty():
            raise IndexError("peek de pila vacía")
        return self.__datos[-1]

    def is_empty(self) -> bool:
        return len(self.__datos) == 0

    def size(self) -> int:
        return len(self.__datos)

    def __repr__(self) -> str:
        if self.is_empty():
            return "PilaArreglo(vacía)"
        items = list(reversed(self.__datos))
        return "PilaArreglo(tope → " + " → ".join(str(x) for x in items) + ")"


class _Nodo:
    """Nodo interno para PilaEnlazada. No usar directamente."""
    def __init__(self, dato: Any, siguiente: '_Nodo | None' = None) -> None:
        self.dato = dato
        self.siguiente = siguiente


class PilaEnlazada(PilaTDA):
    """
    Pila implementada con lista enlazada simple.

    Estructura interna: cadena de _Nodo donde __tope apunta al nodo superior.
    No requiere redimensionamiento; cada push/pop es O(1) estricto.

    Invariante: __tope es None sii is_empty()

    Complejidad:
        push  → O(1) estricto
        pop   → O(1) estricto
        peek  → O(1)
        size  → O(1) (contador mantenido)
    """
    def __init__(self) -> None:
        self.__tope: _Nodo | None = None
        self.__tam: int = 0

    def push(self, item: Any) -> None:
        self.__tope = _Nodo(item, self.__tope)
        self.__tam += 1

    def pop(self) -> Any:
        if self.is_empty():
            raise IndexError("pop de pila vacía")
        valor = self.__tope.dato
        self.__tope = self.__tope.siguiente
        self.__tam -= 1
        return valor

    def peek(self) -> Any:
        if self.is_empty():
            raise IndexError("peek de pila vacía")
        return self.__tope.dato

    def is_empty(self) -> bool:
        return self.__tope is None

    def size(self) -> int:
        return self.__tam

    def __repr__(self) -> str:
        if self.is_empty():
            return "PilaEnlazada(vacía)"
        items = []
        nodo = self.__tope
        while nodo is not None:
            items.append(str(nodo.dato))
            nodo = nodo.siguiente
        return "PilaEnlazada(tope → " + " → ".join(items) + ")"
