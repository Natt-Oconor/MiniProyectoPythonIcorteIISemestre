"""
PRUEBAS - Modulo de arranque.

Ademas de los(unittest.TestCase) de test_estructuras.py, ofrece
`ejecutar_todas()`, que corre la suite completa y devuelve un resumen
de texto. Eso es lo que usan el menu de la consola y el boton
"Ejecutar pruebas automaticas" de la ventana.
"""

import io
import os
import sys
import unittest

CARPETA_PRUEBAS = os.path.dirname(os.path.abspath(__file__))
CARPETA_PROYECTO = os.path.dirname(CARPETA_PRUEBAS)


def construir_suite():
    """Arma la suite con todos los modulos de prueba de la carpeta."""
    if CARPETA_PROYECTO not in sys.path:
        sys.path.insert(0, CARPETA_PROYECTO)
    loader = unittest.TestLoader()
    return loader.discover(start_dir=CARPETA_PRUEBAS, pattern="test_*.py",
                           top_level_dir=CARPETA_PROYECTO)


def ejecutar_todas(verbosidad=0):
    """Corre todas las pruebas. Devuelve un resumen listo para mostrar."""
    buffer = io.StringIO()
    corredor = unittest.TextTestRunner(stream=buffer, verbosity=verbosidad)
    resultado = corredor.run(construir_suite())

    lineas = [linea for linea in buffer.getvalue().splitlines() if linea.strip()]
    detalle = "\n".join(lineas[-6:]) if lineas else ""
    veredicto = "TODO CORRECTO" if resultado.wasSuccessful() else "HAY FALLOS"
    if resultado.wasSuccessful():
        return (f"Veredicto: {veredicto}\n"
                f"Pruebas ejecutadas: {resultado.testsRun}\n\n"
                f"Cola (FIFO) - la mas antigua sale primero.\n"
                f"Pila (LIFO) - la mas reciente sale primero.\n"
                f"Lista      - acceso por posicion, busqueda y reordenamiento.\n\n"
                f"{detalle}")
    return f"Veredicto: {veredicto}\n{detalle}"


if __name__ == "__main__":
    print(ejecutar_todas(verbosidad=1))
