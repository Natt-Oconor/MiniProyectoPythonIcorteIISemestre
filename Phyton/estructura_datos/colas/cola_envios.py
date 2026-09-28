"""
ESTRUCTURA LINEAL 1 de 3 - COLA (FIFO).

Problema que resuelve: las solicitudes llegan por WhatsApp y deben atenderse
en el MISMO orden en que llegaron. La primera en entrar es la primera en
salir. Por eso la estructura apropiada es la COLA.

Se implementa con collections.deque, que ofrece insertar y quitar por el
extremo en tiempo constante (O(1)).

    frente  [ 1, 2, 3 ]  fondo
            ^ entra por aqui ^ sale por aqui
"""

from collections import deque

from estructura_datos.base import EstructuraLineal
from modelos.solicitud import Solicitud


class ColaEnvios(EstructuraLineal):
    """Cola FIFO de solicitudes de envío pendientes de asignacion."""

    def __init__(self, elementos=None):
        self._almacen = deque(elementos) if elementos else deque()

    # --- Operaciones principales de la COLA ---

    def encolar(self, solicitud):
        """Enqueue: agrega una solicitud al final (fondo) de la cola."""
        self._agregar_al_final(solicitud)
        return solicitud

    def desencolar(self):
        """Dequeue: saca la solicitud del frente (la mas antigua)."""
        self._exigir_datos()
        solicitud = self._quitar_del_frente()
        return solicitud

    def frente(self):
        """Peek: consulta la siguiente solicitud sin sacarla."""
        return self.siguiente()

    def agregar(self, solicitud):
        """Metodo de la clase base: en una cola, agregar = encolar."""
        return self.encolar(solicitud)

    def quitar(self):
        """Metodo de la clase base: en una cola, quitar = desencolar."""
        return self.desencolar()

    def siguiente(self):
        """Primera solicitud en salir, sin removerla de la cola."""
        self._exigir_datos()
        return self._almacen[0]

    def cancelar(self, id_envio):
        """Quita de la cola una solicitud cancelada por el cliente.

        Es la unica operacion O(n) de la cola, porque hay que buscar el ID
        en medio de los elementos y reconstruir la cola sin el.
        """
        solicitud = self.buscar(id_envio)
        if solicitud is None:
            return False
        solicitud.marcar_cancelado()
        self._reconstruir_sin(id_envio)
        return True

    # --- Detalles internos ---

    def _agregar_al_final(self, solicitud):
        if not isinstance(solicitud, Solicitud):
            raise TypeError("Solo se encolan objetos Solicitud")
        self._almacen.append(solicitud)

    def _quitar_del_frente(self):
        return self._almacen.popleft()

    def _reconstruir_sin(self, id_envio):
        restantes = deque(s for s in self._almacen if s.id_envio != id_envio)
        self._almacen = restantes

    def orden_atencion(self):
        """Lista de IDs en el orden exacto en que seran atendidos."""
        return self.ids()
