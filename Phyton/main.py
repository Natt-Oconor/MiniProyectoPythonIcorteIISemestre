"""
SIGEPE - Sistema de Gestion de Envios y Paqueteria Empresarial
Punto de entrada unico del proyecto.

    python main.py              abre la ventana grafica
    python main.py --consola    abre el menu de texto
    python main.py --pruebas    corre las pruebas automaticas
    python main.py --estructura COLA   arranca en consola con esa estructura

El sistema esta separado en capas, cada una en su carpeta:

    modelos/          clases de datos (Solicitud, Repartidor)
    estructura_datos/ COLA (FIFO), PILA (LIFO) y LISTA, cada una en su subcarpeta
    procesos/         reglas de negocio: registro, asignacion, cancelacion, consulta
    utilidades/       funciones sueltas de validacion y de formato
    interfaz/consola/ menu de texto
    interfaz/grafica/ ventana con tkinter (formulario para ingresar datos)
    pruebas/          pruebas automaticas de las 3 estructuras
"""

import argparse
import os
import sys

CARPETA_AQUI = os.path.dirname(os.path.abspath(__file__))
if CARPETA_AQUI not in sys.path:
    sys.path.insert(0, CARPETA_AQUI)


def preparar_consola():
    """Evita errores de acentos en consolas antiguas de Windows."""
    for flujo in (sys.stdout, sys.stderr):
        reconfigurar = getattr(flujo, "reconfigure", None)
        if reconfigurar is not None:
            try:
                reconfigurar(encoding="utf-8", errors="replace")
            except (ValueError, OSError):
                pass


def hay_tkinter():
    try:
        import tkinter  # noqa: F401
        return True
    except ImportError:
        return False


def mostrar_banner():
    print("=" * 70)
    print("  SIGEPE - Sistema de Gestion de Envios y Paqueteria")
    print("  Estructuras lineales: LISTA  |  PILA (LIFO)  |  COLA (FIFO)")
    print("=" * 70)


def correr_consola(estructura=None):
    from interfaz.consola.menu_consola import main as menu_consola
    menu_consola(estructura_inicial=estructura)


def correr_grafica():
    from interfaz.grafica.ventana_principal import ejecutar
    ejecutar()


def correr_pruebas(verbosidad=1):
    from pruebas import ejecutar_todas
    print(ejecutar_todas(verbosidad=verbosidad))


def leer_argumentos():
    analizador = argparse.ArgumentParser(
        prog="SIGEPE",
        description="Sistema de gestion de envios con estructuras lineales.")
    analizador.add_argument("--consola", action="store_true",
                            help="usar el menu de texto en vez de la ventana")
    analizador.add_argument("--pruebas", action="store_true",
                            help="correr las pruebas automaticas y salir")
    analizador.add_argument("--estructura", choices=["COLA", "PILA", "LISTA"],
                            help="estructura lineal inicial (modo consola)")
    analizador.add_argument("--version", action="version", version="SIGEPE 2.0")
    return analizador.parse_args()


def main():
    preparar_consola()
    argumentos = leer_argumentos()

    if argumentos.pruebas:
        mostrar_banner()
        correr_pruebas()
        return 0

    if argumentos.consola or argumentos.estructura:
        mostrar_banner()
        correr_consola(argumentos.estructura)
        return 0

    if not hay_tkinter():
        print()
        print("  No se encontro tkinter en este sistema, asi que no se puede")
        print("  abrir la ventana grafica. Se inicia la version de consola.")
        print("  Para instalarlo:  python main.py --consola  (ya esta activo)")
        print()
        correr_consola()
        return 0

    mostrar_banner()
    try:
        correr_grafica()
    except Exception as error:
        print(f"  No se pudo abrir la ventana grafica: {error}")
        print("  Se inicia la version de consola.")
        print()
        correr_consola()
    return 0


if __name__ == "__main__":
    sys.exit(main())
