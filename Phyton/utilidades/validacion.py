"""
Capa UTILIDADES - Funciones de validacion.

Son FUNCIONES sueltas (no metodos de ninguna clase). Sirven tanto a la
interfaz de consola como a la interfaz grafica, para no repetir la
validacion de los datos en dos lugares distintos.
"""

from modelos.solicitud import PRIORIDADES_VALIDAS

MENSAJE_VACIO = "El campo no puede estar vacío."


def no_vacio(valor):
    """True si el texto tiene contenido real."""
    return bool(valor) and bool(str(valor).strip())


def normalizar_texto(valor):
    """Quita espacios sobrantes de los dos extremos."""
    if valor is None:
        return ""
    return str(valor).strip()


def es_entero(valor):
    """True si el valor se puede convertir a numero entero."""
    try:
        int(str(valor).strip())
        return True
    except (TypeError, ValueError):
        return False


def es_prioridad_valida(valor):
    """True si la prioridad es una de las cuatro permitidas."""
    return normalizar_texto(valor) in PRIORIDADES_VALIDAS


def validar_texto(valor, campo="Campo", minimo=1, maximo=60):
    """Valida un texto. Devuelve (texto_limpio, None) o (None, error)."""
    limpio = normalizar_texto(valor)
    if not limpio:
        return None, f"{campo}: {MENSAJE_VACIO}"
    if len(limpio) < minimo:
        return None, f"{campo}: debe tener al menos {minimo} caracter(es)."
    if len(limpio) > maximo:
        return None, f"{campo}: maximo {maximo} caracter(es)."
    return limpio, None


def validar_entero(valor, campo="Numero", minimo=None, maximo=None):
    """Valida un entero. Devuelve (numero, None) o (None, error)."""
    texto = normalizar_texto(valor)
    if not texto:
        return None, f"{campo}: {MENSAJE_VACIO}"
    if not es_entero(texto):
        return None, f"{campo}: '{texto}' no es un numero valido."
    numero = int(texto)
    if minimo is not None and numero < minimo:
        return None, f"{campo}: debe ser mayor o igual a {minimo}."
    if maximo is not None and numero > maximo:
        return None, f"{campo}: debe ser menor o igual a {maximo}."
    return numero, None


def validar_prioridad(valor):
    """Valida la prioridad. Si viene vacia, deja 'Normal'."""
    limpio = normalizar_texto(valor)
    if not limpio:
        return PRIORIDADES_VALIDAS[1], None
    if not es_prioridad_valida(limpio):
        opciones = ", ".join(PRIORIDADES_VALIDAS)
        return None, f"Prioridad: debe ser una de: {opciones}."
    return limpio, None


def validar_solicitud(cliente, direccion, descripcion, prioridad="Normal"):
    """Valida los 4 datos del formulario de una sola vez.

    Devuelve (datos_limpios, None) si todo esta bien, o (None, lista_de_errores).
    """
    errores = []
    resultado = {}

    for campo, valor, largo in (
        ("Cliente", cliente, 40),
        ("Direccion", direccion, 80),
        ("Descripcion", descripcion, 80),
    ):
        limpio, error = validar_texto(valor, campo, minimo=2, maximo=largo)
        if error:
            errores.append(error)
        else:
            resultado[campo.lower()] = limpio

    prioridad_limpia, error = validar_prioridad(prioridad)
    if error:
        errores.append(error)
    else:
        resultado["prioridad"] = prioridad_limpia

    if errores:
        return None, errores
    return resultado, None
