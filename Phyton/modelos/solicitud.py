"""
Capa MODELOS - Clase Solicitud.

Define el objeto de negocio que se guarda dentro de las estructuras lineales
(lista, pila y cola). Solo datos y su propio comportamiento de estado.
No conoce las estructuras de datos ni la interfaz.
"""

ESTADO_PENDIENTE = "Pendiente"
ESTADO_EN_RUTA = "En Ruta"
ESTADO_ENTREGADO = "Entregado"
ESTADO_CANCELADO = "Cancelado"

ESTADOS_VALIDOS = (
    ESTADO_PENDIENTE,
    ESTADO_EN_RUTA,
    ESTADO_ENTREGADO,
    ESTADO_CANCELADO,
)

PRIORIDAD_BAJA = "Baja"
PRIORIDAD_NORMAL = "Normal"
PRIORIDAD_ALTA = "Alta"
PRIORIDAD_URGENTE = "Urgente"

PRIORIDADES_VALIDAS = (
    PRIORIDAD_BAJA,
    PRIORIDAD_NORMAL,
    PRIORIDAD_ALTA,
    PRIORIDAD_URGENTE,
)

# Orden de urgencia: mayor numero = mas urgente (sirve para ordenar la lista).
PESO_PRIORIDAD = {
    PRIORIDAD_BAJA: 1,
    PRIORIDAD_NORMAL: 2,
    PRIORIDAD_ALTA: 3,
    PRIORIDAD_URGENTE: 4,
}


class Solicitud:
    """Solicitud de envío pendiente de asignación."""

    def __init__(self, id_envio, cliente, direccion, descripcion,
                 prioridad=PRIORIDAD_NORMAL):
        self.id_envio = id_envio
        self.cliente = cliente
        self.direccion = direccion
        self.descripcion = descripcion
        self.prioridad = prioridad
        # Ciclo de vida: Pendiente -> En Ruta -> Entregado / Cancelado
        self.estado = ESTADO_PENDIENTE

    # --- Comportamiento propio del modelo ---

    def marcar_en_ruta(self):
        self.estado = ESTADO_EN_RUTA

    def marcar_entregado(self):
        self.estado = ESTADO_ENTREGADO

    def marcar_cancelado(self):
        self.estado = ESTADO_CANCELADO

    def esta_pendiente(self):
        return self.estado == ESTADO_PENDIENTE

    def peso_prioridad(self):
        return PESO_PRIORIDAD.get(self.prioridad, PESO_PRIORIDAD[PRIORIDAD_NORMAL])

    def a_lista(self):
        """Convierte la solicitud en una fila de 5 columnas para la tabla."""
        return (self.id_envio, self.cliente, self.direccion,
                self.descripcion, self.prioridad, self.estado)

    def __eq__(self, otro):
        if not isinstance(otro, Solicitud):
            return NotImplemented
        return self.id_envio == otro.id_envio

    def __hash__(self):
        return hash(self.id_envio)

    def __repr__(self):
        return (f"Solicitud(id={self.id_envio!r}, cliente={self.cliente!r}, "
                f"estado={self.estado!r})")

    def __str__(self):
        return (f"[{self.id_envio}] {self.cliente} | {self.direccion} | "
                f"{self.descripcion} | Prioridad: {self.prioridad} | "
                f"Estado: {self.estado}")
