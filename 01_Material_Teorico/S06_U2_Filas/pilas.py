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
from abc import ABC, abstractmethod # ABC para definir clases abstractas e interfaces
from typing import Any # Any para indicar que un parámetro o retorno puede ser de cualquier tipo

class PilaTDA(ABC): # TDA: Tipo Abstracto de Datos, define la interfaz sin implementación concreta
    """
    TDA Pila (Stack) — interfaz abstracta.

    Una Pila es una estructura LIFO (Last In, First Out): el último
    elemento en entrar es el primero en salir.

    Invariante: size() >= 0 en todo momento.
    """
    @abstractmethod
    def push(self, item: Any) -> None: # Any indica que el item puede ser de cualquier tipo
        """
        Inserta item en el tope de la pila.
        Parámetros: item — elemento a insertar (cualquier tipo)
        Retorno: None
        Complejidad: O(1) amortizado (arreglo) / O(1) estricto (lista enlazada)
        Ejemplo: p.push(42)
        """
        ...

    @abstractmethod
    def pop(self) -> Any: # Retorna el tipo Any porque el elemento del tope puede ser de cualquier tipo
        """
        Elimina y retorna el elemento del tope.
        Retorno: elemento del tope
        Lanza: IndexError si la pila está vacía
        Complejidad: O(1) amortizado (arreglo) / O(1) estricto (lista enlazada)
        """
        ...

    @abstractmethod
    def peek(self) -> Any: # Retorna el tipo Any porque el elemento del tope puede ser de cualquier tipo
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
    def __init__(self) -> None: ## El constructor inicializa una lista vacía para almacenar los elementos de la pila. Esta lista se usará como el arreglo dinámico subyacente.
        self.__datos: list = [] ## __datos es una lista privada que almacena los elementos de la pila. El tope de la pila siempre estará en el último índice de esta lista (__datos[-1]). la variable __datos tiene dos guiones bajos al inicio para indicar que es un atributo **privado de la clase**, lo que significa que no debe ser accedido directamente desde fuera de la clase. en su lugar, se deben usar los métodos push, pop, peek, etc. para interactuar con la pila. se usa un unico guion bajo para indicar que un atributo es "protegido" (convención para uso interno o en subclases), pero aquí se usan dos guiones bajos para enfatizar que es completamente privado y no debe ser accedido desde fuera de la clase.

    def push(self, item: Any) -> None: 
        self.__datos.append(item)

    def pop(self) -> Any:
        if self.is_empty():
            raise IndexError("pop de pila vacía") ## Si la pila está vacía, se lanza una excepción IndexError para indicar que no se puede hacer pop. el comando raise se usa para lanzar excepciones en Python.
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
        return "PilaArreglo(tope → " + " → ".join(str(x) for x in items) + ")" ## Para representar la pila, se invierte la lista __datos para mostrar el tope primero. se convierte cada elemento a string y se unen con " → " para mostrar la secuencia de elementos desde el tope hacia abajo.


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
        self.__tope: _Nodo | None = None ## __tope es un puntero al nodo que está en el tope de la pila. inicialmente es None porque la pila está vacía. cada vez que se hace push, se crea un nuevo nodo que apunta al nodo anterior (el nuevo nodo se convierte en el nuevo tope). cada vez que se hace pop, se actualiza __tope para apuntar al siguiente nodo (el nuevo tope después de eliminar el actual). esto permite que las operaciones push y pop sean O(1) sin necesidad de recorrer la lista enlazada.
        self.__tam: int = 0 ## __tam es un contador que mantiene el número de elementos en la pila. se inicializa en 0 y se incrementa cada vez que se hace push y se decrementa cada vez que se hace pop. esto permite que el método size() retorne el tamaño de la pila en O(1) sin tener que recorrer la lista enlazada para contar los nodos.

    def push(self, item: Any) -> None:
        self.__tope = _Nodo(item, self.__tope) ## Se crea un nuevo nodo con el dato item y el siguiente apuntando al nodo que actualmente es el tope. luego se actualiza __tope para que apunte a este nuevo nodo, convirtiéndolo en el nuevo tope de la pila.
        self.__tam += 1 # Se incrementa el contador de tamaño cada vez que se hace push para mantener el invariante de que size() es O(1). esto asegura que el método size() pueda retornar el número de elementos en la pila sin necesidad de recorrer la lista enlazada para contar los nodos, lo que sería O(n). con este contador, size() simplemente retorna el valor de __tam, garantizando una complejidad constante.

    def pop(self) -> Any:
        if self.is_empty(): ## underflow: intentar hacer pop en una pila vacía. se lanza una excepción IndexError para indicar que no se puede hacer pop porque no hay elementos en la pila.
            raise IndexError("pop de pila vacía")
        valor = self.__tope.dato ## valor es una variable temporal que almacena el dato del nodo que actualmente es el tope de la pila. esto es necesario porque después de actualizar __tope para apuntar al siguiente nodo, perderíamos la referencia al dato del nodo que estamos eliminando. al guardar el dato en valor antes de actualizar __tope, podemos retornar este valor después de hacer pop sin perder la información.
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
