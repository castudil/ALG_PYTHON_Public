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
    Pila implementada con un arreglo que se redimensiona.

    El arreglo es una lista de Python de largo fijo, creada con [None] * capacidad,
    que se usa SOLO por índice (a[i] = x, x = a[i]): nunca append, pop ni insert.
    Así cada costo queda a la vista, igual que con un arreglo en C o Java.

    Estado interno:
        __arreglo — las casillas; las libres valen None
        __n       — cantidad de elementos; el tope está en __arreglo[__n - 1]
                    y el próximo push escribe en __arreglo[__n]

        capacidad 4, __n = 3 → push(10), push(20), push(30)
        índice:   0     1     2     3
                [ 10 ][ 20 ][ 30 ][ ·  ]
                             ▲ tope

    Redimensionamiento:
        arreglo lleno       (n == capacidad)      → duplicar la capacidad
        arreglo a un cuarto (n == capacidad // 4) → reducir a la mitad

    Invariante: __arreglo[__n - 1] es el tope cuando not is_empty()

    Complejidad:
        push  → O(1) amortizado (O(n) solo en la operación que duplica)
        pop   → O(1) amortizado (O(n) solo en la operación que reduce)
        peek  → O(1)
        size  → O(1)
    """
    def __init__(self) -> None: ## El constructor crea un arreglo de 2 casillas vacías. Este arreglo es la estructura subyacente: crece y se contrae copiando a un arreglo nuevo.
        self.__arreglo: list = [None] * 2 ## __arreglo es una lista privada de largo fijo que almacena los elementos de la pila. El tope de la pila siempre estará en la casilla __arreglo[__n - 1]. la variable __arreglo tiene dos guiones bajos al inicio para indicar que es un atributo **privado de la clase**, lo que significa que no debe ser accedido directamente desde fuera de la clase. en su lugar, se deben usar los métodos push, pop, peek, etc. para interactuar con la pila. se usa un unico guion bajo para indicar que un atributo es "protegido" (convención para uso interno o en subclases), pero aquí se usan dos guiones bajos para enfatizar que es completamente privado y no debe ser accedido desde fuera de la clase.
        self.__n: int = 0 ## __n cuenta los elementos: es a la vez size() y el índice de la próxima casilla libre.

    def __redimensionar(self, capacidad: int) -> None:
        # Copia los n elementos a un arreglo nuevo de la capacidad pedida — O(n)
        nuevo = [None] * capacidad
        for i in range(self.__n):
            nuevo[i] = self.__arreglo[i]
        self.__arreglo = nuevo

    def push(self, item: Any) -> None:
        if self.__n == len(self.__arreglo):
            self.__redimensionar(2 * len(self.__arreglo))
        self.__arreglo[self.__n] = item
        self.__n += 1

    def pop(self) -> Any:
        if self.is_empty():
            raise IndexError("pop de pila vacía") ## Si la pila está vacía, se lanza una excepción IndexError para indicar que no se puede hacer pop. el comando raise se usa para lanzar excepciones en Python.
        self.__n -= 1
        item = self.__arreglo[self.__n]
        # Soltar la referencia: el arreglo no debe retener un item que ya salió
        self.__arreglo[self.__n] = None
        if 0 < self.__n == len(self.__arreglo) // 4:
            self.__redimensionar(len(self.__arreglo) // 2)
        return item

    def peek(self) -> Any:
        if self.is_empty():
            raise IndexError("peek de pila vacía")
        return self.__arreglo[self.__n - 1]

    def is_empty(self) -> bool:
        return self.__n == 0

    def size(self) -> int:
        return self.__n

    def _casillas(self) -> list:
        """Copia del arreglo interno, casilla por casilla. Solo para visualizar en clase."""
        return [x for x in self.__arreglo]

    def __repr__(self) -> str:
        if self.is_empty():
            return "PilaArreglo(vacía)"
        items = [self.__arreglo[i] for i in range(self.__n - 1, -1, -1)]
        return "PilaArreglo(tope → " + " → ".join(str(x) for x in items) + ")" ## Para representar la pila, se recorre el arreglo desde el tope (__n - 1) hacia la base (0). se convierte cada elemento a string y se unen con " → " para mostrar la secuencia de elementos desde el tope hacia abajo.


class _Nodo:
    """Nodo interno para PilaEnlazada: guarda un item y la referencia al siguiente nodo."""
    def __init__(self, item: Any, siguiente: '_Nodo | None' = None) -> None:
        self.item = item
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
        self.__tope = _Nodo(item, self.__tope) ## Se crea un nuevo nodo con el item y el siguiente apuntando al nodo que actualmente es el tope. luego se actualiza __tope para que apunte a este nuevo nodo, convirtiéndolo en el nuevo tope de la pila.
        self.__tam += 1 # Se incrementa el contador de tamaño cada vez que se hace push para mantener el invariante de que size() es O(1). esto asegura que el método size() pueda retornar el número de elementos en la pila sin necesidad de recorrer la lista enlazada para contar los nodos, lo que sería O(n). con este contador, size() simplemente retorna el valor de __tam, garantizando una complejidad constante.

    def pop(self) -> Any:
        if self.is_empty(): ## underflow: intentar hacer pop en una pila vacía. se lanza una excepción IndexError para indicar que no se puede hacer pop porque no hay elementos en la pila.
            raise IndexError("pop de pila vacía")
        valor = self.__tope.item ## valor es una variable temporal que almacena el item del nodo que actualmente es el tope de la pila. esto es necesario porque después de actualizar __tope para apuntar al siguiente nodo, perderíamos la referencia al item del nodo que estamos eliminando. al guardar el item en valor antes de actualizar __tope, podemos retornar este valor después de hacer pop sin perder la información.
        self.__tope = self.__tope.siguiente
        self.__tam -= 1
        return valor

    def peek(self) -> Any:
        if self.is_empty():
            raise IndexError("peek de pila vacía")
        return self.__tope.item

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
            items.append(str(nodo.item))
            nodo = nodo.siguiente
        return "PilaEnlazada(tope → " + " → ".join(items) + ")"
