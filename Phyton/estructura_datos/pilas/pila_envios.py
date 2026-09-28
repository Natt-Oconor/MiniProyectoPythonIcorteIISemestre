"""
ESTRUCTURA LINEAL 2 de 3 - PILA (LIFO).

Problema que resuelve: el caso inverso al de la cola. Cuando la peticion
mas reciente es la que tiene prioridad (por ejemplo, un reclamo o una
solicitud que el cliente marco como urgente al final del dia, o el
historial de asignaciones donde interesa el ultimo movimiento primero),
la estructura apropiada es la PILA: el ultimo en entrar es el primero en salir.

    cima  [ 1, 2, 3 ]  base
           ^ sale por aqui ^ entra por aqui
"""

from estructura_datos.base import EstructuraLineal
from modelos.solicitud import Solicitud


class PilaEnvios(EstructuraLineal):
    """Pila LIFO de solicitudes. La ultima registrada sale primero."""

    def __init__(self, elementos=None):
        self._almacen = list(elementos) if elementos else []

    # --- Operaciones principales de la PILA ---

    def apilar(self, solicitud):
        """Push: agrega una solicitud en la cima de la pila."""
        return self._agregar_en_cima(solicitud)

    def desapilar(self):
        """Pop: saca la solicitud de la cima (la mas reciente)."""
        self._exigir_datos()
        return self._quitar_de_la_cima()

    def cima(self):
        """Peek: consulta la solicitud mas reciente sin sacarla."""
        return self.siguiente()

    def agregar(self, solicitud):
        """Metodo de la clase base: en una pila, agregar = apilar."""
        return self.apilar(solicitud)

    def quitar(self):
        """Metodo de la clase base: en una pila, quitar = desapilar."""
        return self.desapilar()

    def siguiente(self):
        """Solicitud de la cima, sin removerla de la pila."""
        self._exigir_datos()
        return self._almacen[-1]

    def cancelar(self, id_envio):
        """Quita de la pila una solicitud cancelada por el cliente."""
        solicitud = self.buscar(id_envio)
        if solicitud is None:
            return False
        solicitud.marcar_cancelado()
        self._reconstruir_sin(id_envio)
        return True

    def cantidad_bajo_cima(self, id_envio):
        """Cuantas solicitudes tiene la pila POR DEBAJO de ese ID.

        Sirve para mostrar de forma didactica que la pila es LIFO y no FIFO.
        """
        for indice, solicitud in enumerate(self._almacen):
            if solicitud.id_envio == id_envio:
                return self.tamanio() - indice - 1
        return -1

    # --- Detalles internos ---

    def _agregar_en_cima(self, solicitud):
        if not isinstance(solicitud, Solicitud):
            raise TypeError("Solo se apilan objetos Solicitud")
        self._almacen.append(solicitud)
        return solicitud

    def _quitar_de_la_cima(self):
        return self._almacen.pop()

    def _reconstruir_sin(self, id_envio):
        self._almacen = [s for s in self._almacen if s.id_envio != id_envio]

    def orden_salida(self):
        """IDs en el orden exacto en que saldran de la pila."""
        return list(reversed(self.ids()))
