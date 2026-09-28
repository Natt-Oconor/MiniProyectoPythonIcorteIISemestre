"""
Capa ESTRUCTURA DE DATOS - Seleccion de la estructura lineal apropiada.

Este paquete tiene una subcarpeta por cada estructura lineal, y dentro de
ella la clase que la implementa:

    estructura_datos/
        base.py                -> EstructuraLineal (contrato comun)
        listas/                -> ListaSolicitudes   (acceso por posicion)
        pilas/                 -> PilaEnvios         (LIFO)
        colas/                 -> ColaEnvios         (FIFO)

Criterio de seleccion:

    ¿Importa el orden de llegada?        -> COLA   (FIFO)
    ¿Importa la peticion mas reciente?   -> PILA   (LIFO)
    ¿Hay que buscar o reordenar?         -> LISTA

Regla: la lista es la estructura generica; la pila y la cola son listas con
la regla de insercion y extraccion restringida a un solo extremo.
"""

from estructura_datos.base import (
    ColaVaciaError,
    EstructuraLineal,
    EstructuraVaciaError,
)
from estructura_datos.listas import ListaSolicitudes
from estructura_datos.pilas import PilaEnvios
from estructura_datos.colas import ColaEnvios

# Registro de estructuras disponibles, para la interfaz y las pruebas.
ESTRUCTURAS = {
    "COLA": ColaEnvios,
    "PILA": PilaEnvios,
    "LISTA": ListaSolicitudes,
}

CRITERIO_SELECCION = {
    "COLA": "El orden de llegada manda: la primera que entra, sale primero.",
    "PILA": "La peticion mas reciente es la prioritaria: la ultima que entra, sale primero.",
    "LISTA": "Se necesita buscar por ID, insertar en cualquier posicion o reordenar.",
}

__all__ = [
    "EstructuraLineal",
    "ColaVaciaError",
    "EstructuraVaciaError",
    "ColaEnvios",
    "PilaEnvios",
    "ListaSolicitudes",
    "ESTRUCTURAS",
    "CRITERIO_SELECCION",
]
