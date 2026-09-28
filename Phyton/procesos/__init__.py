"""
Capa PROCESOS - Reglas de negocio del SIGEPE.

Un proceso es una operacion del negocio que coordina varias piezas:
valida datos, usa una estructura lineal y devuelve un resultado.

    registro.py      -> registrar solicitudes
    asignacion.py    -> repartir solicitudes a los repartidores
    cancelacion.py   -> dar de baja solicitudes
    consulta.py      -> listar, filtrar y resumir

Ninguna de estas funciones imprime en pantalla: devuelven datos. Quien
muestra los resultados es la capa interfaz.
"""

from procesos import asignacion, cancelacion, consulta, registro
from procesos.registro import (
    GeneradorIds,
    registrar_lote,
    registrar_solicitud,
    registrar_varias,
)
from procesos.asignacion import (
    HistorialAsignaciones,
    asignar_prioridad_alta,
    asignar_por_id,
    asignar_siguiente,
    asignar_todas,
    marcar_entregado,
)
from procesos.cancelacion import (
    cancelar_cliente,
    cancelar_solicitud,
    cancelar_todas,
    cancelar_ultima,
)
from procesos.consulta import (
    buscar_por_cliente,
    buscar_por_id,
    estadisticas,
    filtrar_por_prioridad,
    ordenar,
    pendientes,
    proxima,
)

__all__ = [
    "registro", "asignacion", "cancelacion", "consulta",
    "GeneradorIds", "registrar_solicitud", "registrar_varias", "registrar_lote",
    "HistorialAsignaciones", "asignar_siguiente", "asignar_por_id",
    "asignar_prioridad_alta", "asignar_todas", "marcar_entregado",
    "cancelar_solicitud", "cancelar_ultima", "cancelar_todas", "cancelar_cliente",
    "pendientes", "proxima", "buscar_por_id", "buscar_por_cliente",
    "filtrar_por_prioridad", "ordenar", "estadisticas",
]
