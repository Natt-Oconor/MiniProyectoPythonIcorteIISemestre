"""
Capa MODELOS - Clase Repartidor.

Persona que recibe las solicitudes asignadas. Lleva su propio contador de
entregas para poder mostrar productividad.
"""


class Repartidor:
    """Repartidor disponible para asignar envíos."""

    def __init__(self, nombre, zona="Sin zona", entregas=0):
        self.nombre = nombre
        self.zona = zona
        self.entregas = entregas

    def registrar_entrega(self):
        self.entregas += 1

    def __eq__(self, otro):
        if not isinstance(otro, Repartidor):
            return NotImplemented
        return self.nombre == otro.nombre

    def __hash__(self):
        return hash(self.nombre)

    def __repr__(self):
        return f"Repartidor(nombre={self.nombre!r}, zona={self.zona!r})"

    def __str__(self):
        return f"{self.nombre} ({self.zona}) - entregas: {self.entregas}"
