"""
PRUEBAS de las tres estructuras lineales y de los procesos.

Ejecucion:
    python -m unittest discover -s pruebas -v
    python main.py --pruebas

Cada prueba comprueba el comportamiento que hace que la estructura sea lo
que es: la COLA en FIFO, la PILA en LIFO y la LISTA con acceso por posicion.
"""

import unittest

from estructura_datos.base import EstructuraVaciaError
from estructura_datos.colas import ColaEnvios
from estructura_datos.listas import ListaSolicitudes
from estructura_datos.pilas import PilaEnvios
from modelos.repartidor import Repartidor
from modelos.solicitud import (
    ESTADO_CANCELADO,
    ESTADO_EN_RUTA,
    ESTADO_PENDIENTE,
    Solicitud,
)
from procesos import asignacion, cancelacion, consulta, registro


def solicitud(numero, nombre=None, prioridad="Normal"):
    return Solicitud(numero, nombre or f"Cliente {numero}", "Calle 1",
                     "Paquete", prioridad)


class PruebaCola(unittest.TestCase):
    """La COLA debe comportarse como FIFO."""

    def setUp(self):
        self.cola = ColaEnvios()
        for numero in (1, 2, 3):
            self.cola.encolar(solicitud(numero))

    def test_empieza_vacia(self):
        self.assertTrue(ColaEnvios().esta_vacia())
        self.assertEqual(ColaEnvios().tamanio(), 0)

    def test_encolar_aumenta_el_tamanio(self):
        self.assertEqual(self.cola.tamanio(), 3)
        self.cola.encolar(solicitud(4))
        self.assertEqual(self.cola.tamanio(), 4)

    def test_frente_es_la_mas_antigua(self):
        self.assertEqual(self.cola.frente().id_envio, 1)
        self.assertEqual(self.cola.tamanio(), 3, "peek no debe quitar")

    def test_orden_fifo(self):
        self.assertEqual(self.cola.orden_atencion(), [1, 2, 3])
        self.assertEqual(self.cola.desencolar().id_envio, 1)
        self.assertEqual(self.cola.desencolar().id_envio, 2)
        self.assertEqual(self.cola.desencolar().id_envio, 3)
        self.assertTrue(self.cola.esta_vacia())

    def test_desencolar_vacia_falla(self):
        while not self.cola.esta_vacia():
            self.cola.desencolar()
        with self.assertRaises(EstructuraVaciaError):
            self.cola.desencolar()
        with self.assertRaises(IndexError):
            self.cola.desencolar()

    def test_frente_en_vacia_falla(self):
        self.cola.cancelar(1)
        self.cola.cancelar(2)
        self.cola.cancelar(3)
        with self.assertRaises(EstructuraVaciaError):
            self.cola.frente()

    def test_cancelar_intermedia(self):
        cancelada = self.cola.buscar(2)
        self.assertTrue(self.cola.cancelar(2))
        self.assertEqual(self.cola.orden_atencion(), [1, 3])
        self.assertEqual(cancelada.estado, ESTADO_CANCELADO)
        self.assertIsNone(self.cola.buscar(2), "ya no debe estar en la cola")

    def test_cancelar_inexistente(self):
        self.assertFalse(self.cola.cancelar(99))
        self.assertEqual(self.cola.tamanio(), 3)

    def test_solo_acepta_solicitudes(self):
        with self.assertRaises(TypeError):
            self.cola.encolar("no soy una solicitud")

    def test_iteracion_y_len(self):
        self.assertEqual(len(self.cola), 3)
        self.assertEqual([s.id_envio for s in self.cola], [1, 2, 3])
        self.assertIn(2, self.cola)
        self.assertNotIn(99, self.cola)


class PruebaPila(unittest.TestCase):
    """La PILA debe comportarse como LIFO."""

    def setUp(self):
        self.pila = PilaEnvios()
        for numero in (1, 2, 3):
            self.pila.apilar(solicitud(numero))

    def test_cima_es_la_mas_reciente(self):
        self.assertEqual(self.pila.cima().id_envio, 3)
        self.assertEqual(self.pila.tamanio(), 3, "peek no debe quitar")

    def test_orden_lifo(self):
        self.assertEqual(self.pila.orden_salida(), [3, 2, 1])
        self.assertEqual(self.pila.desapilar().id_envio, 3)
        self.assertEqual(self.pila.desapilar().id_envio, 2)
        self.assertEqual(self.pila.desapilar().id_envio, 1)
        self.assertTrue(self.pila.esta_vacia())

    def test_apilar_al_final(self):
        self.pila.apilar(solicitud(4))
        self.assertEqual(self.pila.ids(), [1, 2, 3, 4])
        self.assertEqual(self.pila.cima().id_envio, 4)

    def test_desapilar_vacia_falla(self):
        while not self.pila.esta_vacia():
            self.pila.desapilar()
        with self.assertRaises(EstructuraVaciaError):
            self.pila.desapilar()

    def test_cancelar_del_medio(self):
        cancelada = self.pila.buscar(2)
        self.assertTrue(self.pila.cancelar(2))
        self.assertEqual(self.pila.ids(), [1, 3])
        self.assertEqual(cancelada.estado, ESTADO_CANCELADO)
        self.assertEqual(self.pila.cantidad_bajo_cima(3), 0, "3 ya es la cima")
        self.assertEqual(self.pila.orden_salida(), [3, 1])

    def test_cantidad_bajo_cima(self):
        self.assertEqual(self.pila.cantidad_bajo_cima(1), 2)
        self.assertEqual(self.pila.cantidad_bajo_cima(3), 0)
        self.assertEqual(self.pila.cantidad_bajo_cima(99), -1)

    def test_historial_es_pila(self):
        historial = asignacion.HistorialAsignaciones()
        historial.registrar(solicitud(1), "A")
        historial.registrar(solicitud(2), "B")
        historial.registrar(solicitud(3), "C")
        self.assertEqual(historial.total(), 3)
        self.assertEqual(historial.mas_reciente()[0].id_envio, 3)
        self.assertEqual([s.id_envio for s, _ in historial.ver_todo()],
                         [3, 2, 1])
        self.assertEqual([s.id_envio for s, _ in historial.desenrollar(2)],
                         [2, 3], "desenrollar entrega de la mas antigua a la mas nueva")
        self.assertEqual(historial.total(), 1)


class PruebaLista(unittest.TestCase):
    """La LISTA debe permitir acceso por posicion, busqueda y reordenamiento."""

    def setUp(self):
        self.lista = ListaSolicitudes()
        self.lista.agregar(solicitud(1, prioridad="Baja"))
        self.lista.agregar(solicitud(2, prioridad="Urgente"))
        self.lista.agregar(solicitud(3, prioridad="Alta"))

    def test_acceso_por_posicion(self):
        self.assertEqual(self.lista.obtener_por_posicion(0).id_envio, 1)
        self.assertEqual(self.lista.obtener_por_posicion(2).id_envio, 3)
        self.assertEqual(self.lista.indice_de(2), 1)
        self.assertEqual(self.lista.indice_de(99), -1)

    def test_posicion_fuera_de_rango(self):
        with self.assertRaises(IndexError):
            self.lista.obtener_por_posicion(9)
        with self.assertRaises(IndexError):
            self.lista.agregar_en_posicion(solicitud(4), 99)

    def test_insertar_en_cualquier_posicion(self):
        self.lista.agregar_al_inicio(solicitud(0))
        self.assertEqual(self.lista.ids(), [0, 1, 2, 3])
        self.lista.agregar_en_posicion(solicitud(9), 2)
        self.assertEqual(self.lista.ids(), [0, 1, 9, 2, 3])

    def test_mover_al_inicio(self):
        self.assertTrue(self.lista.mover_a_inicio(3))
        self.assertEqual(self.lista.ids(), [3, 1, 2])
        self.assertFalse(self.lista.mover_a_inicio(3), "ya esta en la posicion 1")

    def test_mover_arriba(self):
        self.assertTrue(self.lista.mover_arriba(3))
        self.assertEqual(self.lista.ids(), [1, 3, 2])
        self.assertFalse(self.lista.mover_arriba(1), "ya esta arriba")

    def test_ordenar_por_prioridad(self):
        self.lista.ordenar_por_prioridad()
        self.assertEqual(self.lista.ids(), [2, 3, 1])

    def test_ordenar_por_prioridad_conserva_orden_de_llegada(self):
        lista = ListaSolicitudes()
        lista.agregar(solicitud(1, prioridad="Alta"))
        lista.agregar(solicitud(2, prioridad="Alta"))
        lista.agregar(solicitud(3, prioridad="Baja"))
        lista.ordenar_por_prioridad()
        self.assertEqual(lista.ids(), [1, 2, 3])

    def test_ordenar_por_id(self):
        lista = ListaSolicitudes()
        for numero in (3, 1, 2):
            lista.agregar(solicitud(numero))
        lista.ordenar_por_id()
        self.assertEqual(lista.ids(), [1, 2, 3])

    def test_invertir(self):
        self.lista.invertir()
        self.assertEqual(self.lista.ids(), [3, 2, 1])

    def test_quitar_por_id(self):
        self.assertTrue(self.lista.quitar_por_id(2))
        self.assertEqual(self.lista.ids(), [1, 3])
        self.assertFalse(self.lista.quitar_por_id(99))

    def test_quitar_toma_el_primero(self):
        self.assertEqual(self.lista.quitar().id_envio, 1)
        self.assertEqual(self.lista.tamanio(), 2)


class PruebaProcesoRegistro(unittest.TestCase):
    """Validacion de los datos que se ingresan."""

    def setUp(self):
        self.estructura = ColaEnvios()

    def test_registro_correcto(self):
        creada, errores = registro.registrar_solicitud(
            self.estructura, "Ana Perez", "Altamira", "Paquete pequeno")
        self.assertIsNone(errores)
        self.assertEqual(creada.estado, ESTADO_PENDIENTE)
        self.assertEqual(self.estructura.tamanio(), 1)

    def test_rechaza_campos_vacios(self):
        creada, errores = registro.registrar_solicitud(
            self.estructura, "", "Altamira", "Paquete")
        self.assertIsNone(creada)
        self.assertTrue(errores)
        self.assertEqual(self.estructura.tamanio(), 0)

    def test_rechaza_prioridad_inventada(self):
        creada, errores = registro.registrar_solicitud(
            self.estructura, "Ana", "Altamira", "Paquete", "Inmediata")
        self.assertIsNone(creada)
        self.assertTrue(errores)

    def test_texto_muy_largo_se_rechaza(self):
        creada, errores = registro.registrar_solicitud(
            self.estructura, "Ana", "Altamira", "x" * 200)
        self.assertIsNone(creada)
        self.assertTrue(errores)

    def test_registrar_varias(self):
        creadas = registro.registrar_varias(self.estructura, 4)
        self.assertEqual(len(creadas), 4)
        self.assertEqual(self.estructura.tamanio(), 4)

    def test_generador_de_ids_no_repite(self):
        generador = registro.GeneradorIds()
        for numero in (1, 2, 3):
            self.estructura.encolar(solicitud(numero))
        self.assertEqual(generador.emitir(self.estructura), 4)
        generador.adoptar([10, 11])
        self.assertEqual(generador.emitir(self.estructura), 12)

    def test_registro_lote(self):
        creadas, errores = registro.registrar_lote(
            self.estructura,
            [("Ana", "Altamira", "Caja"), ("Luis", "Fontana", "Papeles", "Alta")])
        self.assertEqual(errores, [])
        self.assertEqual(len(creadas), 2)
        self.assertEqual(creadas[1].prioridad, "Alta")


class PruebaProcesoAsignacion(unittest.TestCase):
    """La asignacion debe respetar el criterio de cada estructura."""

    def test_asignar_en_cola(self):
        cola = ColaEnvios()
        registro.registrar_varias(cola, 3)
        solicitud, repartidor = asignacion.asignar_siguiente(cola, "Luis")
        self.assertEqual(solicitud.id_envio, 1)
        self.assertEqual(solicitud.estado, ESTADO_EN_RUTA)
        self.assertEqual(cola.tamanio(), 2)
        self.assertEqual(repartidor.entregas, 1)

    def test_asignar_en_pila(self):
        pila = PilaEnvios()
        registro.registrar_varias(pila, 3)
        solicitud, repartidor = asignacion.asignar_siguiente(pila, "Luis")
        self.assertEqual(solicitud.id_envio, 3, "LIFO: sale la ultima")
        self.assertEqual(pila.tamanio(), 2)

    def test_asignar_en_lista(self):
        lista = ListaSolicitudes()
        registro.registrar_varias(lista, 3)
        solicitud, _ = asignacion.asignar_siguiente(lista, "Luis")
        self.assertEqual(solicitud.id_envio, 1)
        self.assertEqual(lista.tamanio(), 2)

    def test_asignar_por_id_en_lista(self):
        lista = ListaSolicitudes()
        registro.registrar_varias(lista, 3)
        solicitud, repartidor = asignacion.asignar_por_id(lista, 2, "Ana")
        self.assertEqual(solicitud.id_envio, 2)
        self.assertEqual(lista.ids(), [1, 3])
        self.assertEqual(repartidor.nombre, "Ana")

    def test_asignar_por_id_inexistente(self):
        lista = ListaSolicitudes()
        registro.registrar_varias(lista, 2)
        solicitud, motivo = asignacion.asignar_por_id(lista, 99, "Ana")
        self.assertIsNone(solicitud)
        self.assertIn("99", str(motivo))

    def test_asignar_prioridad_alta(self):
        lista = ListaSolicitudes()
        lista.agregar(solicitud(1, prioridad="Baja"))
        lista.agregar(solicitud(2, prioridad="Urgente"))
        lista.agregar(solicitud(3, prioridad="Alta"))
        elegida, _, _ = asignacion.asignar_prioridad_alta(lista, "Ana")
        self.assertEqual(elegida.id_envio, 2, "debe salir la mas urgente")
        self.assertEqual(lista.ids(), [3, 1])

    def test_asignar_prioridad_alta_en_cola_avisa(self):
        cola = ColaEnvios()
        registro.registrar_varias(cola, 2)
        elegida, _, aviso = asignacion.asignar_prioridad_alta(cola, "Ana")
        self.assertEqual(elegida.id_envio, 1, "la cola no se puede reordenar")
        self.assertIn("no se puede reordenar", aviso)

    def test_asignar_vacia(self):
        solicitud, motivo = asignacion.asignar_siguiente(ColaEnvios(), "Ana")
        self.assertIsNone(solicitud)
        self.assertIn("No hay solicitudes", str(motivo))

    def test_asignar_todas(self):
        cola = ColaEnvios()
        registro.registrar_varias(cola, 4)
        repartidor = Repartidor("Luis", "Norte")
        resultado = asignacion.asignar_todas(cola, repartidor)
        self.assertEqual(len(resultado), 4)
        self.assertTrue(cola.esta_vacia())
        self.assertEqual(repartidor.entregas, 4)
        self.assertEqual([s.id_envio for s, _ in resultado], [1, 2, 3, 4])

    def test_historial_guarda_el_orden(self):
        cola = ColaEnvios()
        registro.registrar_varias(cola, 2)
        historial = asignacion.HistorialAsignaciones()
        asignacion.asignar_siguiente(cola, "A", historial)
        asignacion.asignar_siguiente(cola, "B", historial)
        self.assertEqual([s.id_envio for s, _ in historial.ver_todo()], [2, 1])

    def test_marcar_entregado(self):
        cola = ColaEnvios()
        cola.encolar(solicitud(1))
        asignacion.asignar_siguiente(cola, "A")
        _, motivo = asignacion.marcar_entregado(cola, 1)
        self.assertIn("ya no esta", str(motivo))


class PruebaProcesoCancelacion(unittest.TestCase):
    """La cancelacion debe sacar la solicitud de la estructura."""

    def setUp(self):
        self.cola = ColaEnvios()
        registro.registrar_varias(self.cola, 3)

    def test_cancelar_existente(self):
        ok, mensaje = cancelacion.cancelar_solicitud(self.cola, 2)
        self.assertTrue(ok)
        self.assertIn("cancelada", mensaje)
        self.assertEqual(self.cola.tamanio(), 2)

    def test_cancelar_inexistente(self):
        ok, mensaje = cancelacion.cancelar_solicitud(self.cola, 99)
        self.assertFalse(ok)
        self.assertIn("No se encontro", mensaje)

    def test_cancelar_ultima(self):
        ok, _ = cancelacion.cancelar_ultima(self.cola)
        self.assertTrue(ok)
        self.assertEqual(self.cola.ids(), [2, 3])

    def test_cancelar_todas(self):
        cantidad = cancelacion.cancelar_todas(self.cola)
        self.assertEqual(cantidad, 3)
        self.assertTrue(self.cola.esta_vacia())

    def test_cancelar_por_cliente(self):
        cola = ColaEnvios()
        cola.encolar(solicitud(1, "Ana Perez"))
        cola.encolar(solicitud(2, "Luis Mora"))
        cola.encolar(solicitud(3, "Ana Perez"))
        cantidad = cancelacion.cancelar_cliente(cola, "ana perez")
        self.assertEqual(cantidad, 2)
        self.assertEqual(cola.ids(), [2])

    def test_cancelar_en_pila(self):
        pila = PilaEnvios()
        registro.registrar_varias(pila, 3)
        self.assertTrue(cancelacion.cancelar_solicitud(pila, 1)[0])
        self.assertEqual(pila.ids(), [2, 3])


class PruebaProcesoConsulta(unittest.TestCase):
    """Filtros y estadisticas."""

    def setUp(self):
        self.lista = ListaSolicitudes()
        self.lista.agregar(solicitud(1, "Ana Perez", "Baja"))
        self.lista.agregar(solicitud(2, "Luis Mora", "Urgente"))
        self.lista.agregar(solicitud(3, "Ana Perez", "Alta"))

    def test_pendientes(self):
        cola = ColaEnvios()
        registro.registrar_varias(cola, 2)
        asignacion.asignar_siguiente(cola, "A")
        self.assertEqual(len(consulta.pendientes(cola)), 1)

    def test_proxima_vacia(self):
        self.assertIsNone(consulta.proxima(ColaEnvios()))

    def test_buscar_por_cliente(self):
        encontrados = consulta.buscar_por_cliente(self.lista, "ana")
        self.assertEqual([s.id_envio for s in encontrados], [1, 3])

    def test_buscar_por_direccion(self):
        self.assertEqual(len(consulta.buscar_por_direccion(self.lista, "calle")), 3)
        self.assertEqual(len(consulta.buscar_por_direccion(self.lista, "zzz")), 0)

    def test_filtrar_por_prioridad(self):
        self.assertEqual(
            [s.id_envio for s in consulta.filtrar_por_prioridad(self.lista, "Urgente")],
            [2])

    def test_ordenar_por_prioridad(self):
        datos = consulta.ordenar(self.lista, "prioridad")
        self.assertEqual([s.id_envio for s in datos], [2, 3, 1])

    def test_ordenar_no_modifica(self):
        consulta.ordenar(self.lista, "cliente")
        self.assertEqual(self.lista.ids(), [1, 2, 3])

    def test_criterio_de_cada_estructura(self):
        self.assertIn("COLA", consulta.criterio_estructura(ColaEnvios()))
        self.assertIn("PILA", consulta.criterio_estructura(PilaEnvios()))
        self.assertIn("LISTA", consulta.criterio_estructura(ListaSolicitudes()))

    def test_estadisticas(self):
        datos = consulta.estadisticas(self.lista)
        self.assertEqual(datos["total_elementos"], 3)
        self.assertEqual(datos["pendientes"], 3)
        self.assertEqual(datos["clientes"], 2)
        self.assertIn("1", datos["siguiente_en_salir"])

    def test_operaciones_por_estructura(self):
        cola = ", ".join(consulta.descripcion_operaciones(ColaEnvios()))
        pila = ", ".join(consulta.descripcion_operaciones(PilaEnvios()))
        lista = ", ".join(consulta.descripcion_operaciones(ListaSolicitudes()))
        self.assertIn("encolar", cola)
        self.assertIn("desencolar", cola)
        self.assertIn("apilar", pila)
        self.assertIn("cima", pila)
        self.assertIn("mover_a_inicio", lista)


class PruebaPruebasDelModuloOriginal(unittest.TestCase):
    """Las 4 pruebas que traia el archivo original, ahora por estructura."""

    def test_prueba_1_encolar_y_tamanio(self):
        cola = ColaEnvios()
        self.assertTrue(cola.esta_vacia())
        cola.encolar(Solicitud(1, "Ana Perez", "Altamira", "Paquete pequeno"))
        cola.encolar(Solicitud(2, "Luis Mora", "Villa Fontana", "Documentos"))
        cola.encolar(Solicitud(3, "Rosa Gomez", "Bello Horizonte", "Comida"))
        self.assertEqual(cola.tamanio(), 3)

    def test_prueba_2_orden_fifo(self):
        cola = ColaEnvios()
        registro.registrar_varias(cola, 3)
        self.assertEqual(cola.frente().id_envio, 1)
        solicitud, repartidor = asignacion.asignar_siguiente(cola, "Repartidor 1")
        self.assertEqual(solicitud.id_envio, 1)
        self.assertEqual(solicitud.estado, ESTADO_EN_RUTA)
        self.assertEqual(repartidor.nombre, "Repartidor 1")

    def test_prueba_3_cancelar_intermedia(self):
        cola = ColaEnvios()
        registro.registrar_varias(cola, 3)
        asignacion.asignar_siguiente(cola, "Repartidor 1")   # sale la 1
        self.assertTrue(cola.cancelar(3))                     # se cancela la 3
        self.assertEqual(cola.tamanio(), 1)
        self.assertEqual(cola.frente().id_envio, 2)

    def test_prueba_4_cola_vacia_controlada(self):
        cola = ColaEnvios()
        registro.registrar_varias(cola, 1)
        cola.desencolar()
        self.assertTrue(cola.esta_vacia())
        with self.assertRaises(IndexError):
            cola.desencolar()

    def test_prueba_5_historial_en_pila(self):
        """La version nueva del modulo tambien muestra la PILA en accion."""
        pila = PilaEnvios()
        registro.registrar_varias(pila, 3)
        self.assertEqual(pila.cima().id_envio, 3)
        cancelacion.cancelar_solicitud(pila, 2)
        self.assertEqual(pila.ids(), [1, 3])


if __name__ == "__main__":
    unittest.main(verbosity=2)
