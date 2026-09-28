"""
Interfaz GRAFICA - Ventana del SIGEPE (tkinter).

    formulario_solicitud.py -> los datos que se ingresar
    pestana_estructura.py   -> una pestana por estructura lineal
    ventana_principal.py    -> arma toda la pantalla
    widgets.py              -> controles reutilizables

Si el sistema no tiene tkinter, importar este paquete no falla: la
aplicacion cae automaticamente en la version de consola.
"""

from interfaz.grafica.ventana_principal import TKINTER_DISPONIBLE

__all__ = ["TKINTER_DISPONIBLE"]
