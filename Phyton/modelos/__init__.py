"""
Capa MODELOS - Paquete de datos.

Aqui viven las clases de negocio. No deben importar ni estructura_datos,
ni procesos, ni interfaz: eso lo hace el resto de capas.
"""

from modelos.solicitud import (
    ESTADO_CANCELADO,
    ESTADO_EN_RUTA,
    ESTADO_ENTREGADO,
    ESTADO_PENDIENTE,
    ESTADOS_VALIDOS,
    PRIORIDAD_ALTA,
    PRIORIDAD_BAJA,
    PRIORIDAD_NORMAL,
    PRIORIDAD_URGENTE,
    PRIORIDADES_VALIDAS,
    PESO_PRIORIDAD,
    Solicitud,
)
from modelos.repartidor import Repartidor

__all__ = [
    "Solicitud",
    "Repartidor",
    "ESTADO_PENDIENTE",
    "ESTADO_EN_RUTA",
    "ESTADO_ENTREGADO",
    "ESTADO_CANCELADO",
    "ESTADOS_VALIDOS",
    "PRIORIDAD_BAJA",
    "PRIORIDAD_NORMAL",
    "PRIORIDAD_ALTA",
    "PRIORIDAD_URGENTE",
    "PRIORIDADES_VALIDAS",
    "PESO_PRIORIDAD",
]
