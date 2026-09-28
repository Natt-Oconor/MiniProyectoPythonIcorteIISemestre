"""
Interfaz CONSOLA - Version de texto del SIGEPE.

Se usa cuando la ventana grafica no esta disponible (por ejemplo, si el
sistema no tiene tkinter instalado) o cuando se pide explicitamente con:

    python main.py --consola
"""

from interfaz.consola.entradas import (
    pedir_confirmacion,
    pedir_corte,
    pedir_entero,
    pedir_opcion,
    pedir_prioridad,
    pedir_repartidor,
    pedir_texto,
)
from interfaz.consola.menu_consola import Sesion, main, mostrar_menu, mostrar_bienvenida

__all__ = [
    "main",
    "Sesion",
    "mostrar_menu",
    "mostrar_bienvenida",
    "pedir_texto",
    "pedir_entero",
    "pedir_opcion",
    "pedir_prioridad",
    "pedir_confirmacion",
    "pedir_repartidor",
    "pedir_corte",
]
