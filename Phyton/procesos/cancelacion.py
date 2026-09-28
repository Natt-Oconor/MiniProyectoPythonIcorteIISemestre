"""
Capa PROCESOS - Proceso de CANCELACION.

Cancelar es: localizar la solicitud por su ID, marcarla como "Cancelado"
y quitarla de la estructura para que deje de consumir turno de reparto.
"""

from estructura_datos.base import EstructuraVaciaError
from utilidades.formato import texto_estado_pendiente


def cancelar_solicitud(estructura, id_envio):
    """Cancela una solicitud por su ID.

    Devuelve (True, None) si se cancelo, o (False, motivo).
    """
    try:
        cancelada = estructura.cancelar(id_envio)
    except EstructuraVaciaError:
        return False, "No hay solicitudes pendientes."
    except AttributeError:
        return False, "Esta estructura no admite cancelacion."

    if cancelada:
        return True, f"Solicitud #{id_envio} cancelada."
    return False, f"No se encontro la solicitud #{id_envio} en la estructura."


def cancelar_ultima(estructura):
    """Cancela la solicitud que sale primero (frente de la cola / cima)."""
    solicitud = estructura.siguiente()
    return cancelar_solicitud(estructura, solicitud.id_envio)


def cancelar_todas(estructura):
    """Vacia la estructura cancelando todo. Devuelve cuantas cancelo."""
    canceladas = 0
    while not estructura.esta_vacia():
        solicitud = estructura.siguiente()
        ok, _ = cancelar_solicitud(estructura, solicitud.id_envio)
        if not ok:
            break
        canceladas += 1
    return canceladas


def cancelar_cliente(estructura, nombre_cliente):
    """Cancela todas las solicitudes de un cliente. Devuelve la cantidad."""
    a_cancelar = [s.id_envio for s in estructura.listar()
                  if s.cliente.strip().lower() == nombre_cliente.strip().lower()]
    canceladas = 0
    for id_envio in a_cancelar:
        ok, _ = cancelar_solicitud(estructura, id_envio)
        if ok:
            canceladas += 1
    return canceladas


def aviso_si_vacia(estructura):
    """Mensaje de ayuda cuando no hay nada que mostrar."""
    if estructura.esta_vacia():
        return "No hay solicitudes pendientes."
    return texto_estado_pendiente(estructura.tamanio())
