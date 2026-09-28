"""
Interfaz CONSOLA - Menu principal por texto.

Es la version sin ventana grafica. Comparte los mismos procesos que la
interfaz grafica: aqui solo se pide el dato, se llama al proceso y se
imprime el resultado.
"""

from estructura_datos import ESTRUCTURAS, CRITERIO_SELECCION
from estructura_datos.base import EstructuraVaciaError
from procesos import asignacion, cancelacion, consulta, registro
from utilidades import formato
from interfaz.consola.entradas import (
    pedir_confirmacion,
    pedir_entero,
    pedir_opcion,
    pedir_prioridad,
    pedir_repartidor,
    pedir_texto,
)

OPCION_SALIR = "0"


class Sesion:
    """Guarda el estado de la sesion: las 3 estructuras y el historial."""

    def __init__(self):
        self.estructuras = {nombre: clase() for nombre, clase in ESTRUCTURAS.items()}
        self.actual = "COLA"
        self.generador = registro.GeneradorIds()
        self.historial = asignacion.HistorialAsignaciones()

    @property
    def estructura(self):
        return self.estructuras[self.actual]


# --- Pantallas ---

def mostrar_bienvenida():
    print(formato.titulo("SIGEPE - Sistema de Gestion de Envios y Paqueteria"))
    print("  Estructuras lineales disponibles: LISTA, PILA y COLA.")
    print("  Se eligio la COLA (FIFO) porque el orden de llegada manda:")
    print("  la primera solicitud registrada es la primera en asignarse.")


def elegir_estructura(sesion):
    print("\n===== 1. Elegir estructura lineal =====")
    for nombre in ESTRUCTURAS:
        marca = " <--(opcion por defecto)" if nombre == "COLA" else ""
        print(f"  {nombre}{marca}")
        print(f"      {CRITERIO_SELECCION[nombre]}")
    while True:
        opcion = input("\nElige la estructura (L/P/C) [C]: ").strip().upper()
        if opcion in ("L", "LISTA"):
            sesion.actual = "LISTA"
        elif opcion in ("P", "PILA"):
            sesion.actual = "PILA"
        elif opcion in ("C", "COLA", ""):
            sesion.actual = "COLA"
        else:
            print("  Opcion no valida.")
            continue
        print(f"  Estructura activa: {consulta.criterio_estructura(sesion.estructura)}")
        return sesion.actual


def mostrar_menu(sesion):
    estructura = sesion.estructura
    print(f"\n===== SIGEPE | {consulta.criterio_estructura(estructura)} =====")
    print(f"  Solicitudes en espera: {estructura.tamanio()}")
    print("  1. Registrar nueva solicitud")
    print("  2. Ver la siguiente solicitud")
    print("  3. Asignar la siguiente a un repartidor")
    print("  4. Cancelar una solicitud por ID")
    print("  5. Listar solicitudes pendientes")
    print("  6. Ver estadisticas de la estructura")
    print("  7. Cargar ejemplo de 5 solicitudes")
    print("  8. Cambiar de estructura lineal")
    print("  9. Vaciar la estructura actual")
    print("  P. Ejecutar pruebas automaticas")
    print("  0. Salir")


# --- Acciones del menu ---

def opcion_registrar(sesion):
    print("\n--- Registrar solicitud ---")
    cliente = pedir_texto("Nombre del cliente: ", 2, 40, "El cliente")
    direccion = pedir_texto("Direccion de entrega: ", 2, 80, "La direccion")
    descripcion = pedir_texto("Descripcion del paquete: ", 2, 80, "La descripcion")
    prioridad = pedir_prioridad()

    id_envio = sesion.generador.emitir(sesion.estructura)
    solicitud, errores = registro.registrar_solicitud(
        sesion.estructura, cliente, direccion, descripcion, prioridad, id_envio)

    if errores:
        for error in errores:
            print(f"  ERROR: {error}")
        return
    print(f"  Solicitud #{solicitud.id_envio} registrada.")
    print(f"  Pendientes: {formato.texto_estado_pendiente(sesion.estructura.tamanio())}")


def opcion_ver_siguiente(sesion):
    print("\n--- Siguiente en salir ---")
    solicitud = consulta.proxima(sesion.estructura)
    if solicitud is None:
        print("  No hay solicitudes pendientes.")
        return
    verbo = {"COLA": "al frente de la cola",
             "PILA": "en la cima de la pila",
             "LISTA": "en la posicion 1 de la lista"}[sesion.actual]
    print(f"  {verbo}: {solicitud}")


def opcion_asignar(sesion):
    print("\n--- Asignar solicitud ---")
    if sesion.estructura.esta_vacia():
        print("  No hay solicitudes pendientes.")
        return
    nombre_repartidor = pedir_repartidor()
    solicitud, repartidor = asignacion.asignar_siguiente(
        sesion.estructura, nombre_repartidor, sesion.historial)
    if solicitud is None:
        print(f"  {repartidor}")
        return
    print(f"  Asignada a {repartidor.nombre}: {solicitud}")
    print(f"  Quedan {formato.texto_estado_pendiente(sesion.estructura.tamanio())}.")


def opcion_cancelar(sesion):
    print("\n--- Cancelar solicitud ---")
    if sesion.estructura.esta_vacia():
        print("  No hay solicitudes pendientes.")
        return
    print("  IDs disponibles:",
          ", ".join(str(i) for i in sesion.estructura.ids()) or "(ninguno)")
    id_envio = pedir_entero("ID de la solicitud a cancelar: ", minimo=1,
                            campo="El ID")
    ok, mensaje = cancelacion.cancelar_solicitud(sesion.estructura, id_envio)
    print(f"  {mensaje}")


def opcion_listar(sesion):
    print("\n--- Solicitudes pendientes ---")
    datos = consulta.ordenar(sesion.estructura, "orden")
    if not datos:
        print("  No hay solicitudes pendientes.")
        return
    print(formato.subtitulo(
        f"{consulta.criterio_estructura(sesion.estructura)}"))
    for linea in formato.tabla_solicitudes(datos):
        print(linea)
    siguiente = consulta.proxima(sesion.estructura)
    if siguiente is not None:
        print(f"  Primero en salir: {formato.resumen_solicitud(siguiente)}")


def opcion_estadisticas(sesion):
    print("\n--- Estadisticas ---")
    datos = consulta.estadisticas(sesion.estructura)
    for linea in formato.estadisticas_texto(datos):
        print(linea)


def opcion_cargar_ejemplo(sesion):
    print("\n--- Cargar ejemplo ---")
    creadas = registro.registrar_varias(sesion.estructura, 5)
    for solicitud in creadas:
        sesion.generador.adoptar([solicitud.id_envio])
    print(f"  {len(creadas)} solicitudes de ejemplo cargadas.")
    opcion_listar(sesion)


def opcion_cambiar_estructura(sesion):
    print()
    elegir_estructura(sesion)
    sesion.generador.reiniciar(1)
    for estructura in sesion.estructuras.values():
        sesion.generador.adoptar(estructura.ids())
    print("  (Cada estructura guarda sus propias solicitudes.)")
    for nombre, estructura in sesion.estructuras.items():
        print(f"      {nombre}: {formato.texto_estado_pendiente(estructura.tamanio())}")


def opcion_vaciar(sesion):
    print("\n--- Vaciar la estructura ---")
    if sesion.estructura.esta_vacia():
        print("  No hay solicitudes pendientes.")
        return
    print(f"  {formato.texto_estado_pendiente(sesion.estructura.tamanio())} "
          f"en {sesion.actual}.")
    if not pedir_confirmacion("  ¿Cancelar todas?", por_defecto=False):
        print("  Operacion cancelada.")
        return
    cantidad = cancelacion.cancelar_todas(sesion.estructura)
    print(f"  Se cancelaron {cantidad} solicitud(es).")


def opcion_pruebas(sesion):
    print("\n--- Pruebas automaticas ---")
    from pruebas import ejecutar_todas
    for linea in ejecutar_todas().splitlines():
        print(f"  {linea}")


# --- Bucle principal ---

ACCIONES = {
    "1": opcion_registrar,
    "2": opcion_ver_siguiente,
    "3": opcion_asignar,
    "4": opcion_cancelar,
    "5": opcion_listar,
    "6": opcion_estadisticas,
    "7": opcion_cargar_ejemplo,
    "8": opcion_cambiar_estructura,
    "9": opcion_vaciar,
    "P": opcion_pruebas,
}


def main(estructura_inicial=None):
    mostrar_bienvenida()
    sesion = Sesion()
    if estructura_inicial:
        nombre = estructura_inicial.upper()
        if nombre in sesion.estructuras:
            sesion.actual = nombre
    else:
        elegir_estructura(sesion)

    while True:
        mostrar_menu(sesion)
        opcion = pedir_opcion("Elige una opcion: ", list(ACCIONES) + [OPCION_SALIR])
        if opcion == OPCION_SALIR:
            print("  Hasta luego.")
            break
        try:
            ACCIONES[opcion](sesion)
        except EstructuraVaciaError as error:
            print(f"  {error}")
        except (TypeError, ValueError) as error:
            print(f"  Dato invalido: {error}")
        except (KeyboardInterrupt, EOFError):
            print("\n  Interrumpido por el usuario.")
            break


if __name__ == "__main__":
    main()
