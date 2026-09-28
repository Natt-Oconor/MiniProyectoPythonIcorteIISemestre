"""
Capa PROCESOS - Proceso de CONSULTA y ESTADISTICAS.

Consultar es: ver el contenido de la estructura, filtrarlo y resumirlo.
Todas son funciones puras: reciben una estructura y devuelven informacion,
sin modificarla.
"""

from modelos.solicitud import (
    ESTADO_EN_RUTA,
    ESTADO_PENDIENTE,
    PRIORIDADES_VALIDAS,
)
from estructura_datos.colas.cola_envios import ColaEnvios
from estructura_datos.listas.lista_solicitudes import ListaSolicitudes
from estructura_datos.pilas.pila_envios import PilaEnvios


def pendientes(estructura):
    """Solicitudes que siguen esperando asignacion."""
    return [s for s in estructura.listar() if s.estado == ESTADO_PENDIENTE]


def proxima(estructura):
    """La solicitud que sale primero, o None si esta vacia."""
    if estructura.esta_vacia():
        return None
    return estructura.siguiente()


def buscar_por_id(estructura, id_envio):
    return estructura.buscar(id_envio)


def buscar_por_cliente(estructura, texto):
    texto = (texto or "").strip().lower()
    if not texto:
        return []
    return [s for s in estructura.listar() if texto in s.cliente.lower()]


def buscar_por_direccion(estructura, texto):
    texto = (texto or "").strip().lower()
    if not texto:
        return []
    return [s for s in estructura.listar() if texto in s.direccion.lower()]


def filtrar_por_prioridad(estructura, prioridad):
    prioridad = (prioridad or "").strip()
    if not prioridad:
        return estructura.listar()
    return [s for s in estructura.listar() if s.prioridad == prioridad]


def ordenar(estructura, criterio="orden"):
    """Ordena una copia de la lista segun un criterio.

    criterios: orden, prioridad, cliente, id
    """
    datos = estructura.listar()
    if criterio == "prioridad":
        return sorted(datos, key=lambda s: -s.peso_prioridad())
    if criterio == "cliente":
        return sorted(datos, key=lambda s: s.cliente.lower())
    if criterio == "id":
        return sorted(datos, key=lambda s: s.id_envio)
    return datos


def nombre_estructura(estructura):
    return type(estructura).__name__


def criterio_estructura(estructura):
    """Texto que explica por que se eligio esa estructura."""
    if isinstance(estructura, ColaEnvios):
        return "COLA (FIFO) - la primera en entrar es la primera en salir."
    if isinstance(estructura, PilaEnvios):
        return "PILA (LIFO) - la ultima en entrar es la primera en salir."
    if isinstance(estructura, ListaSolicitudes):
        return "LISTA - acceso por posicion, busqueda y reordenamiento."
    return "ESTRUCTURA LINEAL"


def descripcion_operaciones(estructura):
    """Lista de operaciones disponibles segun la estructura."""
    base = ["agregar", "quitar", "siguiente", "esta_vacia", "tamanio",
            "listar", "buscar", "cancelar"]
    if isinstance(estructura, ColaEnvios):
        extra = ["encolar", "desencolar", "frente", "orden_atencion"]
    elif isinstance(estructura, PilaEnvios):
        extra = ["apilar", "desapilar", "cima", "orden_salida"]
    else:
        extra = ["agregar_al_inicio", "quitar_por_id", "indice_de",
                 "mover_a_inicio", "ordenar_por_prioridad"]
    return base + extra


def estadisticas(estructura):
    """Resumen numerico de lo que hay dentro de la estructura."""
    datos = estructura.listar()
    por_estado = {}
    por_prioridad = {p: 0 for p in PRIORIDADES_VALIDAS}
    for solicitud in datos:
        por_estado[solicitud.estado] = por_estado.get(solicitud.estado, 0) + 1
        por_prioridad[solicitud.prioridad] = por_prioridad.get(solicitud.prioridad, 0) + 1

    siguientes = ""
    if datos:
        siguiente = estructura.siguiente()
        siguientes = f"#{siguiente.id_envio} {siguiente.cliente}"

    return {
        "estructura": nombre_estructura(estructura),
        "criterio": criterio_estructura(estructura).split(" - ")[0],
        "total_elementos": len(datos),
        "pendientes": por_estado.get(ESTADO_PENDIENTE, 0),
        "en_ruta": por_estado.get(ESTADO_EN_RUTA, 0),
        "siguiente_en_salir": siguientes,
        "por_prioridad": por_prioridad,
        "clientes": len({s.cliente for s in datos}),
        "operaciones": len(descripcion_operaciones(estructura)),
    }
