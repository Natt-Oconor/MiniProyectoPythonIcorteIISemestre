"""
Capa PROCESOS - Proceso de REGISTRO.

Registrar una solicitud es: validar los datos, Armar el objeto Solicitud,
generar su ID y encolarlo en la estructura elegida.

Este modulo no sabe si la estructura es lista, pila o cola: solo usa los
metodos comunes (agregar, esta_vacia, tamanio). Eso permite cambiar de
estructura sin tocar ningun proceso.
"""

from modelos.solicitud import PRIORIDAD_NORMAL, Solicitud
from utilidades.validacion import validar_solicitud


class GeneradorIds:
    """Genera los IDs de envio de forma correlativa y sin repetir."""

    def __init__(self, inicio=1):
        self._siguiente = inicio
        self._emitidos = 0

    def siguiente(self):
        valor = self._siguiente
        self._siguiente += 1
        self._emitidos += 1
        return valor

    def emitir(self, estructura):
        """Genera un ID que todavia no exista en la estructura."""
        id_envio = self.siguiente()
        while estructura.existe(id_envio):
            id_envio = self.siguiente()
        return id_envio

    def adoptar(self, ids_existentes):
        """Ajusta el generador para no repetir IDs ya cargados."""
        for id_envio in ids_existentes:
            if isinstance(id_envio, int) and id_envio >= self._siguiente:
                self._siguiente = id_envio + 1

    @property
    def emitidos(self):
        return self._emitidos

    def reiniciar(self, inicio=1):
        self._siguiente = inicio
        self._emitidos = 0


def registrar_solicitud(estructura, cliente, direccion, descripcion,
                        prioridad=PRIORIDAD_NORMAL, id_envio=None):
    """Agrega una solicitud validada a la estructura.

    Devuelve (solicitud_creada, None) o (None, [errores]).
    """
    datos, errores = validar_solicitud(cliente, direccion, descripcion, prioridad)
    if errores:
        return None, errores

    if id_envio is None:
        id_envio = len(estructura.listar()) + 1

    solicitud = Solicitud(id_envio, datos["cliente"], datos["direccion"],
                           datos["descripcion"], datos["prioridad"])
    estructura.agregar(solicitud)
    return solicitud, None


def registrar_varias(estructura, cantidad=5, prefijo="Cliente"):
    """Carga rapida de solicitudes de ejemplo (util para practicas)."""
    modelos = [
        ("Ana Perez", "Altamira", "Paquete pequeno"),
        ("Luis Mora", "Villa Fontana", "Documentos"),
        ("Rosa Gomez", "Bello Horizonte", "Comida"),
        ("Carlos Diaz", "Robledo", "Ropa"),
        ("Maria Lopez", "La Candelaria", "Medicamento"),
        ("Jorge Ruiz", "Envigado", "Electrodomestico"),
    ]
    creadas = []
    for indice in range(cantidad):
        nombre, direccion, descripcion = modelos[indice % len(modelos)]
        solicitud, errores = registrar_solicitud(
            estructura, nombre, direccion, descripcion)
        if not errores:
            creadas.append(solicitud)
    return creadas


def registrar_lote(estructura, filas):
    """Registra varias solicitudes de una lista de tuplas.

    filas = [(cliente, direccion, descripcion, prioridad), ...]
    Devuelve (creadas, errores).
    """
    creadas = []
    errores = []
    for fila in filas:
        cliente, direccion, descripcion = fila[0], fila[1], fila[2]
        prioridad = fila[3] if len(fila) > 3 else PRIORIDAD_NORMAL
        solicitud, error = registrar_solicitud(
            estructura, cliente, direccion, descripcion, prioridad)
        if error:
            errores.extend(error)
        else:
            creadas.append(solicitud)
    return creadas, errores
