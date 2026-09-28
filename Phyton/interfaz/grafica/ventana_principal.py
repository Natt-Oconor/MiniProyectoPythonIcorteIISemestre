"""
Interfaz GRAFICA - Ventana principal (tkinter).

Arma la pantalla completa del SIGEPE:

    +---------------------------------------------------------------+
    | Menu: Archivo | Herramientas | Ayuda                           |
    +---------------------------------------------------------------+
    | FORMULARIO DE REGISTRO    |  PESTANAS: COLA | PILA | LISTA     |
    | (datos que pide el        |  tabla de la estructura +         |
    |  sistema)                 |  boton de asignar                 |
    +---------------------------------------------------------------+
    | Actividad            | Historial de asignaciones (PILA)         |
    +---------------------------------------------------------------+
    | Barra de estado                                                 |
    +---------------------------------------------------------------+

El `import tkinter` va dentro de un try a proposito: si el sistema no tiene
tkinter, este modulo todavia se puede importar y la aplicacion cae
automaticamente en la version de consola.
"""

try:
    import tkinter as tk
    from tkinter import messagebox, ttk
    TKINTER_DISPONIBLE = True
except ImportError:
    TKINTER_DISPONIBLE = False
    tk = None
    ttk = None
    messagebox = None

from estructura_datos import CRITERIO_SELECCION
from estructura_datos.colas import ColaEnvios
from estructura_datos.listas import ListaSolicitudes
from estructura_datos.pilas import PilaEnvios
from procesos import asignacion, cancelacion, consulta, registro
from utilidades import formato
from interfaz.grafica.widgets import (
    aplicar_estilos,
    crear_area_texto,
    escribir_log,
    mostrar_texto,
)
from interfaz.grafica.formulario_solicitud import FormularioSolicitud
from interfaz.grafica.pestana_estructura import PestanaEstructura

ESTRUCTURAS = {
    "COLA": ColaEnvios,
    "PILA": PilaEnvios,
    "LISTA": ListaSolicitudes,
}

AYUDA = (
    "COMO USAR ESTA APLICACION\n\n"
    "1. Formulario de la izquierda\n"
    "   Escribe Cliente, Direccion, Descripcion y Prioridad, y presiona\n"
    "   'Registrar'. La solicitud entra en la pestana que este abierta.\n\n"
    "2. Pestanas COLA, PILA y LISTA\n"
    "   Cada una guarda sus propias solicitudes. La fila resaltada es la\n"
    "   que sale primero segun el criterio de esa estructura.\n\n"
    "3. Asignar\n"
    "   Escribe el nombre del repartidor y presiona el boton de asignar.\n"
    "   En la LISTA te pide el ID de la solicitud concreta.\n\n"
    "4. Cancelar o Marcar entregado\n"
    "   Marca una fila de la tabla y usa el boton correspondiente.\n\n"
    "5. Historial de la derecha\n"
    "   Guarda las asignaciones en una PILA: el ultimo movimiento sale\n"
    "   primero, por eso el mas reciente aparece arriba.\n\n"
    "Atajo: en el formulario, Enter registra la solicitud."
)

ACERCA_DE = (
    "SIGEPE v2.0\n"
    "Seleccion de la estructura lineal apropiada: Lista, Pila y Cola.\n\n"
    "Capas separadas por responsabilidad:\n"
    "  modelos/          clases de datos (Solicitud, Repartidor)\n"
    "  estructura_datos/ listas, pilas, colas\n"
    "  procesos/         reglas de negocio\n"
    "  utilidades/       funciones de validacion y formato\n"
    "  interfaz/         consola y grafica\n"
    "  pruebas/          pruebas automaticas"
)


if TKINTER_DISPONIBLE:

    class VentanaPrincipal(tk.Tk):
        """Ventana principal del sistema."""

        def __init__(self):
            super().__init__()
            self.title("SIGEPE - Sistema de Gestion de Envios y Paqueteria")
            self.geometry("1180x740")
            self.minsize(1000, 620)

            # --- Estado de la aplicacion ---
            self.estructuras = {nombre: clase()
                                for nombre, clase in ESTRUCTURAS.items()}
            self.generador = registro.GeneradorIds()
            self.historial = asignacion.HistorialAsignaciones()
            self.solicitudes_asignadas = []

            aplicar_estilos(self)
            self._construir_menu()
            self._construir_encabezado()
            self._construir_cuerpo()
            self._construir_pie()

            self.protocol("WM_DELETE_WINDOW", self.cerrar)
            self.cargar_ejemplo(silencioso=True)
            self.refrescar_todo()

        # ================= Construccion de la pantalla =================

        def _construir_menu(self):
            barra = tk.Menu(self)

            archivo = tk.Menu(barra, tearoff=0)
            archivo.add_command(label="Cargar ejemplo",
                                command=self.cargar_ejemplo)
            archivo.add_command(label="Vaciar todo", command=self.vaciar_todo)
            archivo.add_separator()
            archivo.add_command(label="Salir", command=self.cerrar)
            barra.add_cascade(label="Archivo", menu=archivo)

            herramientas = tk.Menu(barra, tearoff=0)
            herramientas.add_command(label="Ejecutar pruebas automaticas",
                                     command=self.ejecutar_pruebas)
            herramientas.add_command(label="Criterio de seleccion",
                                     command=self.mostrar_criterio)
            barra.add_cascade(label="Herramientas", menu=herramientas)

            ayuda = tk.Menu(barra, tearoff=0)
            ayuda.add_command(label="Como usar la app", command=self.mostrar_ayuda)
            ayuda.add_command(label="Acerca de", command=self.mostrar_acerca_de)
            barra.add_cascade(label="Ayuda", menu=ayuda)

            self.config(menu=barra)

        def _construir_encabezado(self):
            marco = ttk.Frame(self, padding=(14, 10, 14, 4))
            marco.pack(fill="x")
            ttk.Label(marco, text="SIGEPE", style="Titulo.TLabel").pack(side="left")
            ttk.Label(
                marco,
                text="Seleccion de la estructura lineal apropiada: "
                     "Lista  |  Pila  |  Cola",
                style="Subtitulo.TLabel").pack(side="left", padx=16)
            self.var_rotulo_estructura = tk.StringVar(value="")
            ttk.Label(marco, textvariable=self.var_rotulo_estructura,
                      style="Rotulo.TLabel").pack(side="right")

        def _construir_cuerpo(self):
            marco = ttk.Frame(self, padding=(12, 4, 12, 0))
            marco.pack(fill="both", expand=True)
            marco.columnconfigure(0, weight=0, minsize=330)
            marco.columnconfigure(1, weight=1)
            marco.rowconfigure(0, weight=1)

            # Columna izquierda: los datos que pide el sistema.
            self.formulario = FormularioSolicitud(
                marco, on_registrar=self.registrar_solicitud)
            self.formulario.grid(row=0, column=0, sticky="nsw", padx=(0, 10))

            # Columna derecha: una pestana por estructura lineal.
            derecha = ttk.Frame(marco)
            derecha.grid(row=0, column=1, sticky="nsew")

            self.notebook = ttk.Notebook(derecha)
            self.notebook.pack(fill="both", expand=True)

            self.pestanas = {}
            for nombre in ESTRUCTURAS:
                pestana = PestanaEstructura(
                    self.notebook, nombre, self.estructuras[nombre],
                    on_asignar=self.asignar,
                    on_cancelar=self.cancelar,
                    on_entregar=self.marcar_entregado,
                    on_recargar=self.refrescar_todo,
                    on_log=self.registrar_log)
                self.notebook.add(pestana, text=f"{nombre}  ({self.nombre_corto(nombre)})")
                self.pestanas[nombre] = pestana

            self.notebook.bind("<<NotebookTabChanged>>", self.al_cambiar_pestana)

        def _construir_pie(self):
            self.barra_estado = ttk.Label(
                self, text="  Listo.", style="Estado.TLabel", anchor="w",
                padding=(12, 5))
            self.barra_estado.pack(fill="x", side="bottom", pady=(6, 0))

            marco = ttk.Frame(self, padding=(12, 8, 12, 0))
            marco.pack(fill="both", expand=False)
            marco.columnconfigure(0, weight=3)
            marco.columnconfigure(1, weight=2)
            marco.rowconfigure(0, weight=1)

            actividad = ttk.LabelFrame(marco, text="Actividad reciente",
                                       padding=8)
            actividad.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
            marco_log, self.log = crear_area_texto(actividad, alto=8)
            marco_log.pack(fill="both", expand=True)

            historial = ttk.LabelFrame(
                marco, text="Historial de asignaciones (PILA - el ultimo sale primero)",
                padding=8)
            historial.grid(row=0, column=1, sticky="nsew")
            marco_historial, self.historico = crear_area_texto(historial, alto=8)
            marco_historial.pack(fill="both", expand=True)

        # ================= Utilidades de apoyo =================

        @staticmethod
        def nombre_corto(nombre):
            return {"COLA": "FIFO", "PILA": "LIFO",
                    "LISTA": "posicional"}.get(nombre, "")

        def pestana_activa(self):
            """Nombre de la estructura de la pestana visible."""
            indice = self.notebook.index("current")
            if indice is None:
                return "COLA"
            texto = self.notebook.tab(indice, "text").split()[0]
            return texto if texto in self.estructuras else "COLA"

        # ================= Operaciones =================

        def registrar_solicitud(self, datos):
            """Callback del formulario: inserta en la pestana activa."""
            nombre = self.pestana_activa()
            estructura = self.estructuras[nombre]

            id_envio = self.generador.emitir(estructura)
            solicitud, errores = registro.registrar_solicitud(
                estructura, datos["cliente"], datos["direccion"],
                datos["descripcion"], datos["prioridad"], id_envio)

            if errores:
                messagebox.showerror("Datos invalidos", "\n".join(errores),
                                     parent=self)
                return False

            self.refrescar_todo()
            self.registrar_log(f"Solicitud #{solicitud.id_envio} registrada "
                               f"en la {nombre}: {solicitud.cliente} "
                               f"({solicitud.prioridad})")
            return True

        def asignar(self, nombre, repartidor_texto, id_envio=None):
            """Asigna la proxima solicitud (o la indicada, en la LISTA)."""
            estructura = self.estructuras[nombre]
            if estructura.esta_vacia():
                messagebox.showinfo(
                    "Sin solicitudes",
                    f"No hay solicitudes pendientes en la {nombre}.",
                    parent=self)
                return

            if id_envio is None:
                solicitud, repartidor = asignacion.asignar_siguiente(
                    estructura, repartidor_texto, self.historial)
                if solicitud is None:
                    messagebox.showinfo("No se pudo asignar",
                                        str(repartidor), parent=self)
                    return
            else:
                solicitud, repartidor = asignacion.asignar_por_id(
                    estructura, id_envio, repartidor_texto, self.historial)
                if solicitud is None:
                    messagebox.showinfo("No se pudo asignar",
                                        str(repartidor), parent=self)
                    return

            self.solicitudes_asignadas.append(solicitud)
            self.refrescar_todo()
            self.registrar_log(
                f"[{nombre}] #{solicitud.id_envio} {solicitud.cliente} "
                f"-> {repartidor.nombre} (Entregas: {repartidor.entregas})")

        def cancelar(self, nombre, id_envio):
            ok, mensaje = cancelacion.cancelar_solicitud(
                self.estructuras[nombre], id_envio)
            if ok:
                self.registrar_log(f"[{nombre}] {mensaje}")
            else:
                messagebox.showwarning("No se pudo cancelar", mensaje, parent=self)
            self.refrescar_todo()
            return ok

        def marcar_entregado(self, nombre, id_envio):
            for solicitud in self.solicitudes_asignadas:
                if solicitud.id_envio == id_envio:
                    solicitud.marcar_entregado()
                    self.registrar_log(
                        f"Solicitud #{id_envio} de {solicitud.cliente} "
                        f"marcada como Entregado.")
                    self.refrescar_todo()
                    return True
            messagebox.showinfo(
                "Sin asignacion",
                f"La solicitud #{id_envio} de la {nombre} todavia no fue "
                "asignada.\n\nAsignala primero para poder marcarla como "
                "entregada.", parent=self)
            return False

        def cargar_ejemplo(self, silencioso=False):
            total = 0
            for estructura in self.estructuras.values():
                creadas = registro.registrar_varias(estructura, 5)
                for solicitud in creadas:
                    self.generador.adoptar([solicitud.id_envio])
                total += len(creadas)
            if not silencioso:
                self.refrescar_todo()
                self.registrar_log(
                    f"Ejemplo cargado: 5 solicitudes en cada estructura "
                    f"({total} en total).")
            return total

        def vaciar_todo(self):
            respuesta = messagebox.askyesno(
                "Vaciar todo",
                "Se cancelaran todas las solicitudes de las tres "
                "estructuras\ny se borrara el historial.\n\n¿Continuar?",
                parent=self)
            if not respuesta:
                return
            for estructura in self.estructuras.values():
                cancelacion.cancelar_todas(estructura)
            self.solicitudes_asignadas.clear()
            self.historial.limpiar()
            self.generador.reiniciar(1)
            self.refrescar_todo()
            self.registrar_log("Se vaciaron las tres estructuras.")

        def ejecutar_pruebas(self):
            from pruebas import ejecutar_todas
            messagebox.showinfo("Pruebas automaticas", ejecutar_todas(),
                                parent=self)

        def mostrar_criterio(self):
            lineas = ["Por que se eligio cada estructura:\n"]
            for nombre, estructura in self.estructuras.items():
                lineas.append(nombre)
                lineas.append(f"   {consulta.criterio_estructura(estructura)}")
                operaciones = ", ".join(
                    consulta.descripcion_operaciones(estructura))
                lineas.append(f"   Operaciones: {operaciones}")
                lineas.append("")
            lineas.append("Regla:")
            lineas.append("  La lista es la estructura general. La pila y la")
            lineas.append("  cola son listas con la insercion y la extraccion")
            lineas.append("  restringidas a un solo extremo.")
            messagebox.showinfo("Criterio de seleccion", "\n".join(lineas),
                                parent=self)

        def mostrar_ayuda(self):
            messagebox.showinfo("Guia rapida", AYUDA, parent=self)

        def mostrar_acerca_de(self):
            messagebox.showinfo("Acerca de SIGEPE", ACERCA_DE, parent=self)

        # ================= Refresco =================

        def refrescar_todo(self):
            for nombre, pestana in self.pestanas.items():
                pestana.refrescar(self.estructuras[nombre])
            self.refrescar_historial()
            activa = self.pestana_activa()
            self.var_rotulo_estructura.set(
                CRITERIO_SELECCION.get(activa, ""))

        def refrescar_historial(self):
            if self.historial.total() == 0:
                lineas = formato.tabla_simple(
                    [], vacio="Todavia no hay asignaciones.")
            else:
                lineas = formato.tabla_simple(
                    [f"#{s.id_envio}  {s.cliente}  ->  {r.nombre} "
                     f"({r.entregas} entregas)"
                     for s, r in self.historial.ver_todo()])
            mostrar_texto(self.historico, lineas)

        def registrar_log(self, mensaje):
            escribir_log(self.log, mensaje)
            pendientes = sum(e.tamanio() for e in self.estructuras.values())
            self.barra_estado.configure(
                text=f"  En espera: {pendientes}   |   "
                     f"Asignadas: {len(self.solicitudes_asignadas)}   |   "
                     f"Historial: {self.historial.total()}   |   {mensaje}")

        def al_cambiar_pestana(self, _evento=None):
            self.refrescar_todo()

        def cerrar(self):
            self.destroy()

    def ejecutar():
        """Abre la ventana grafica del SIGEPE."""
        app = VentanaPrincipal()
        app.mainloop()
        return app

else:
    VentanaPrincipal = None

    def ejecutar():
        raise RuntimeError(
            "tkinter no esta instalado en este sistema. "
            "Usa la version de consola:  python main.py --consola")


if __name__ == "__main__":
    ejecutar()
