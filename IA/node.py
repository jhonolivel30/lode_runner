"""
    Jhon Oliver Castillo Caraballo
    22-SISN-2-063
"""

class Nodo:
    """
    Clase base para los nodos del árbol de comportamiento.
    """

    def __init__(self):
        """
        Inicializa el nodo con una lista vacía de hijos.
        """
        self.hijos = []

    def agregar_hijo(self, hijo):
        """
        Agrega un hijo al nodo.
        """
        self.hijos.append(hijo)

    def ejecutar(self):
        """
        Ejecuta el nodo y retorna el resultado.
        """
        pass


class Selector(Nodo):
    """
    Clase que implementa un nodo selector en el árbol de comportamiento.
    Ejecuta sus hijos en orden hasta que uno retorne True.

    Returns:
        bool: True si algún hijo retorna True, False si todos retornan False
    """

    def ejecutar(self):
        """
        Ejecuta los hijos en secuencia hasta encontrar uno exitoso.

        Returns:
            bool: True si algún hijo tuvo éxito, False en caso contrario
        """
        for hijo in self.hijos:
            if hijo.ejecutar():
                return True
        return False


class Secuencia(Nodo):
    """
    Clase que implementa un nodo de secuencia en el árbol de comportamiento.
    Ejecuta todos sus hijos en orden hasta que uno falle.

    Returns:
        bool: True si todos los hijos retornan True, False si alguno falla
    """

    def ejecutar(self):
        """
        Ejecuta los hijos en secuencia hasta que uno falle.

        Returns:
            bool: True si todos los hijos tuvieron éxito, False si alguno falló
        """
        for hijo in self.hijos:
            if not hijo.ejecutar():
                return False
        return True


class Accion(Nodo):
    """
    Clase que implementa un nodo de acción en el árbol de comportamiento.
    Ejecuta una acción específica pasada como parámetro.

    Args:
        accion (callable): Función a ejecutar cuando se active este nodo
    """

    def __init__(self, accion):
        """
        Inicializa el nodo de acción.

        Args:
            accion (callable): Función que se ejecutará
        """
        super().__init__()
        self.accion = accion

    def ejecutar(self):
        """
        Ejecuta la acción asociada a este nodo.

        Returns:
            bool: Resultado de la ejecución de la acción
        """
        return self.accion()


class Invertir(Nodo):
    """
    Clase que implementa un nodo inversor en el árbol de comportamiento.
    Invierte el resultado de la ejecución de su hijo.

    Args:
        accion (Nodo): Nodo hijo cuyo resultado será invertido
    """

    def __init__(self, accion):
        """
        Inicializa el nodo inversor.

        Args:
            accion (Nodo): Nodo hijo a invertir
        """
        super().__init__()
        self.agregar_hijo(accion)

    def ejecutar(self):
        """
        Ejecuta el hijo e invierte su resultado.

        Returns:
            bool: Negación del resultado de la ejecución del hijo
        """
        return not self.hijos[0].ejecutar()
