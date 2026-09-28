"""
Capa ESTRUCTURA DE DATOS - Clase base abstracta.

Define el contrato comun a las tres estructuras lineales del proyecto:
lista, pila y cola. Cada subcarpeta implementa un unico metodo clave
(`agregar` / quitar) y el comportamiento especifico de su estructura.
"""

from abc import ABC, abstractmethod


class EstructuraLineal(ABC):
    """Contrato minimo comun a lista, pila y cola de solicitudes."""

    # --- Metodos que cada estructura debe definir ---

    @abstractmethod
    def agregar(self, solicitud):
        """Inserta una solicitud en la estructura."""

    @abstractmethod
    def quitar(self):
        """Saca la solicitud que corresponda segun el criterio de la
        estructura (el frente en la cola, la cima en la pila)."""

    @abstractmethod
    def siguiente(self):
        """Consulta la solicitud que seria la proxima en salir, sin sacarla."""

    # --- Metodos comunes, ya resueltos para las tres estructuras ---

    def esta_vacia(self):
        return self.tamanio() == 0

    def tamanio(self):
        return len(self._almacen)

    def listar(self):
        """Devuelve una copia de los elementos en su orden interno."""
        return list(self._almacen)

    def buscar(self, id_envio):
        """Devuelve la solicitud con ese ID o None si no existe."""
        for solicitud in self._almacen:
            if solicitud.id_envio == id_envio:
                return solicitud
        return None

    def existe(self, id_envio):
        return self.buscar(id_envio) is not None

    def ids(self):
        return [solicitud.id_envio for solicitud in self._almacen]

    def _exigir_datos(self):
        if self.esta_vacia():
            raise EstructuraVaciaError("No hay solicitudes pendientes")

    def _cancelar_en_memoria(self, id_envio):
        """Marca como cancelada la solicitud indicada (sin quitarla)."""
        solicitud = self.buscar(id_envio)
        if solicitud is None:
            return False
        solicitud.marcar_cancelado()
        return True

    def __len__(self):
        return self.tamanio()

    def __contains__(self, id_envio):
        return self.existe(id_envio)

    def __iter__(self):
        return iter(self._almacen)

    def __str__(self):
        return (f"{type(self).__name__} con {self.tamanio()} "
                f"solicitud(es) pendiente(s)")


class EstructuraVaciaError(IndexError):
    """Se pidio sacar un elemento de una estructura sin elementos.

    Hereda de IndexError para no romper el codigo del modulo original
    (sige siendo atrapable con `except IndexError`).
    """


# Alias historico: el modulo original solo tenia cola.
ColaVaciaError = EstructuraVaciaError
