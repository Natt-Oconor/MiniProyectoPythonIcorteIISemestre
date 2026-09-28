"""
Capa UTILIDADES - Funciones de formato.

Funciones sueltas que arman los textos y tablas que se ven en pantalla.
Se usan en la consola y tambien en la parte baja de la ventana grafica.
"""

from modelos.solicitud import ESTADO_PENDIENTE

ANCHO = 78


def linea(caracter="-", ancho=ANCHO):
    return caracter * ancho


def titulo(texto):
    return f"\n{linea('=')}\n  {texto}\n{linea('=')}"


def subtitulo(texto):
    return f"\n{texto}\n{linea('-')}"


def fila_tabla(valores, anchos):
    """Arma una fila de tabla respetando el ancho de cada columna."""
    partes = []
    for valor, ancho in zip(valores, anchos):
        texto = str(valor)
        if len(texto) > ancho:
            texto = texto[:ancho - 1] + "."
        partes.append(texto.ljust(ancho))
    return "  " + " | ".join(partes)


def tabla_solicitudes(solicitudes):
    """Devuelve la tabla de solicitudes como lista de lineas de texto."""
    if not solicitudes:
        return ["  No hay solicitudes pendientes."]

    anchos = (5, 18, 22, 26, 9, 11)
    encabezados = ("ID", "CLIENTE", "DIRECCION", "DESCRIPCION", "PRIORIDAD", "ESTADO")
    lineas = [fila_tabla(encabezados, anchos), linea("-", 96)]
    for posicion, solicitud in enumerate(solicitudes, start=1):
        valores = (solicitud.id_envio,) + tuple(solicitud.a_lista()[1:])
        lineas.append(fila_tabla(valores, anchos))
    lineas.append(linea("-", 96))
    lineas.append(f"  Total: {len(solicitudes)} solicitud(es)")
    return lineas


def tabla_simple(elementos, vacio="No hay elementos."):
    if not elementos:
        return [f"  {vacio}"]
    return [f"  {pos}. {elemento}" for pos, elemento in enumerate(elementos, 1)]


def estadisticas_texto(estadisticas):
    """Convierte el diccionario de estadisticas en lineas legibles."""
    lineas = [linea("-")]
    for clave, valor in estadisticas.items():
        etiqueta = clave.replace("_", " ").capitalize()
        lineas.append(f"  {etiqueta.ljust(22)}: {valor}")
    lineas.append(linea("-"))
    return lineas


def marcar(texto, condicion):
    """Agrega un visto bueno o una advertencia al final de un texto."""
    return f"{texto}  [OK]" if condicion else f"{texto}  [FALLA]"


def resumen_solicitud(solicitud):
    """Texto corto de una solicitud, para barras de estado y mensajes."""
    if solicitud is None:
        return "Sin solicitud"
    return (f"#{solicitud.id_envio} {solicitud.cliente} - "
            f"{solicitud.direccion} ({solicitud.estado})")


def texto_estado_pendiente(cantidad):
    if cantidad == 1:
        return "1 solicitud pendiente"
    return f"{cantidad} solicitudes pendientes"


def asegurar_pendiente(estado):
    return estado == ESTADO_PENDIENTE
