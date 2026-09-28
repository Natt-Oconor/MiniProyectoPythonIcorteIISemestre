"""
Capa INTERFAZ - Presentacion del sistema.

Dos versiones del mismo sistema, sobre los mismos procesos:

    interfaz/consola/   menus de texto (funciona sin ventana)
    interfaz/grafica/   ventana con tkinter (formulario y tablas)

Regla de la capa: no se permiten `print` dentro de procesos ni estructuras
de datos. La interfaz pide, el proceso responde, la interfaz muestra.
"""

__all__ = ["consola", "grafica"]
