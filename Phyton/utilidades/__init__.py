"""
Capa UTILIDADES - Funciones de apoyo reutilizables.

    validacion.py  -> funciones que revisan los datos que ingresa el usuario
    formato.py     -> funciones que arman los textos y tablas de pantalla

Ninguna de las dos clases de datos: no guardan estado, solo Transforman o
comprueban valores.
"""

from utilidades import formato, validacion

__all__ = ["validacion", "formato"]
