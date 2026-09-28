"""
ESTRUCTURA LINEAL 3 de 3 - LISTA.

Problema que resuelve: cuando el orden de llegada NO es el criterio, sino
que hay que poder buscar, reordenar y dar prioridad (por ejemplo, mover un
envio urgente al principio sin sacar el resto de la cola), la estructura
apropiada es la LISTA: acceso por posicion, insercion en cualquier punto y
busqueda lineal.

La lista es la estructura base de la que salen la pila y la cola.
"""

from estructura_datos.base import EstructuraLineal
from modelos.solicitud import Solicitud


class ListaSolicitudes(EstructuraLineal):
    """Lista de solicitudes con acceso por posicion y reordenamiento."""

    def __init__(self, elementos=None):
        self._almacen = list(elementos) if elementos else []

    # --- Insercion ---

    def agregar(self, solicitud):
        """Inserta al final de la lista."""
        return self.agregar_al_final(solicitud)

    def agregar_al_inicio(self, solicitud):
        """Inserta al principio de la lista (sirve para lo urgente)."""
        self._validar(solicitud)
        self._almacen.insert(0, solicitud)
        return solicitud

    def agregar_en_posicion(self, solicitud, posicion):
        """Inserta en una posicion concreta (0 = inicio)."""
        self._validar(solicitud)
        if posicion < 0 or posicion > self.tamanio():
            raise IndexError("Posicion fuera de rango")
        self._almacen.insert(posicion, solicitud)
        return solicitud

    def agregar_al_final(self, solicitud):
        self._validar(solicitud)
        self._almacen.append(solicitud)
        return solicitud

    # --- Acceso ---

    def siguiente(self):
        """La primera de la lista (posicion 0)."""
        self._exigir_datos()
        return self._almacen[0]

    def quitar(self):
        """Saca el primer elemento de la lista (posicion 0)."""
        self._exigir_datos()
        return self._quitar_de_posicion(0)

    def quitar_por_id(self, id_envio):
        """Elimina una solicitud por su ID. Devuelve True si la borro."""
        solicitud = self.buscar(id_envio)
        if solicitud is None:
            return False
        solicitud.marcar_cancelado()
        self._almacen = [s for s in self._almacen if s.id_envio != id_envio]
        return True

    def obtener_por_posicion(self, posicion):
        self._exigir_datos()
        if posicion < 0 or posicion >= self.tamanio():
            raise IndexError("Posicion fuera de rango")
        return self._almacen[posicion]

    def indice_de(self, id_envio):
        """Posicion (base 0) de una solicitud, o -1 si no esta."""
        for indice, solicitud in enumerate(self._almacen):
            if solicitud.id_envio == id_envio:
                return indice
        return -1

    # --- Reordenamiento ---

    def mover_a_inicio(self, id_envio):
        """Sube una solicitud al principio. True si la movio."""
        indice = self.indice_de(id_envio)
        if indice <= 0:
            return False
        solicitud = self._almacen.pop(indice)
        self._almacen.insert(0, solicitud)
        return True

    def mover_arriba(self, id_envio):
        """Sube una solicitud una posicion (intercambio con la anterior)."""
        indice = self.indice_de(id_envio)
        if indice <= 0:
            return False
        self._almacen[indice - 1], self._almacen[indice] = (
            self._almacen[indice], self._almacen[indice - 1])
        return True

    def ordenar_por_prioridad(self):
        """Ordena la lista de mayor a menor urgencia, sin perder el orden
        de llegada entre solicitudes de la misma prioridad."""
        self._almacen.sort(key=lambda s: -s.peso_prioridad())
        return self.listar()

    def ordenar_por_id(self):
        self._almacen.sort(key=lambda s: s.id_envio)
        return self.listar()

    def invertir(self):
        self._almacen.reverse()
        return self.listar()

    def cancelar(self, id_envio):
        """Alias de quitar_por_id para mantener la misma interfaz de la
        cola y la pila."""
        return self.quitar_por_id(id_envio)

    # --- Detalles internos ---

    def _validar(self, solicitud):
        if not isinstance(solicitud, Solicitud):
            raise TypeError("Solo se agregan objetos Solicitud")

    def _quitar_de_posicion(self, posicion):
        return self._almacen.pop(posicion)
