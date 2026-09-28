"""
Capa PROCESOS - Proceso de ASIGNACION.

Asignar es: tomar la solicitud que la estructura considera la proxima
(el frente de la COLA, la cima de la PILA, la primera de la LISTA),
sacarla de la estructura y pasarla a estado "En Ruta".

Como el metodo comun se llama `quitar`, este proceso funciona igual para
las tres estructuras sin cambiar una linea de codigo.
"""

from modelos.repartidor import Repartidor
from estructura_datos.base import EstructuraVaciaError
from utilidades.validacion import normalizar_texto


class HistorialAsignaciones:
    """Historial de asignaciones guardado en PILA (LIFO).

    Es un buen ejemplo de uso natural de la pila: al revisar el historial
    se quiere ver primero lo ultimo que ocurrio.
    """

    def __init__(self):
        self._pila = []

    def registrar(self, solicitud, repartidor):
        self._pila.append((solicitud, repartidor))
        return solicitud

    def mas_reciente(self):
        if not self._pila:
            return None
        return self._pila[-1]

    def ver_todo(self):
        """Del mas reciente al mas antiguo (orden de pila)."""
        return list(reversed(self._pila))

    def desenrollar(self, cantidad=1):
        """Saca las ultimas asignaciones, de la mas reciente a la mas vieja."""
        sacadas = []
        for _ in range(cantidad):
            if not self._pila:
                break
            sacadas.append(self._pila.pop())
        return list(reversed(sacadas))

    def limpiar(self):
        self._pila.clear()

    def total(self):
        return len(self._pila)

    def __len__(self):
        return len(self._pila)


def _preparar_repartidor(repartidor):
    """Acepta un Repartidor o un simple nombre de texto."""
    if isinstance(repartidor, Repartidor):
        return repartidor
    return Repartidor(normalizar_texto(repartidor) or "Repartidor sin nombre")


def asignar_siguiente(estructura, repartidor, historial=None):
    """Saca la proxima solicitud de la estructura y la asigna.

    Devuelve (solicitud, repartidor) o (None, motivo_del_error).
    """
    try:
        solicitud = estructura.quitar()
    except EstructuraVaciaError:
        return None, "No hay solicitudes pendientes para asignar."

    repartidor = _preparar_repartidor(repartidor)
    solicitud.marcar_en_ruta()
    repartidor.registrar_entrega()

    if historial is not None:
        historial.registrar(solicitud, repartidor)

    return solicitud, repartidor


def asignar_por_id(estructura, id_envio, repartidor, historial=None):
    """Asigna una solicitud concreta, sin importar su posicion.

    Solo tiene sentido en la LISTA, donde existe buscar por ID.
    """
    solicitud = estructura.buscar(id_envio)
    if solicitud is None:
        return None, f"No se encontro la solicitud #{id_envio}."

    if hasattr(estructura, "quitar_por_id"):
        estructura.quitar_por_id(id_envio)
    else:
        estructura.cancelar(id_envio)

    solicitud.marcar_en_ruta()
    repartidor = _preparar_repartidor(repartidor)
    repartidor.registrar_entrega()

    if historial is not None:
        historial.registrar(solicitud, repartidor)
    return solicitud, repartidor


def asignar_prioridad_alta(estructura, repartidor, historial=None):
    """Ordena por urgencia y asigna la mas urgente.

    Solo la LISTA sabe reordenarse por prioridad. En la COLA y la PILA el
    orden es fijo, asi que se asigna la que salga primero y se avisa.
    """
    aviso = ""
    if hasattr(estructura, "ordenar_por_prioridad"):
        estructura.ordenar_por_prioridad()
    else:
        aviso = (f"  Aviso: la {type(estructura).__name__} no se puede "
                 f"reordenar; se asigno la que sale primero.")
    solicitud, repartidor = asignar_siguiente(estructura, repartidor, historial)
    return solicitud, repartidor, aviso


def marcar_entregado(estructura, id_envio):
    """Cambia el estado de una solicitud a Entregado.

    La solicitud ya no esta en la estructura (fue asignada), por eso se
    busca en el historial de la interfaz.
    """
    solicitud = estructura.buscar(id_envio)
    if solicitud is None:
        return None, f"La solicitud #{id_envio} ya no esta en la estructura."
    solicitud.marcar_entregado()
    return solicitud, None


def asignar_todas(estructura, repartidor, historial=None):
    """Asigna una por una todas las solicitudes que queden en la estructura."""
    asignadas = []
    while not estructura.esta_vacia():
        solicitud, repartidor = asignar_siguiente(estructura, repartidor, historial)
        if solicitud is None:
            break
        asignadas.append((solicitud, repartidor))
    return asignadas
