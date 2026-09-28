"""
Interfaz CONSOLA - Captura de datos por teclado.

Envoltorios de input() que no repiten la validacion: la logica esta en
utilidades/validacion.py, aqui solo se pide y se reintenta.
"""

from modelos.solicitud import PRIORIDADES_VALIDAS
from utilidades.validacion import (
    validar_entero,
    validar_texto,
)


def pedir_texto(mensaje, minimo=1, maximo=60, campo="El campo"):
    """Pide un texto y no permite dejarlo vacio."""
    while True:
        valor = input(mensaje).strip()
        if not valor:
            print(f"  {campo} no puede estar vacio. Intenta de nuevo.")
            continue
        if len(valor) < minimo:
            print(f"  {campo} debe tener al menos {minimo} caracteres.")
            continue
        if len(valor) > maximo:
            print(f"  {campo} maximo {maximo} caracteres.")
            continue
        return valor


def pedir_entero(mensaje, minimo=None, maximo=None, campo="Numero"):
    """Pide un numero entero valido."""
    while True:
        valor = input(mensaje).strip()
        if not valor:
            print("  Ingresa un numero valido.")
            continue
        numero, error = validar_entero(valor, campo, minimo, maximo)
        if error:
            print(f"  {error} Intenta de nuevo.")
            continue
        return numero


def pedir_opcion(mensaje, validas):
    """Pide una opcion de menu, reintentando hasta que sea valida."""
    validas = [str(v) for v in validas]
    while True:
        opcion = input(mensaje).strip()
        if opcion in validas:
            return opcion
        print(f"  Opcion no valida. Elige entre: {', '.join(validas)}")


def pedir_prioridad(mensaje="Prioridad (Baja/Normal/Alta/Urgente) [Normal]: "):
    """Pide la prioridad; si se deja vacia usa 'Normal'."""
    print(f"  Opciones: {', '.join(PRIORIDADES_VALIDAS)}")
    while True:
        valor = input(mensaje).strip() or PRIORIDADES_VALIDAS[1]
        if valor in PRIORIDADES_VALIDAS:
            return valor
        print("  Prioridad no valida. Intenta de nuevo.")


def pedir_confirmacion(mensaje, por_defecto=False):
    """Pide confirmacion si/no."""
    pista = "S/n" if por_defecto else "s/N"
    while True:
        valor = input(f"{mensaje} [{pista}] ").strip().lower()
        if not valor:
            return por_defecto
        if valor in ("s", "si", "y", "yes"):
            return True
        if valor in ("n", "no"):
            return False
        print("  Responde s o n.")


def pedir_repartidor(mensaje="Nombre del repartidor: "):
    nombre = input(mensaje).strip()
    return nombre or "Repartidor 1"


def pedir_corte(mensaje="Texto a buscar: "):
    return pedir_texto(mensaje, minimo=1, maximo=40, campo="La busqueda")


__all__ = [
    "pedir_texto",
    "pedir_entero",
    "pedir_opcion",
    "pedir_prioridad",
    "pedir_confirmacion",
    "pedir_repartidor",
    "pedir_corte",
    "validar_texto",
]
